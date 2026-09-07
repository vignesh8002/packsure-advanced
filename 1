from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime
import json


# ============================================================
# LEGAL METROLOGY COMPLIANCE RULE ENGINE
# SIH Problem Statement: 26034
# ============================================================

@dataclass
class RuleResult:
    rule_no: str
    requirement: str
    status: str
    observation: str
    severity: str


class LegalMetrologyRuleEngine:

    def __init__(self):
        # Core declarations checked by the prototype.
        # Keep these in a separate configuration/database so
        # amended government rules can be updated without
        # changing application logic.

        self.required_declarations = {

            "product_name": {
                "rule": "Rule 6",
                "name": "Name / generic name of commodity"
            },

            "manufacturer": {
                "rule": "Rule 6 / Rule 10",
                "name": "Manufacturer / Packer / Importer details"
            },

            # =================================================
            # ADDED: DATE OF MANUFACTURE
            # =================================================
            "date_of_manufacture": {
                "rule": "Rule 6",
                "name": "Month and year of manufacture"
            },

            # =================================================
            # ADDED: BEST BEFORE / EXPIRY / USE BY
            # =================================================
            "best_before": {
                "rule": "Rule 6",
                "name": "Best before / Expiry / Use by date"
            },

            "net_quantity": {
                "rule": "Rule 6 / Rule 11",
                "name": "Net quantity"
            },

            "mrp": {
                "rule": "Rule 6",
                "name": "Maximum Retail Price (MRP)"
            },

            "consumer_care": {
                "rule": "Rule 6",
                "name": "Consumer care details"
            },

            "country_of_origin": {
                "rule": "Rule 6",
                "name": "Country of origin, where applicable"
            }
        }

    # --------------------------------------------------------
    # Utility
    # --------------------------------------------------------

    def is_present(self, value):

        if value is None:
            return False

        if isinstance(value, str):
            return bool(value.strip())

        return True

    # --------------------------------------------------------
    # Rule 6 - Mandatory declarations
    # --------------------------------------------------------

    def check_mandatory_declarations(self, product: Dict):

        results = []

        for field, info in self.required_declarations.items():

            # =================================================
            # Country of origin is conditional
            # =================================================

            if field == "country_of_origin":

                if product.get("is_imported", False):
                    required = True
                else:
                    required = False

            # =================================================
            # Best before / expiry is conditional
            # =================================================

            elif field == "best_before":

                if product.get("requires_best_before", False):
                    required = True
                else:
                    required = False

            else:
                required = True

            # ------------------------------------------------
            # Not applicable
            # ------------------------------------------------

            if not required:

                results.append(
                    RuleResult(
                        info["rule"],
                        info["name"],
                        "N/A",
                        "Not applicable for this product.",
                        "LOW"
                    )
                )

                continue

            # ------------------------------------------------
            # Declaration present
            # ------------------------------------------------

            if self.is_present(product.get(field)):

                results.append(
                    RuleResult(
                        info["rule"],
                        info["name"],
                        "PASS",
                        f"{info['name']} detected.",
                        "NONE"
                    )
                )

            # ------------------------------------------------
            # Declaration missing
            # ------------------------------------------------

            else:

                results.append(
                    RuleResult(
                        info["rule"],
                        info["name"],
                        "FAIL",
                        f"Mandatory declaration missing: "
                        f"{info['name']}.",
                        "HIGH"
                    )
                )

        return results

    # --------------------------------------------------------
    # MRP validation
    # --------------------------------------------------------

    def check_mrp(self, product: Dict):

        mrp = product.get("mrp")

        selling_price = product.get("selling_price")

        if mrp is None:

            return RuleResult(
                "Rule 6",
                "Maximum Retail Price",
                "FAIL",
                "MRP not detected.",
                "HIGH"
            )

        if selling_price is not None:

            try:

                mrp = float(mrp)

                selling_price = float(
                    selling_price
                )

                if selling_price > mrp:

                    return RuleResult(
                        "Rule 18",
                        "Selling price",
                        "FAIL",
                        f"Selling price ₹{selling_price:.2f} "
                        f"exceeds declared MRP ₹{mrp:.2f}.",
                        "HIGH"
                    )

            except ValueError:
                pass

        return RuleResult(
            "Rule 6",
            "Maximum Retail Price",
            "PASS",
            f"Declared MRP: ₹{mrp}",
            "NONE"
        )

    # --------------------------------------------------------
    # Net quantity validation
    # --------------------------------------------------------

    def check_net_quantity(self, product: Dict):

        quantity = product.get(
            "net_quantity"
        )

        if not self.is_present(quantity):

            return RuleResult(
                "Rule 6 / Rule 11",
                "Net quantity",
                "FAIL",
                "Net quantity declaration is missing.",
                "HIGH"
            )

        unit = product.get(
            "quantity_unit"
        )

        allowed_units = [
            "g",
            "kg",
            "ml",
            "l",
            "m",
            "cm",
            "mm",
            "number",
            "nos"
        ]

        if unit:

            normalized = unit.lower().strip()

            if normalized not in allowed_units:

                return RuleResult(
                    "Rule 11",
                    "Net quantity",
                    "FAIL",
                    f"Unrecognized quantity unit: {unit}",
                    "MEDIUM"
                )

        return RuleResult(
            "Rule 6 / Rule 11",
            "Net quantity",
            "PASS",
            f"Net quantity detected: "
            f"{quantity} {unit or ''}".strip(),
            "NONE"
        )

    # --------------------------------------------------------
    # Readability / font check
    # --------------------------------------------------------

    def check_readability(self, product: Dict):

        readable = product.get(
            "readable",
            True
        )

        if readable:

            return RuleResult(
                "Rule 7 / Rule 9",
                "Readability and declaration visibility",
                "PASS",
                "Declaration appears readable based on "
                "image analysis.",
                "NONE"
            )

        return RuleResult(
            "Rule 7 / Rule 9",
            "Readability and declaration visibility",
            "FAIL",
            "Declaration may not satisfy readability/"
            "visibility requirements.",
            "MEDIUM"
        )

    # --------------------------------------------------------
    # Principal Display Panel
    # --------------------------------------------------------

    def check_pdp(self, product: Dict):

        pdp_visible = product.get(
            "pdp_visible",
            True
        )

        if pdp_visible:

            return RuleResult(
                "Rule 8",
                "Principal Display Panel",
                "PASS",
                "Required declaration area detected "
                "on package.",
                "NONE"
            )

        return RuleResult(
            "Rule 8",
            "Principal Display Panel",
            "FAIL",
            "Required declaration could not be verified "
            "on the principal display panel.",
            "MEDIUM"
        )

    # --------------------------------------------------------
    # Unit Sale Price
    # --------------------------------------------------------

    def check_unit_sale_price(self, product: Dict):

        unit_sale_price = product.get(
            "unit_sale_price"
        )

        if self.is_present(unit_sale_price):

            return RuleResult(
                "Rule 6",
                "Unit Sale Price",
                "PASS",
                f"Unit sale price detected: "
                f"{unit_sale_price}",
                "NONE"
            )

        return RuleResult(
            "Rule 6",
            "Unit Sale Price",
            "REVIEW",
            "Unit sale price could not be detected. "
            "Applicability depends on the product/category "
            "and current Rules.",
            "MEDIUM"
        )

    # --------------------------------------------------------
    # Complete compliance check
    # --------------------------------------------------------

    def check_product(self, product: Dict):

        results = []

        results.extend(
            self.check_mandatory_declarations(
                product
            )
        )

        results.append(
            self.check_mrp(
                product
            )
        )

        results.append(
            self.check_net_quantity(
                product
            )
        )

        results.append(
            self.check_readability(
                product
            )
        )

        results.append(
            self.check_pdp(
                product
            )
        )

        results.append(
            self.check_unit_sale_price(
                product
            )
        )

        return results

    # --------------------------------------------------------
    # Overall result
    # --------------------------------------------------------

    def calculate_summary(self, results):

        passed = sum(
            1
            for r in results
            if r.status == "PASS"
        )

        failed = sum(
            1
            for r in results
            
            if r.status == "FAIL"
        )

        review = sum(
            1
            for r in results
            if r.status == "REVIEW"
        )

        applicable = (
            passed +
            failed +
            review
        )

        if applicable:

            score = round(
                (passed / applicable) * 100,
                2
            )

        else:

            score = 0

        if failed > 0:

            overall = "NON-COMPLIANT"

        elif review > 0:

            overall = "REVIEW REQUIRED"

        else:

            overall = "COMPLIANT"

        return {
            "passed": passed,
            "failed": failed,
            "review": review,
            "score": score,
            "overall": overall
        }


