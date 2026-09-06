"""
quality_checker.py
------------------
PACKSURE AI - Member 2 (Computer Vision & Image Processing)

Analyzes a RAW input image (before enhancement) and reports:
    - blur / sharpness
    - brightness
    - resolution
    - an overall 0-100 quality score

This module never raises on a "bad" image - it always returns a
report so the rest of the pipeline (OCR + compliance engine) can
decide whether to mark a result as PASS / FAIL / UNCERTAIN.
"""

import cv2
import numpy as np


# --------------------------------------------------------------------------
# Thresholds (tuned for hackathon MVP - "reliable enough" over "perfect")
# --------------------------------------------------------------------------

BLUR_HIGH_THRESHOLD = 50      # score < 50  -> HIGH BLUR
BLUR_MEDIUM_THRESHOLD = 100   # 50-100      -> MEDIUM BLUR
                              # > 100       -> LOW BLUR / SHARP

BRIGHTNESS_DARK_THRESHOLD = 60     # < 60      -> DARK
BRIGHTNESS_BRIGHT_THRESHOLD = 180  # 60-180    -> GOOD, > 180 -> TOO BRIGHT

MIN_GOOD_WIDTH = 640  # width < 640 -> LOW RESOLUTION

# Quality score weights
SHARPNESS_WEIGHT = 0.5
BRIGHTNESS_WEIGHT = 0.3
RESOLUTION_WEIGHT = 0.2

# Caps used to normalize raw scores into a 0-100 sub-score before weighting.
# (Laplacian variance and pixel brightness are on different scales, so we
# clamp/normalize each into 0-100 before combining.)
SHARPNESS_NORMALIZATION_CAP = 300.0  # variance >= this -> treated as 100
BRIGHTNESS_IDEAL_CENTER = 120.0      # "perfect" brightness for scoring


# --------------------------------------------------------------------------
# FEATURE 1 - BLUR DETECTION (Variance of Laplacian)
# --------------------------------------------------------------------------

