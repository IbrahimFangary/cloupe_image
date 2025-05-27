# cloupe_image

`cloupe_image` reconstructs large high-resolution microscope images stored as tiles inside 10x Genomics `.cloupe` files by stitching them into a single image.

## Installation

```bash
pip install git+https://github.com/IbrahimFangary/cloupe_image.git
```

# how to use 
```python
import cloupe_image

cloupe_image.stitch_cloupe_image('your_file.cloupe')
```

## The output includes a very high-resolution image (stitched_highres.tiff) and a downsampled version (stitched_downsampled.tiff) for easier visualization.
Example to display downsampled image:
```python
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('stitched_downsampled.tiff')
plt.imshow(img)
plt.axis('off')
plt.show()
```

Thanks to cellgeni/cloupe for inspiration and concepts used in this project.
some of the concepts used in this repo are from cellgeni/cloupe, such as opening a cloupe file in Python and iterating through its content 
