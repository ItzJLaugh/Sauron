#!/bin/bash
#
iptables -N ICMP_LIMIT
iptables -N syn_flood

#set default policies
iptables -P INPUT -j DROP
iptables -P OUTPUT -j DROP
iptables -P FORWARD -j DROP
#set input
iptables -A INPUT -i lo -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -p tcp -p tcp -m tcp --dport 4477 -m state --state NEW,ESTABLISHED -j ACCPT
iptables -A INPUT -p tcp -p tcp -m tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -m hashlimit --hashlimit-upto 2/sec --hashlimit-burst 2 --hashlimit-mode srcip --hashlimit-name
iptables -A INPUT -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -j syn_flood
iptables -A INPUT -p udp -m udp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -p udp -m udp --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 53 -m stat --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -j LOG --log-prefix "IDS-DROP " --log-level 4

#set output
iptables -A OUTPUT -i lo -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -p tcp -m tcp --sport 4477 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -m tcp -m tcp --sport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p udp -m udp --sport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -m tcp --sport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p udp -m udp --sport 443 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -m tcp --sport 443 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -m tcp --sport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -m tcp --sport 8000 -m state --state NEW,ESTABLISHED -j ACCEPT

#set forward
iptables -A FORWARD -i lo -m state --state NEW,ESTABLISHED -j ACCEPT
#set custom

#syn_flood

iptables -A syn_flood -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -m limit --limit 1/sec --limit-burst 3 -j ACCEPT
iptables -A syn_flood -p tcp -m tcp -j LOG --log-prefix "IDS-SYN-FLOOD"
iptables -A syn_flood -j DROP

#icmp_limit

iptables -A INPUT -p icmp -j ICMP_LIMIT
iptables -A ICMP_LIMIT -p icmp -m length --length 20:1492 -j ACCEPT
iptables -A ICMP_LIMIT -m limit --limit 10/sec --limit-burst 3 -j LOG --log-prefix "ICMP_FRAG iptables:" --log-level 7
iptables -A ICMP_LIMIT -j DROP

