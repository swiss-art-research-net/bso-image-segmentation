
## Workflow

### Fetch input data

Need:
```csv
id, image, width, height
```

id: unique identifier (will be used as fiel name)
image: IIIF Image API URL
width: original width of image
height: original height of image

Provided as either
    - input CSV file
    - SPARQL query

Arguments:
- mode: CSV/SPARQL
- sparqlQuery: binding to ?id ?image ?width ?height
- SPARQL endpoint

If SPARQL query, store output as CSV

### Fetch image sizes

For rows in input data that lack width and height (e.g. when not available through SPARQL), fetch image sizes by parsing IIIF API

### Download images

Arguments:
- folder where images should be downloaded to

Download images only if not already present. Resize to width 1024 (through IIIF call)

### Apply model

Arguments:
- folder where images are
- output txt

Read txt file with image coordinates
Segment only images that are not already present in txt file

### Create RDF data

Read input data and convert to RDF regions.