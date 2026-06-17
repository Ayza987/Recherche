'''from app.services.master_service import IFMClient
from app.services.decoder_service import DecoderService


class CollectorService:

    def __init__(self):

        self.client = IFMClient()

    def collect(self):

        result = []

        for port in range(1, 9):

            data = self.client.get_full_port_health(
                port
            )

            if not data.get(
                "connected"
            ):
                continue

            health = data.get(
                "health_parameters",
                {}
            )

            sensor = {

                "port": port,

                "serial_number":
                    DecoderService.hex_to_string(
                        health.get(
                            "serial_number",
                            {}
                        ).get(
                            "hex_value",
                            ""
                        )
                    ),

                "firmware":
                    DecoderService.hex_to_string(
                        health.get(
                            "firmware",
                            {}
                        ).get(
                            "hex_value",
                            ""
                        )
                    ),

                "hardware":
                    DecoderService.hex_to_string(
                        health.get(
                            "hardware",
                            {}
                        ).get(
                            "hex_value",
                            ""
                        )
                    ),

                "operating_hours":
                    DecoderService.hex_to_int(
                        health.get(
                            "operating_hours",
                            {}
                        ).get(
                            "hex_value",
                            "0"
                        )
                    ),

                "power_on_cycles":
                    health.get(
                        "power_on_cycles",
                        {}
                    ).get(
                        "hex_value",
                        ""
                    ),

                "device_status":
                    data.get(
                        "device_status_label"
                    )
            }

            result.append(
                sensor
            )

        return result'''