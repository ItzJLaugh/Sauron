from sqlalchemy import Column, Integer, String, DateTime, Boolean  # type: ignore
from sqlalchemy.sql import func  # type: ignore
from database import Base


class Device(Base):
    """Represents every device discovered on the network."""
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, default="Unknown Device")
    ip_address = Column(String, unique=True, index=True, nullable=False)
    mac_address = Column(String, unique=True, index=True, nullable=False)
    device_role = Column(String, default="host")
    status = Column(String, default="online")
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class TopologyLink(Base):
    """Represents physical or logical links between devices."""
    __tablename__ = "topology_links"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String, nullable=False)
    target_id = Column(String, nullable=False)
    link_type = Column(String, default="ethernet")
    is_active = Column(Boolean, default=True)


class Event(Base):
    """Every iptables log entry parsed from kern.log."""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    severity = Column(String, index=True)
    signature = Column(String)
    source_ip = Column(String, index=True)
    dest_ip = Column(String)
    protocol = Column(String)
    action = Column(String, default="LOGGED")
    payload_preview = Column(String, nullable=True)
