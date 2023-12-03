import gradio as gr

import boto3
import json
import base64
from botocore.config import Config

import requests
from requests.auth import HTTPBasicAuth

base_url = "https://0.0.0.0:9200"
username = "admin"
password = "admin"

# Disable SSL warnings, equivalent to the --insecure flag in curl
requests.packages.urllib3.disable_warnings()

my_config = Config(
    region_name = 'us-east-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

bedrock = boto3.client(service_name="bedrock", config=my_config)
bedrock_runtime = boto3.client(service_name="bedrock-runtime", config=my_config)


def get_embedding_for_text(text):
    body = json.dumps(
        {
            "inputText": text
        }
    )

    response = bedrock_runtime.invoke_model(
        body=body, 
        modelId="amazon.titan-embed-image-v1", 
        accept="application/json", 
        contentType="application/json"       
    )

    vector_json = json.loads(response['body'].read().decode('utf8'))

    return vector_json, text


def result_to_html(hit):

    #get image as base64 the images are in the images folder
    img = open("images/" + hit['_source']['posterPath'], 'rb')
    img_base64 = base64.b64encode(img.read()).decode('utf-8').replace('\n', '')


    html = f"""
    <div style="display: flex; flex-direction: row; align-items: center; margin-bottom: 10px;">
        <img src="data:image/png;base64,{img_base64}" style="width: 150px; height: 225px; margin-right: 10px;"/>
        <div style="display: flex; flex-direction: column; justify-content: space-between;">
            <div style="display: flex; flex-direction: row; align-items: center; justify-content: space-between;">
                <div style="font-size: 20px; font-weight: bold; margin-right: 10px;">{hit['_source']['title']}</div>
                <div style="font-size: 20px; font-weight: bold; margin-right: 10px;">{hit['_score']}</div>
            </div>
            <div style="font-size: 15px;">{hit['_source']['plotSummary']}</div>
        </div>
    </div>
    """
    return html

def query(text, n=1):

    text_embedding = get_embedding_for_text(text)

    query = {
        "size": n,
        "query": {
            "knn": {
            "titan_multimodal_embedding": {
                "vector": text_embedding[0]['embedding'],
                "k": n
            }
            }
        },
        "_source": ["movieId", "title", "imdbMovieId", "posterPath", "plotSummary"]
        }

    response = requests.get(base_url + "/multi-modal-embedding-index/_search", auth=HTTPBasicAuth(username, password), verify=False, json=query)

    results = response.json()

    results_html = ""
    for hit in results['hits']['hits']:
        results_html += result_to_html(hit)

    return results_html

input_text = gr.Textbox(lines=2, label="Input Text")
output_html = gr.HTML(label="Results")


title = "Movie Search"
description = "Search for movies based on title or a description of the movie poster."

demo = gr.Interface(
    fn=query,
    inputs=input_text,
    outputs=output_html,
    title=title,
    description=description,
).launch()
