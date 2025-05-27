"""
cloupe_image_stitcher

A package to extract and stitch spatial transcriptomics images from 10x Genomics .cloupe files.
"""

from .stitch_cloupe_image import stitch_cloupe_image

__all__ = ["stitch_cloupe_image"]
