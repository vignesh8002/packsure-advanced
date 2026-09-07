import { useState, useEffect } from "react";

function ImageUpload({ onImagesChange }) {
  const [images, setImages] = useState([]);

  const MAX_PRODUCTS = 10;

  useEffect(() => {
    if (onImagesChange) {
      onImagesChange(images);
    }
  }, [images, onImagesChange]);

  const handleImageChange = (event) => {
    const files = Array.from(event.target.files);

    if (files.length === 0) return;

    if (images.length + files.length > MAX_PRODUCTS) {
      alert("You can upload maximum 10 products.");
      event.target.value = "";
      return;
    }

    const allowedTypes = [
      "image/jpeg",
      "image/png",
    ];

    for (const file of files) {
      if (!allowedTypes.includes(file.type)) {
        alert("Please upload only JPG or PNG images.");
        event.target.value = "";
        return;
      }

      if (file.size > 10 * 1024 * 1024) {
        alert("Each image must be less than 10 MB.");
        event.target.value = "";
        return;
      }
    }

    const newImages = files.map((file) => ({
      file: file,
      preview: URL.createObjectURL(file),
    }));

    setImages((currentImages) => [
      ...currentImages,
      ...newImages,
    ]);

    event.target.value = "";
  };

  const deleteImage = (index) => {
    URL.revokeObjectURL(images[index].preview);

    setImages((currentImages) =>
      currentImages.filter((_, i) => i !== index)
    );
  };

  const clearAll = () => {
    images.forEach((image) => {
      URL.revokeObjectURL(image.preview);
    });

    setImages([]);
  };

  return (
    <div style={{ textAlign: "center" }}>

      <h2>🖼️ Upload Product Images</h2>

      <p>
        Upload 1 to 10 different product images.
      </p>

      <h3 style={{ color: "#2563eb" }}>
        Products Uploaded: {images.length} / {MAX_PRODUCTS}
      </h3>

      {images.length < MAX_PRODUCTS && (
        <input
          type="file"
          accept="image/jpeg,image/png"
          multiple
          onChange={handleImageChange}
        />
      )}

      {images.length > 0 && (
        <div>

          <h3>📦 Uploaded Products</h3>

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(150px, 1fr))",
              gap: "15px",
            }}
          >

            {images.map((image, index) => (
              <div
                key={index}
                style={{
                  border: "1px solid #ddd",
                  padding: "10px",
                  borderRadius: "12px",
                  background: "#ffffff",
                }}
              >

                <strong>
                  Product {index + 1}
                </strong>

                <img
                  src={image.preview}
                  alt={`Product ${index + 1}`}
                  style={{
                    width: "100%",
                    marginTop: "8px",
                    borderRadius: "8px",
                  }}
                />

                <button
                  onClick={() => deleteImage(index)}
                  style={{
                    background: "#dc2626",
                    marginTop: "8px",
                  }}
                >
                  🗑️ Delete
                </button>

              </div>
            ))}

          </div>

          <br />

          <button
            onClick={clearAll}
            style={{
              background: "#64748b",
            }}
          >
            🗑️ Clear All
          </button>

        </div>
      )}

    </div>
  );
}

export default ImageUpload;