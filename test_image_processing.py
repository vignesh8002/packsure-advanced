"""Automated tests for the Member 2 quality and enhancement pipeline."""

import unittest

import cv2
import numpy as np

from image_processing.image_processor import process_image
from image_processing.quality_checker import check_image_quality


def make_test_image(width=1200, height=900, brightness=220):
    image = np.full((height, width, 3), brightness, dtype=np.uint8)
    for index, text in enumerate(("PRODUCT LABEL", "MRP 120", "NET WT 500 g")):
        cv2.putText(
            image,
            text,
            (60, 180 + index * 180),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (20, 20, 20),
            4,
        )
    return image


class ImageProcessingTests(unittest.TestCase):
    def assert_processed(self, image):
        report = check_image_quality(image)
        processed = process_image(image)

        self.assertIn(report["blur"], {"HIGH", "MEDIUM", "LOW"})
        self.assertIn(report["brightness"], {"DARK", "GOOD", "TOO_BRIGHT"})
        self.assertGreaterEqual(report["quality_score"], 0)
        self.assertLessEqual(report["quality_score"], 100)
        self.assertEqual(processed.ndim, 3)
        self.assertEqual(processed.shape[2], 3)
        self.assertGreaterEqual(processed.shape[1], 640)

    def test_clear_image(self):
        report = check_image_quality(make_test_image())
        self.assertEqual(report["brightness"], "TOO_BRIGHT")
        self.assert_processed(make_test_image(brightness=130))

    def test_blurry_image(self):
        image = cv2.GaussianBlur(make_test_image(brightness=130), (31, 31), 12)
        report = check_image_quality(image)
        self.assertEqual(report["blur"], "HIGH")
        self.assert_processed(image)

    def test_dark_image(self):
        image = make_test_image(brightness=35)
        report = check_image_quality(image)
        self.assertEqual(report["brightness"], "DARK")
        self.assert_processed(image)

    def test_bright_image(self):
        image = make_test_image(brightness=245)
        report = check_image_quality(image)
        self.assertEqual(report["brightness"], "TOO_BRIGHT")
        self.assert_processed(image)

    def test_rotated_image(self):
        image = make_test_image(brightness=130)
        center = (image.shape[1] // 2, image.shape[0] // 2)
        matrix = cv2.getRotationMatrix2D(center, 8, 1.0)
        rotated = cv2.warpAffine(image, matrix, (image.shape[1], image.shape[0]))
        self.assert_processed(rotated)

    def test_noisy_image(self):
        image = make_test_image(brightness=130)
        noise = np.random.default_rng(7).normal(0, 18, image.shape)
        noisy = np.clip(image.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        self.assert_processed(noisy)

    def test_low_resolution_image(self):
        image = make_test_image(width=320, height=240, brightness=130)
        report = check_image_quality(image)
        self.assertEqual(report["resolution"], "LOW")
        self.assert_processed(image)

    def test_invalid_image_is_reported_cleanly(self):
        with self.assertRaises(ValueError):
            check_image_quality(np.empty((0, 0, 3), dtype=np.uint8))
        with self.assertRaises(ValueError):
            process_image(None)


if __name__ == "__main__":
    unittest.main()