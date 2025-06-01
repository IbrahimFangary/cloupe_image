# cloupe_image

High-resolution microscope images (e.g., 20,000 × 20,000 pixels), which are much larger than the `tissue_hires_image.png`, are often not readily available as a single file. Instead, these images are usually stored inside the `.cloupe` file as multiple smaller tiles (chunks) at various resolutions.

This package is used for opening a `.cloupe` file, extracting these image tiles, and stitching them together to reconstruct the full high-resolution microscope image.

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
Example to display downsampled image:
```python
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('stitched_downsampled.tiff')
plt.imshow(img)
plt.axis('off')
plt.show()
```



### Thanks to [cellgeni/cloupe](https://github.com/cellgeni/cloupe.git) for inspiration and concepts used in this project.
some of the concepts used in this repo are from cellgeni/cloupe, such as opening a cloupe file in Python and iterating through its content 
