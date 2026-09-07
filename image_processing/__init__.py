"""
image_processing package
-------------------------
PACKSURE AI - Member 2 (Computer Vision) deliverable.

Exposes the two main entry points other team members need:

    from image_processing.quality_checker import check_image_quality
    from image_processing.image_processor import process_image
"""

from .quality_checker import check_image_quality
from .image_processor import process_image

__all__ = ["check_image_quality", "process_image"]