# ============================================================
# PDF REPORT
# ============================================================

def generate_pdf_report(
        product: Dict,
        results: List[RuleResult],
        summary: Dict,
        filename="compliance_report.pdf"
):

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle
    )

    document = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    story = []

    # --------------------------------------------------------
    # Title
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "PACKAGED COMMODITY COMPLIANCE REPORT",
            styles["Title"]
        )
    )

    story.append(
        Spacer(
            1,
            10
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated:</b> "
            f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(
            1,
            15
        )
    )

    # ========================================================
    # Product information
    # ========================================================

    product_data = [

        [
            "Product",
            product.get(
                "product_name",
                "Not detected"
            )
        ],

        [
            "Manufacturer",
            product.get(
                "manufacturer",
                "Not detected"
            )
        ],

        # ====================================================
        # ADDED TO PDF
        # ====================================================

        [
            "Date of Manufacture",
            product.get(
                "date_of_manufacture",
                "Not detected"
            )
        ],

        [
            "Best Before / Expiry / Use By",
            product.get(
                "best_before",
                "N/A"
            )
        ],

        [
            "Net Quantity",
            f"{product.get('net_quantity', 'N/A')} "
            f"{product.get('quantity_unit', '')}"
        ],

        [
            "MRP",
            f"₹{product.get('mrp', 'N/A')}"
        ],

        [
            "Country",
            product.get(
                "country_of_origin",
                "N/A"
            )
        ],

        [
            "Consumer Care",
            product.get(
                "consumer_care",
                "N/A"
            )
        ]
    ]

    table = Table(
        product_data,
        colWidths=[
            150,
            350
        ]
    )

    table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(
        table
    )

    story.append(
        Spacer(
            1,
            20
        )
    )

    # ========================================================
    # Summary
    # ========================================================

    story.append(
        Paragraph(
            f"<b>Overall Status:</b> "
            f"{summary['overall']}",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Compliance Score: "
            f"{summary['score']}%",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Passed: {summary['passed']} | "
            f"Failed: {summary['failed']} | "
            f"Review: {summary['review']}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(
            1,
            20
        )
    )

    # ========================================================
    # Rule results
    # ========================================================

    story.append(
        Paragraph(
            "Rule-by-Rule Assessment",
            styles["Heading2"]
        )
    )

    result_data = [

        [
            "Rule",
            "Requirement",
            "Status",
            "Observation"
        ]
    ]

    for result in results:

        result_data.append([

            result.rule_no,

            result.requirement,

            result.status,

            result.observation
        ])

    result_table = Table(
        result_data,
        colWidths=[
            70,
            120,
            70,
            240
        ],
        repeatRows=1
    )

    result_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                5
            )
        ])
    )

    story.append(
        result_table
    )

    story.append(
        Spacer(
            1,
            20
        )
    )

    # ========================================================
    # Legal note
    # ========================================================

    story.append(
        Paragraph(
            "<b>Important:</b> This automated assessment is "
            "intended as a screening and decision-support tool. "
            "Final legal determination should be made by the "
            "competent enforcement authority after verification "
            "of the package and applicable law/amendments.",
            styles["Normal"]
        )
    )

    document.build(
        story
    )


# ============================================================
# DEMO PRODUCT
# ============================================================

if __name__ == "__main__":

    with open("scanned_product.json",
    "r", encoding="utf-8") as file:
        scanned_product = json.load(file)


    # ========================================================
    # CREATE ENGINE
    # ========================================================

    engine = LegalMetrologyRuleEngine()

    # ========================================================
    # CHECK PRODUCT
    # ========================================================

    results = engine.check_product(
        scanned_product
    )

    # ========================================================
    # CALCULATE SUMMARY
    # ========================================================

    summary = engine.calculate_summary(
        results
    )

    # ========================================================
    # PRINT RESULT
    # ========================================================

    print(
        "\n===================================="
    )

    print(
        "LEGAL METROLOGY COMPLIANCE RESULT"
    )

    print(
        "===================================="
    )

    print(
        f"Product: "
        f"{scanned_product['product_name']}"
    )

    print(
        f"Status: "
        f"{summary['overall']}"
    )

    print(
        f"Score: "
        f"{summary['score']}%"
    )

    print(
        f"Passed: "
        f"{summary['passed']}"
    )

    print(
        f"Failed: "
        f"{summary['failed']}"
    )

    print(
        f"Review: "
        f"{summary['review']}"
    )

    print(
        "\nRULE RESULTS:"
    )

    for result in results:

        print(
            f"[{result.status}] "
            f"{result.rule_no} - "
            f"{result.requirement}: "
            f"{result.observation}"
        )

    # ========================================================
    # GENERATE PDF
    # ========================================================

    generate_pdf_report(

        scanned_product,

        results,

        summary,

        "compliance_report.pdf"
    )

    print(
        "\nPDF generated: compliance_report.pdf"
    )