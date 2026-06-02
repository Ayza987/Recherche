from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from app.database.database import Base


class Sensor(Base):

    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True)

    serial_number = Column(String)

    firmware = Column(String)

    hardware = Column(String)

    master_ip = Column(String)

    port = Column(Integer)

    active = Column(Boolean)


class SensorReading(Base):

    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True)

    sensor_id = Column(
        Integer,
        ForeignKey("sensors.id")
    )

    operating_hours = Column(Integer)

    power_cycles = Column(Integer)

    device_status = Column(String)

    timestamp = Column(DateTime)