from app.services.ifm_client import IFMClient


class MasterService:

    def __init__(self):

        self.client = IFMClient()

    def collect(self):

        ports = []

        for port in range(1, 9):

            try:

                port_data = self.client.get_full_port_health(
                    port
                )

                ports.append(
                    port_data
                )

            except Exception as e:

                ports.append(
                    {
                        "port": port,
                        "error": str(e)
                    }
                )

        return {
            "master_ip": self.client.endpoint,
            "ports": ports
        }