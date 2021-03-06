# BSO Image Segmentation

This repository contains methods for determining the coordinates (bounding box) of the relevant content in the digitised images of the [BSO](https://bso.swissartresearch.net) collection.

Two different approaches have been used: a Machine Learning method using [DHSegment](https://dhsegment.readthedocs.io/en/latest/) and a deterministic method using [OpenCV](https://opencv.org/)

## Examples
<table>
  <thead>
    <tr><th>Original Image</th><th>Relevant Region</tr>
  </thead>
  <tbody>
    <tr>
      <td><img src="https://www.e-rara.ch/zuz/i3f/v20/21210416/full/300,/0/default.jpg"></td>
      <td><img src="https://www.e-rara.ch/zuz/i3f/v20/21210416/57,64,6447,4742/300,/0/default.jpg"></td>
    </tr>
    <tr>
      <td><img src="https://www.e-rara.ch/zuz/i3f/v20/12847340/full/300,/0/default.jpg"></td>
      <td><img src="https://www.e-rara.ch/zuz/i3f/v20/12847340/30,32,2166,1395/300,/0/default.jpg"></td>
    </tr>
    <tr>
      <td><img src="https://bso-iiif.swissartresearch.net/iiif/2/nb-1030793/full/300,/0/default.jpg"></td>
      <td><img src="https://bso-iiif.swissartresearch.net/iiif/2/nb-1030793/1141,1164,3625,1969/300,/0/default.jpg"></td>
    </tr>
  </tbody>
</table>

## Contents

  * [OpenCV](#opencv)
  * [DHSegment](#dhsegment)
  * [Docker](#docker)
  * [Pipeline](#pipeline)
## OpenCV

### Usage

To use the openCV detection method import the class in your Python project

```python
from openCV.BSOImageCropping import BSOImageCropping
```

Load an image using opencv and convert it to the RGB format
```python
import cv2
image = cv2.imread(filename)
image = image[:,:,::-1]
```

Get the bounding box of the relevant region:
```python
detector = BSOImageCropping()
x,y,w,h = detector.cropImage(image)
```
#### Options
##### Selection strategy
There are two strategies for determining the relevant region. They return either the largest region detected or the largest region that is closest to a square. The latter strategy is useful for eliminating the colour bar as an option. The default strategy returns the squarest region.

```python
# Return largest region
x,y,w,h = detector.cropImage(image, selectMethod=BSOImageCropping.SELECT_LARGEST)
```

```python
# Return squarest largest region
x,y,w,h = detector.cropImage(image, selectMethod=BSOImageCropping.SELECT_SQUAREST)
```

##### Debugging

Initialise the class with `showImages=True` to display the in-between steps. Useful for debugging in a Jupyter Notebook.

```python
detector = BSOImageCropping(showImages=True)
```


## DHSegment
### Prerequisite

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
6. Clone the [dhSegment](https://github.com/dhlab-epfl/dhSegment) repo:
` git clone https://github.com/dhlab-epfl/dhSegment.git`

Alternatively, use the Docker configuration included in the repository.

**Note:** make sure you have GIT LFS installed on the client where the repository is cloned. Otherwise, the pre-trained model will not be included.

### Training

- (optional) Annotate images data using [RunwayML](https://runwayml.com/)
- Download images using the `download-annotated-images.ipynb` notebook
- Create training data using the `generate-training-images.ipynb` notebook
- Split into training and validation set by running the `split-training-data.ipynb` notebook until the appropriate cell
- Download pretrained model by running:
```
cd pretrained_models
python download_resnet_pretrained_model.py
cd ..
```
- Train by running `python dhSegment/train.py with training/config.json`
- (optional) observe training by running `tensorboard --logdir model`

### Classifying

- Download images to classify using the `download-images-to-classify.ipynb`
- (optional) Set the `limit` and `randomise` parameters to download only some of the images
- Run `python predict.py`

#### Annotating images using RunwayML

RunwayML supports the creation of annotated datasets. This is currently possible without a paid subscription. To do so

1. Go to Train
2. Choose _Image_
3. Create a new dataset, picking a folder with BSO images
4. Pick or create an annotation group with the categories `Colour Bar`, `Image`, and `Document`
5. Annotate images
6. Export annotations

### Debug

To check the result visually on specific images, place them in the `debug/images` directory. Enter the container with

```
docker exec -it sari_image_classification_dhsegment bash
```

and run

```
python debug.py
```

The results are saved in `debug/processed_images`.
## Docker

To avoid having to configure the environment locally, you can use the Docker configuration (CPU only).

Copy and edit the `.env` configuration: `cp .env.example .env`

And run using `docker-compose up -d`

Jupyter notebooks are accessible at [localhost:8890]() (if default ports are used). To execute Python commands, bash into Docker container using `docker exec -it sari_image_classification_dhsegment bash` (if default container name is used)

## Pipeline

The repository includes a Jupyter Notebook that can be used to run a complete image segmentation pipeline from retrieving the images, to applying the pretrained model and outputting RDF/Trig files for ingest into a [ResearchSpace](https://www.researchspace.org) or [Metaphacts](https://bitbucket.org/metaphacts/metaphacts-community) Instance.

The pipeline can operate from a CSV data file or by querying a SPARQL endpoint directly. In the latter case, make sure that the SPARQL endpoint is accessible by the Jupyter Notebook. If you are running the Notebook using the Docker Compose configuration provided, this might mean attaching the container to the an external (Docker) network. The included `docker-compose.override.example.yml` file can be used as a template.

Configuration of the workflow is done by adapting the file `pipeline/config.yml` as required. Then, acces the `notebooks/pipeline.ipynb` or `notebooks/pipeline-opencv.ipynb` notebook and execute the steps provided 

### config.yml
```yaml
# The CSV file to store and (in CSV mode) read the input data
dataFile: ../data/data.csv

# The Trig file to store the RDF output
trigFile: ../output/regions.trig

# The directory where source images are stored or downloaded to
imageDirectory: ../data/images


# Operation mode
# ---
# SPARQL : Query data from a SPARQL endpoint (configuration below)
# CSV : Read data from CSV file (configuration below)
mode: SPARQL

# The endpoint to execute the query when in SPARQL mode
endpoint: http://blazegraph:8080/blazegraph/sparql

# The SPARQL Query (when in SPARQL mode)
# ---
# The SPARQL Query should bind to
# ?id : unique identifier (will also used as file name to store the images)
# ?image : the IIIF Image API URL of the image
# ?width : (optional) the width of the image in its original size
# ?height : (optional) the height of the image in its original size
query: '
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX la: <https://linked.art/ns/terms/>
    PREFIX search: <https://platform.swissartresearch.net/search/>
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    
    SELECT ?id ?image ?width ?height WHERE {
      ?subject a search:Object ;
        crm:P128_carries/la:digitally_shown_by/la:digitally_available_via ?iiif . 
      ?iiif dcterms:conformsTo <http://iiif.io/api/image> ;
            la:access_point ?image .
      BIND(STRAFTER(STR(?subject), "https://resource.swissartresearch.net/artwork/") as ?id)
  } ORDER BY ?id'
```
