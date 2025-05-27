from setuptools import setup, find_packages

setup(
    name="Cloupe_image",
    version="0.1.0",
    author="Ibrahim Fangary",
    description="Tool to stitch high-res images (the closest resolution to the microscope image) from 10x Genomics .cloupe files",
    packages=find_packages(),
    install_requires=[
        "Pillow",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'stitch-cloupe=cloupe_image.stitch_cloupe_image:stitch_cloupe_image_cli',
        ],
    },
)

