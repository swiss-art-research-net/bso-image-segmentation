# BSO Image Segmentation

Training data and models to extract coordinates of image, document and colour bar from images.

## Usage

- Clone [dhSegment](https://github.com/dhlab-epfl/dhSegment) repo
- Annotate images data using [RunwayML](https://runwayml.com/)
- Create training data using the `generate-training-images.ipynb` notebook
- t.b.c.

## Annotating images using RunwayML

RunwayML supports the creation of annotated datasets. This is currently possible without a paid subscription. To do so

1. Go to Train
2. Choose _Image_
3. Create a new dataset, picking a folder with BSO images
4. Pick or create an annotation group with the categories `Colour Bar`, `Image`, and `Document`
5. Annotate images
6. Export annotations