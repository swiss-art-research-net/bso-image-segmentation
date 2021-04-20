# BSO Image Segmentation

Training data and models to extract coordinates of image, document and colour bar from images.

## Prerequisite

Follow preparation steps from https://dhsegment.readthedocs.io/en/latest/start/install.html:

1. Install Anaconda or Miniconda
2. Create a virtual environment
`conda create -n dh_segment python=3.6`
3. Activate it
`conda activate dh_segment`
4. Install dhSegment
`pip install git+https://github.com/dhlab-epfl/dhSegment`
5. Install TensorFlow 1.13
`conda install tensorflow-gpu=1.13.1`

## Training

- Clone [dhSegment](https://github.com/dhlab-epfl/dhSegment) repo:
` git clone https://github.com/dhlab-epfl/dhSegment.git`
- (optional) Annotate images data using [RunwayML](https://runwayml.com/)
- Download images using the `download-annotated-images.ipynb` notebook
- Create training data using the `generate-training-images.ipynb` notebook
- Split into training and validation set by crunning the `split-training-data.ipynb` notebook until the appropriate cell
- Download pretrained model by running:
```
cd pretrained_models
python download_resnet_pretrained_model.py
cd ..
```
- Train by running `python dhSegment/train.py with training/config.json`
- (optional) observe training by running `tensorboard --logdir model`

## Classifying

- Download images to classify using the `download-images-to-classify.ipynb`
- (optional) Set the `limit` and `randomise` parameters to download only some of the images
- Run `python predict.py`

## Annotating images using RunwayML

RunwayML supports the creation of annotated datasets. This is currently possible without a paid subscription. To do so

1. Go to Train
2. Choose _Image_
3. Create a new dataset, picking a folder with BSO images
4. Pick or create an annotation group with the categories `Colour Bar`, `Image`, and `Document`
5. Annotate images
6. Export annotations

## Docker

To avoid having to configure the environment locally, you can use the Docker configuration (CPU only).

Copy and edit the `.env` configuration: `cp .env.example .env`

And run using `docker-compose up -d`