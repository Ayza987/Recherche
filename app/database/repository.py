from app.database.models import SensorReading


class SensorRepository:

    @staticmethod
    def save(db, sensor):

        row = SensorReading(

            port=sensor.get("port"),

            serial_number=sensor.get(
                "serial_number"
            ),

            firmware=sensor.get(
                "firmware"
            ),

            hardware=sensor.get(
                "hardware"
            ),

            operating_hours=sensor.get(
                "operating_hours"
            ),

            power_on_cycles=sensor.get(
                "power_on_cycles"
            ),

            device_status=sensor.get(
                "device_status"
            )
        )

        db.add(row)

        db.commit()