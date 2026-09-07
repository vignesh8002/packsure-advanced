
import re


class EntityExtractor:

    def extract_mrp(self, text):
        patterns = [
            r"MRP\s*[:\-]?\s*(?:Rs\.?|₹)?\s*(\d+(?:\.\d+)?)",
            r"MAXIMUM\s*RETAIL\s*PRICE\s*[:\-]?\s*(?:Rs\.?|₹)?\s*(\d+(?:\.\d+)?)"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                return match.group(1)

        return None

    def extract_batch_number(self, text):
        pattern = (
            r"(?:B\.?NO\.?|BATCH\s*NO\.?|BATCH)"
            r"\s*[:\-]?\s*([A-Z0-9\/\-]+)"
        )

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1)

        return None

    def extract_dates(self, text):
        pattern = r"\b\d{2}[\/\-]\d{2}[\/\-]\d{2,4}\b"

        return re.findall(pattern, text)

    def extract_net_quantity(self, text):
        patterns = [
            r"(?:NET\s*(?:QTY|QUANTITY)|NETQTY)"
            r"\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(g|kg|ml|l|mg)",
            r"\b(\d+(?:\.\d+)?)\s*(g|kg|ml|l|mg)\b"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                return f"{match.group(1)} {match.group(2)}"

        return None

    def extract_phone(self, text):
        pattern = r"\b[6-9]\d{9}\b"

        match = re.search(pattern, text)

        if match:
            return match.group(0)

        return None

    def extract_email(self, text):
        pattern = (
            r"\b[A-Za-z0-9._%+-]+@"
            r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        )

        match = re.search(pattern, text)

        if match:
            return match.group(0)

        return None

    def extract_country(self, text):
        countries = [
            "Made in India",
            "Product of India",
            "India"
        ]

        for country in countries:
            if country.lower() in text.lower():
                return country

        return None

    def extract_all(self, text):
        return {
            "mrp": self.extract_mrp(text),
            "batch_number": self.extract_batch_number(text),
            "dates": self.extract_dates(text),
            "net_quantity": self.extract_net_quantity(text),
            "phone": self.extract_phone(text),
            "email": self.extract_email(text),
            "country": self.extract_country(text)
        }


if __name__ == "__main__":

    extractor = EntityExtractor()

    sample_text = """
    MRP Rs. 48/- (INCL. OF ALL TAXES)
    PER PACK/B.NO.: 2474972646
    21/01/27
    NET QTY: 80 g
    Made in India
    """

    result = extractor.extract_all(sample_text)

    print("\n==============================")
    print("       EXTRACTED FIELDS")
    print("==============================\n")

    for key, value in result.items():
        print(f"{key}: {value}")

