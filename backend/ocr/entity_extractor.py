"""Regex-based product-label entity extraction."""

from __future__ import annotations

import re

ENTITY_FIELDS = (
	"product_name", "mrp", "net_quantity", "manufacturer", "packer", "address",
	"country_of_origin", "customer_care_phone", "customer_care_email",
	"manufacturing_date", "packing_date", "best_before", "expiry_date",
)
MONTHS = {name: number for number, name in enumerate(
	("january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"), 1
)}


def _first(patterns: list[str], text: str) -> re.Match[str] | None:
	for pattern in patterns:
		match = re.search(pattern, text, re.IGNORECASE)
		if match:
			return match
	return None


def _date(value: str) -> str | None:
	value = re.sub(r"\s+", " ", value.strip())
	month = re.match(r"([A-Za-z]+)\s+(\d{4})$", value)
	if month:
		month_name = month.group(1).lower()
		number = next(
			(number for name, number in MONTHS.items() if name.startswith(month_name)),
			None,
		)
		return f"{number:02d}/{month.group(2)}" if number else None
	match = re.fullmatch(r"(\d{1,2})[/-](\d{4})", value)
	if match:
		return f"{int(match.group(1)):02d}/{match.group(2)}"
	match = re.fullmatch(r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})", value)
	if match:
		year = match.group(3)
		year = year if len(year) == 4 else "20" + year
		return f"{int(match.group(1)):02d}/{int(match.group(2)):02d}/{year}"
	return value or None


def _nearby_value(lines: list[str], labels: tuple[str, ...]) -> str | None:
	for index, line in enumerate(lines):
		for label in labels:
			match = re.search(rf"{label}\s*[:\-]?\s*(.*)$", line, re.IGNORECASE)
			if match:
				value = match.group(1).strip()
				return value or (lines[index + 1].strip() if index + 1 < len(lines) else None)
	return None


def extract_entities(text: str) -> dict[str, str | None]:
	"""Extract supported fields without guessing missing product information."""
	result = {field: None for field in ENTITY_FIELDS}
	text = text or ""
	lines = [line.strip() for line in text.splitlines() if line.strip()]

	match = _first([r"(?:MRP|MAXIMUM\s+RETAIL\s+PRICE)\s*[:\-]?\s*(?:Rs\.?|INR|₹)?\s*([\d,]+(?:\.\d+)?)"], text)
	if match:
		result["mrp"] = f"{match.group(1).replace(',', '')} INR"

	match = _first([r"(?:NET[_ ]QUANTITY|NET[_ ](?:QTY|WEIGHT|WT))\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(kg|mg|ml|g|l)\b", r"\b(\d+(?:\.\d+)?)\s*(kg|mg|ml|g|l)\b"], text)
	if match:
		result["net_quantity"] = f"{match.group(1)} {match.group(2).lower()}"

	match = re.search(r"(?:MADE\s+IN|COUNTRY[_ ]OF[_ ]ORIGIN|PRODUCT\s+OF)\s*[:\-]?\s*([A-Za-z]+)", text, re.IGNORECASE)
	if match:
		result["country_of_origin"] = match.group(1).title()

	for field, labels in {
		"manufacturer": (r"MANUFACTURED(?:\s*&\s*PACKED)?\s+BY", r"MFD?\.?\s*BY", r"MFG\.?\s*BY", r"MANUFACTURER"),
		"packer": (r"PACKED\s+BY", r"PACKER", r"MARKETED\s+BY"),
	}.items():
		value = _nearby_value(lines, labels)
		if value:
			result[field] = value

	email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
	if email:
		result["customer_care_email"] = email.group(0)
	phone = re.search(r"(?:\+91[ -]?)?[6-9]\d{9}\b|\b1800[ -]?\d{3}[ -]?\d{4}\b", text)
	if phone:
		result["customer_care_phone"] = phone.group(0)

	date_pattern = r"(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}[/-]\d{4}|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4})"
	for field, labels in {
		"manufacturing_date": r"(?:MFD|MFG|MANUFACTUR(?:ED|ING)\s+DATE)",
		"packing_date": r"(?:PACKING[_ ]DATE|PACKED|PKD)",
		"expiry_date": r"(?:EXPIRY|EXP|EXPIRES\s+ON|USE\s+BEFORE)",
	}.items():
		match = re.search(rf"{labels}\s*[:\-]?\s*({date_pattern})", text, re.IGNORECASE)
		if match:
			result[field] = _date(match.group(1))
	match = re.search(r"(?:BEST\s+BEFORE|CONSUME\s+WITHIN)\s*[:\-]?\s*(\d+\s*(?:months?|days?|years?))", text, re.IGNORECASE)
	if match:
		result["best_before"] = re.sub(r"\s+", " ", match.group(1).lower())

	address = _nearby_value(lines, (r"ADDRESS",))
	if address:
		result["address"] = address

	excluded = re.compile(r"MRP|NET[_ ]|PACK|MADE IN|COUNTRY|PRODUCT OF|MANUFACTUR|MARKET|ADDRESS|\d{5,}|@", re.IGNORECASE)
	for line in lines:
		if not excluded.search(line):
			result["product_name"] = line
			break
	return result


class EntityExtractor:
	"""Backwards-compatible wrapper around :func:`extract_entities`."""

	def extract_all(self, text: str) -> dict[str, str | None]:
		return extract_entities(text)
