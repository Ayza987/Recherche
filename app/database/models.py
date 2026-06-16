from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
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

    serial_number = Column(String)

    firmware = Column(String)

    hardware = Column(String)

    operating_hours = Column(Integer)

    power_on_cycles = Column(String)

    device_status = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )