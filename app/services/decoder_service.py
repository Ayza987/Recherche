class DecoderService:

    @staticmethod
    def hex_to_string(value):

        try:

            return bytes.fromhex(
                value
            ).decode(
                "utf-8",
                errors="ignore"
            )

        except:

            return value

    @staticmethod
    def hex_to_int(value):

        try:

            return int(
                value,
                16
            )

        except:

            return None