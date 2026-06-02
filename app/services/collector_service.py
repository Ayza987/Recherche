# Boucle de collecte temps réel

from datetime import datetime
import random


class CollectorService:

    async def collect(self):

        return {

            "sensor": "distance_sensor",

            "operating_hours": random.randint(
                35,
                45
            ),

            "power_cycles": random.randint(
                45,
                55
            ),

            "device_status": random.choice(
                [
                    "operational",
                    "warning",
                    "maintenance"
                ]
            ),

            "timestamp": datetime.now().isoformat()
        }