def calculate_blur_score(image):
    """
    Sharp image -> more edges -> higher Laplacian variance -> higher score.
    Blurry image -> fewer strong edges -> lower Laplacian variance.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    score = cv2.Laplacian(gray, cv2.CV_64F).var()
    return float(score)


def classify_blur(blur_score):
    if blur_score < BLUR_HIGH_THRESHOLD:
        return "HIGH"
    elif blur_score < BLUR_MEDIUM_THRESHOLD:
        return "MEDIUM"
    else:
        return "LOW"


# --------------------------------------------------------------------------
# FEATURE 2 - BRIGHTNESS DETECTION
# --------------------------------------------------------------------------

def calculate_brightness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = gray.mean()
    return float(brightness)


def classify_brightness(brightness_score):
    if brightness_score < BRIGHTNESS_DARK_THRESHOLD:
        return "DARK"
    elif brightness_score <= BRIGHTNESS_BRIGHT_THRESHOLD:
        return "GOOD"
    else:
        return "TOO_BRIGHT"


# --------------------------------------------------------------------------
# FEATURE 3 - RESOLUTION CHECK
# --------------------------------------------------------------------------

def check_resolution(image):
    height, width = image.shape[:2]
    resolution_status = "GOOD" if width >= MIN_GOOD_WIDTH else "LOW"
    return {
        "width": int(width),
        "height": int(height),
        "resolution": resolution_status,
    }


# --------------------------------------------------------------------------
# FEATURE 4 - OVERALL QUALITY SCORE (0-100)
# --------------------------------------------------------------------------

def _sharpness_sub_score(blur_score):
    """Normalize Laplacian variance into a 0-100 sub-score."""
    normalized = (blur_score / SHARPNESS_NORMALIZATION_CAP) * 100.0
    return float(np.clip(normalized, 0.0, 100.0))


def _brightness_sub_score(brightness_score):
    """
    Normalize brightness into a 0-100 sub-score.
    Score is highest near the ideal center and falls off toward
    extremes (too dark or too bright).
    """
    distance_from_ideal = abs(brightness_score - BRIGHTNESS_IDEAL_CENTER)
    # Max possible distance is roughly BRIGHTNESS_IDEAL_CENTER (toward 0)
    # or (255 - BRIGHTNESS_IDEAL_CENTER) toward the bright end.
    max_distance = max(BRIGHTNESS_IDEAL_CENTER, 255.0 - BRIGHTNESS_IDEAL_CENTER)
    normalized = 100.0 - (distance_from_ideal / max_distance) * 100.0
    return float(np.clip(normalized, 0.0, 100.0))


def _resolution_sub_score(width):
    """Normalize resolution into a 0-100 sub-score."""
    if width >= MIN_GOOD_WIDTH:
        return 100.0
    return float(np.clip((width / MIN_GOOD_WIDTH) * 100.0, 0.0, 100.0))


def calculate_quality_score(blur_score, brightness_score, width):
    sharpness_sub = _sharpness_sub_score(blur_score)
    brightness_sub = _brightness_sub_score(brightness_score)
    resolution_sub = _resolution_sub_score(width)

    quality_score = (
        sharpness_sub * SHARPNESS_WEIGHT
        + brightness_sub * BRIGHTNESS_WEIGHT
        + resolution_sub * RESOLUTION_WEIGHT
    )
    return round(float(np.clip(quality_score, 0.0, 100.0)), 1)


def classify_quality(quality_score):
    if quality_score >= 80:
        return "EXCELLENT"
    elif quality_score >= 60:
        return "ACCEPTABLE"
    elif quality_score >= 40:
        return "POOR"
    else:
        return "VERY_POOR"


# --------------------------------------------------------------------------
# MAIN ENTRY POINT
# --------------------------------------------------------------------------

def check_image_quality(image):
    """
    Analyze the ORIGINAL (pre-processing) image.

    Args:
        image: OpenCV image (BGR numpy array), e.g. from cv2.imread()
               or decoded from an uploaded file.

    Returns:
        dict, e.g.:
        {
            "quality_score": 82,
            "quality_rating": "EXCELLENT",
            "blur_score": 145.2,
            "blur": "LOW",
            "brightness_score": 130.4,
            "brightness": "GOOD",
            "width": 1920,
            "height": 1080,
            "resolution": "GOOD"
        }

    This function never raises for a "bad" image - a poor image
    just produces a low quality_score. Only structurally invalid
    input (None / empty array) raises ValueError so the caller can
    return a clean HTTP 400 instead of a crash deep in OpenCV.
    """
    if (
        image is None
        or not hasattr(image, "shape")
        or image.ndim != 3
        or image.shape[2] != 3
        or image.size == 0
    ):
        raise ValueError("check_image_quality: received an invalid/empty image")

    blur_score = calculate_blur_score(image)
    blur_status = classify_blur(blur_score)

    brightness_score = calculate_brightness(image)
    brightness_status = classify_brightness(brightness_score)

    resolution_info = check_resolution(image)

    quality_score = calculate_quality_score(
        blur_score, brightness_score, resolution_info["width"]
    )
    quality_rating = classify_quality(quality_score)

    return {
        "quality_score": quality_score,
        "quality_rating": quality_rating,
        "low_confidence": quality_score < 60,
        "blur_score": round(blur_score, 1),
        "blur": blur_status,
        "brightness_score": round(brightness_score, 1),
        "brightness": brightness_status,
        "width": resolution_info["width"],
        "height": resolution_info["height"],
        "resolution": resolution_info["resolution"],
    }


if __name__ == "__main__":
    # Quick manual smoke test:
    #   python quality_checker.py path/to/image.jpg
    import sys

    if len(sys.argv) < 2:
        print("Usage: python quality_checker.py <image_path>")
        sys.exit(1)

    img = cv2.imread(sys.argv[1])
    if img is None:
        print(f"Could not read image: {sys.argv[1]}")
        sys.exit(1)

    result = check_image_quality(img)
    print(result)
