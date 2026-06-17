from app.database.models import SensorReading


class SensorRepository:

    @staticmethod
    def save(db, sensor):

        health = sensor.get(
            "health_parameters",
            {}
        )

        row = SensorReading(

            port=sensor.get(
                "port"
            ),

            port_label=sensor.get(
                "port_label"
            ),

            serial_number=health.get(
                "serial_number",
                {}
            ).get(
                "hex_value"
            ),

            firmware=health.get(
                "firmware",
                {}
            ).get(
                "hex_value"
            ),

            hardware=health.get(
                "hardware",
                {}
            ).get(
                "hex_value"
            ),

            operating_hours=health.get(
                "operating_hours",
                {}
            ).get(
                "hex_value"
            ),

            power_on_cycles=health.get(
                "power_on_cycles",
                {}
            ).get(
                "hex_value"
            ),

            device_status=sensor.get(
                "device_status_label"
            ),

            pdin_hex=sensor.get(
                "pdin_hex"
            ),

            iolinkevent_hex=sensor.get(
                "iolinkevent_hex"
            )
        )

        db.add(row)

        db.commit()