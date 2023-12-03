# Using AWS Titan multimodal embeddings for searching movie by title and poster

Demo project to create a search engine for movies using AWS Titan multimodal embeddings. An AWS account is required to create the embeddings, the application itself, as well as Opensearch run locally.

## Pre-requisites

- AWS account
- Access to AWS Bedrock and AWS Titan models
- Docker compose / Docker
- Python 3.9 or above

___Remark__: Using AWS Bedrock and AWS Titan is not covered by the free tier._

## Setup
Install the required python packages:

```bash
pip install -r requirements.txt
```

Start opensearch and the opensearch dashboard with docker-compose:

```bash
docker-compose up -d
```

### Prepping the data

The notebook `data_prep.ipynb` contains the code to fetch the data and create the embeddings before storing them in and opensearch index.

- Downloads the images and meta-data
- Creates the embeddings
- Create the index
- PUT the embeddings to the index

The `movielens` folder contains data on 56 movies (released in 2023 and more than 150 ratings on Movielens)


### Gradio Application

The `app.py` file contains the code to run the gradio application. The application allows you to search for movies by title and poster. The application will return the top 3 results based on the cosine similarity between the query and the embeddings via an Opensearch knn query.

## Article on Medium

[Article](https://pjcr.medium.com/using-aws-titan-multimodal-embeddings-for-searching-movie-by-title-and-poster-aaf9a89da665)