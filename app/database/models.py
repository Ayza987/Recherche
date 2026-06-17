from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime

from datetime import datetime

from app.database.database import Base


class SensorReading(Base):

    __tablename__ = "sensor_readings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    port = Column(Integer)

    port_label = Column(String)

    serial_number = Column(String)

    firmware = Column(String)

    hardware = Column(String)

    operating_hours = Column(String)

    power_on_cycles = Column(String)

    device_status = Column(String)

    pdin_hex = Column(Text)

    iolinkevent_hex = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )