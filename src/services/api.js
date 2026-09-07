const USE_MOCK_API = true;

export async function scanProduct(image) {
  if (USE_MOCK_API) {
    return {
      overall_score: 82,
      status: "PASS",
      checks: [
        {
          name: "Product Name",
          status: "PASS",
          message: "Product name is clearly mentioned.",
        },
        {
          name: "Net Quantity",
          status: "PASS",
          message: "Net quantity is available.",
        },
        {
          name: "Country of Origin",
          status: "FAIL",
          message: "Country of origin is missing.",
        },
        {
          name: "Packing Date",
          status: "UNCERTAIN",
          message: "Packing date could not be clearly identified.",
        },
      ],
    };
  }
}