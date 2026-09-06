"""
image_processor.py
-------------------
PACKSURE AI - Member 2 (Computer Vision & Image Processing)

Takes a raw product-label image and enhances it so OCR (Member 3)
has the best possible chance of reading the label correctly.

Pipeline:
    Input Image
      -> Resize
      -> Denoise
      -> CLAHE Contrast Enhancement
      -> Deskew
      -> Perspective Correction (bonus, best-effort)
      -> Enhanced Image
"""

import cv2
import numpy as np


# --------------------------------------------------------------------------
# STEP 1 - RESIZE
# --------------------------------------------------------------------------

MAX_WIDTH = 1600
MIN_WIDTH = 640
DEFAULT_TARGET_WIDTH = 1280


def resize_image(image, target_width=DEFAULT_TARGET_WIDTH):
    """
    Resize while preserving aspect ratio. Never stretches the image.

    - If the image is already within [MIN_WIDTH, MAX_WIDTH], leave it
      close to its own size (only resample toward target_width when
      it's meaningfully different, to avoid needless quality loss).
    - Small images are upscaled toward target_width.
    - Very large images are downscaled toward target_width.
    """
    height, width = image.shape[:2]

    if width == target_width:
        return image

    # Clamp target within the recommended min/max bounds.
    effective_target = int(np.clip(target_width, MIN_WIDTH, MAX_WIDTH))

    ratio = effective_target / width
    new_height = int(height * ratio)

    interpolation = cv2.INTER_CUBIC if ratio > 1 else cv2.INTER_AREA
    resized = cv2.resize(
        image,
        (effective_target, new_height),
        interpolation=interpolation,
    )
    return resized


# --------------------------------------------------------------------------
# STEP 2 - DENOISING
# --------------------------------------------------------------------------

def denoise_image(image):
    """
    Remove camera/sensor noise while trying not to wipe out small text.
    Uses moderate strength (h=10) per the recommended defaults.
    """
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)


# --------------------------------------------------------------------------
# STEP 3 - CLAHE CONTRAST ENHANCEMENT
# --------------------------------------------------------------------------

def enhance_contrast(image):
    """
    Apply CLAHE on the L channel (LAB color space) to fix shadows,
    glossy glare, and uneven lighting common on product packaging.
    """
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_l = clahe.apply(l)

    merged = cv2.merge((enhanced_l, a, b))
    result = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
    return result


# --------------------------------------------------------------------------
# STEP 4 - ROTATION / DESKEW
# --------------------------------------------------------------------------

MIN_SKEW_ANGLE_TO_CORRECT = 2.0  # degrees - ignore tiny/no skew


def _detect_skew_angle(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold to isolate dark text/marks on a lighter background.
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    coords = cv2.findNonZero(thresh)

    if coords is None:
        return 0.0

    angle = cv2.minAreaRect(coords)[-1]

    # cv2.minAreaRect angle convention correction
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    return float(angle)


def deskew_image(image):
    """
    Detect and correct small rotations so text lines are horizontal.
    Skips correction entirely if the detected angle is negligible,
    or if correction would clearly be spurious (e.g. blank image).
    """
    angle = _detect_skew_angle(image)

    if abs(angle) < MIN_SKEW_ANGLE_TO_CORRECT:
        return image

    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image,
        matrix,
        (width, height),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )
    return rotated


# --------------------------------------------------------------------------
# STEP 5 - PERSPECTIVE CORRECTION (BONUS - best effort, never blocks pipeline)
# --------------------------------------------------------------------------

def correct_perspective(image):
    """
    Best-effort perspective correction: tries to find the largest
    quadrilateral contour (assumed to be the label) and warps it to
    a flat rectangle. If no confident quadrilateral is found, the
    original image is returned unchanged - this is a bonus feature
    and must never break the main pipeline.
    """
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)

        contours, _ = cv2.findContours(
            edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )
        if not contours:
            return image

        image_area = image.shape[0] * image.shape[1]
        largest_quad = None
        largest_area = 0

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            if len(approx) == 4:
                area = cv2.contourArea(approx)
                # Require the quad to be a meaningful chunk of the frame
                # (avoids grabbing tiny noise contours) but not the
                # entire frame border itself.
                if area > 0.25 * image_area and area > largest_area:
                    largest_area = area
                    largest_quad = approx

        if largest_quad is None:
            return image

        pts = largest_quad.reshape(4, 2).astype("float32")
        rect = _order_quad_points(pts)
        (tl, tr, br, bl) = rect

        width_top = np.linalg.norm(tr - tl)
        width_bottom = np.linalg.norm(br - bl)
        max_width = int(max(width_top, width_bottom))

        height_left = np.linalg.norm(bl - tl)
        height_right = np.linalg.norm(br - tr)
        max_height = int(max(height_left, height_right))

        if max_width <= 0 or max_height <= 0:
            return image

        destination = np.array(
            [
                [0, 0],
                [max_width - 1, 0],
                [max_width - 1, max_height - 1],
                [0, max_height - 1],
            ],
            dtype="float32",
        )

        matrix = cv2.getPerspectiveTransform(rect, destination)
        warped = cv2.warpPerspective(image, matrix, (max_width, max_height))
        return warped

    except Exception:
        # Bonus feature - never let it take down the main pipeline.
        return image


def _order_quad_points(pts):
    """Order 4 points as top-left, top-right, bottom-right, bottom-left."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)

    rect[0] = pts[np.argmin(s)]       # top-left (smallest sum)
    rect[2] = pts[np.argmax(s)]       # bottom-right (largest sum)
    rect[1] = pts[np.argmin(diff)]    # top-right (smallest difference)
    rect[3] = pts[np.argmax(diff)]    # bottom-left (largest difference)
    return rect


# --------------------------------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------------------------------

def process_image(image, apply_perspective_correction=False):
    """
    Run the full enhancement pipeline on a raw product image.

    Args:
        image: OpenCV image (BGR numpy array).
        apply_perspective_correction: off by default since it's a
            bonus/experimental step; flip to True once validated on
            real test images.

    Returns:
        Enhanced OpenCV image (BGR numpy array). Never raises for a
        poor-quality image - worst case, later steps are skipped and
        the least-processed valid image is returned.
    """
    if (
        image is None
        or not hasattr(image, "shape")
        or image.ndim != 3
        or image.shape[2] != 3
        or image.size == 0
    ):
        raise ValueError("process_image: received an invalid/empty image")

    working_image = image

    try:
        working_image = resize_image(working_image)
    except Exception:
        pass

    try:
        working_image = denoise_image(working_image)
    except Exception:
        pass

    try:
        working_image = enhance_contrast(working_image)
    except Exception:
        pass

    try:
        working_image = deskew_image(working_image)
    except Exception:
        pass

    if apply_perspective_correction:
        working_image = correct_perspective(working_image)

    return working_image


if __name__ == "__main__":
    # Quick manual smoke test:
    #   python image_processor.py path/to/image.jpg path/to/output.jpg
    import sys

    if len(sys.argv) < 3:
        print("Usage: python image_processor.py <input_path> <output_path>")
        sys.exit(1)

    img = cv2.imread(sys.argv[1])
    if img is None:
        print(f"Could not read image: {sys.argv[1]}")
        sys.exit(1)

    processed = process_image(img)
    cv2.imwrite(sys.argv[2], processed)
    print(f"Saved processed image to {sys.argv[2]}")
