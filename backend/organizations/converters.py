class INNConverter:
    regex = r"\d{10}|\d{12}"

    def to_python(self, value: str) -> str:
        return value

    def to_url(self, value: str) -> str:
        return value