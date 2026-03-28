from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey # type: ignore
from sqlalchemy.sql import func # type:ignore
from database import Base

class Device(Base):
    """
    The Nodes: Represents every device discovered on your network.
    """
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, default="Unknown Device")
    ip_address = Column(String, unique=True, index=True, nullable=False)
    mac_address = Column(String, unique=True, index=True, nullable=False)
    device_role = Column(String, default="host") # router, switch, workstation, iot
    status = Column(String, default="online")    # online, offline, warning, compromised
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class TopologyLink(Base):
    """
    The Edges: Represents the physical or logical links between devices.
    """
    __tablename__ = "topology_links"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String, nullable=False) # Key of the source node
    target_id = Column(String, nullable=False) # Key of the target node
    link_type = Column(String, default="ethernet")
    is_active = Column(Boolean, default=True)

class Event(Base):
    """
    The IDS Alerts: Every suspicious packet found in the logs.
    """
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    severity = Column(String, index=True)        # low, medium, high, critical
    signature = Column(String)                   # e.g., "Potential Port Scan"
    source_ip = Column(String, index=True)
    dest_ip = Column(String)
    protocol = Column(String)                    # TCP, UDP, ICMP
    action = Column(String, default="LOGGED")    # LOGGED, BLOCKED
    payload_preview = Column(String, nullable=True)