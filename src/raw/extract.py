import requests
import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv(".env")

items_dict = {
    "/posts": "posts",
    "/users": "users",
    "/comments": "comments"
}

BASE_URL = os.getenv("base_url")
AWS_PROFILE = os.getenv("AWS_PROFILE")
S3_BUCKET = os.getenv("S3_BUCKET")

if not BASE_URL or not AWS_PROFILE or not S3_BUCKET:
    raise ValueError("Verifique as variáveis de ambiente no arquivo .env")


def extract_api(item):

    response = requests.get(BASE_URL + item, timeout=30)
    response.raise_for_status()

    dados = response.json()

    return dados


def upload_s3(dados, item):

    session = boto3.Session(profile_name=AWS_PROFILE)

    cliente = session.client("s3")

    string = json.dumps(dados, ensure_ascii=False).encode("utf-8")

    nome = items_dict.get(item)

    cliente.put_object(
        Bucket=S3_BUCKET,
        Key=f"bronze/{nome}.json",
        Body=string,
        ContentType="application/json"
    )


def extract_load_api(item):

    dados = extract_api(item)

    print(f"{item} extraído com sucesso!")

    upload_s3(dados, item)

    print(f"{item} inserido no bucket com sucesso!")


if __name__ == "__main__":

    for item in items_dict:
        extract_load_api(item)