# Service de communication avec les masters IO-Link

import httpx


class MasterService:

    def __init__(self, ip):

        self.base_url = f"http://{ip}/iolink/v1/"


    async def request(
        self,
        cid,
        adr
    ):

        payload = {
            "code": "request",
            "cid": cid,
            "adr": adr,
            "data": {}
        }

        async with httpx.AsyncClient() as client:

            response = await client.post(
                self.base_url,
                json=payload,
                timeout=10
            )

            return response.json()