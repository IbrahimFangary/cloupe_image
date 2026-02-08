# cloupe_image

High-resolution microscope images (e.g., 20,000 × 20,000 pixels), which are much larger than the `tissue_hires_image.png`, are often not readily available as a single file. Instead, these images are usually stored inside the 10X Genomics `.cloupe` file as multiple smaller tiles (chunks) at various resolutions.

This package implements a **multi-resolution tile pyramid reconstruction** method to recover high-resolution microscope images stored inside 10x Genomics `.cloupe` files. Large histology images (e.g., 20,000 × 20,000 pixels) are not stored as single files, but rather as collections of smaller image tiles at multiple resolution levels, similar to the approach used in platforms like Google Maps. The package extracts these tiles, reconstructs their spatial arrangement, and stitches them together to generate the full high-resolution image, enabling direct access to image data that is otherwise unavailable as a standalone file.

## Installation

```bash
pip install git+https://github.com/IbrahimFangary/cloupe_image.git
```

## how to use 
```python
import Cloupe_image

Cloupe_image.stitch_cloupe_image('your_cloupe_file.cloupe')
```

The output includes a very high-resolution image (stitched_highres.tiff) and a downsampled version (stitched_downsampled.tiff) for easier visualization.

### Display the downsampled image:
```python
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('stitched_downsampled.tiff')
plt.imshow(img)
plt.axis('off')
plt.show()
```



### Thanks to [cellgeni/cloupe](https://github.com/cellgeni/cloupe.git) for inspiration and concepts used in this project.
some of the concepts used in this package are from cellgeni/cloupe, such as opening a Cloupe file in Python and iterating through its content 
