import json
import os

import boto3
import psycopg2
from fastapi import FastAPI

app = FastAPI(title="CloudShop API")

DB_HOST = "aws-cloud-lab-dev-postgres.cs3i6a24sthk.us-east-1.rds.amazonaws.com"
DB_NAME = "cloudshop"
DB_SECRET_ARN = "arn:aws:secretsmanager:us-east-1:589744711110:secret:aws-cloud-lab-dev-db-credentials-RrSMqY"
AWS_REGION = "us-east-1"


def get_db_credentials():
    client = boto3.client("secretsmanager", region_name=AWS_REGION)
    response = client.get_secret_value(SecretId=DB_SECRET_ARN)
    return json.loads(response["SecretString"])


@app.get("/")
def root():
    return {"service": "CloudShop API", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/db-health")
def db_health():
    creds = get_db_credentials()

    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=creds["username"],
        password=creds["password"],
        port=5432,
        connect_timeout=5,
    )

    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "database": "postgres",
        "status": "connected",
        "result": result[0],
    }


@app.get("/products")
def products():
    return [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Phone", "price": 699.99},
        {"id": 3, "name": "Headphones", "price": 149.99},
    ]