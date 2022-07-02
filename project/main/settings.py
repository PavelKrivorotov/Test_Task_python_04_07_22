
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import boto3
from botocore.client import Config


# ...

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "e974c76505f166db6299661101ad78974df4e3b705f0879ecc2db7b959a09f55"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_SECONDS  = 86400


# Database connect
 
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread" : False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Test Database connect

test_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"

test_engine = create_engine(test_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread" : False})

test_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# MinIo connect

MINIO_URL = "http://localhost:9000"

MINIO_ACCESS_KEY = "elx2jIjtZzQE5ZHP"

MINIO_SECRET_KEY = "17cdq3AO3hC7tJgicEGcBWPOa7yMue2n"

CLIENT = boto3.resource('s3', endpoint_url = MINIO_URL, aws_access_key_id = MINIO_ACCESS_KEY, aws_secret_access_key = MINIO_SECRET_KEY,
                        config = Config(signature_version='s3v4'))

IDK = boto3.client('s3', endpoint_url = MINIO_URL, aws_access_key_id = MINIO_ACCESS_KEY, aws_secret_access_key = MINIO_SECRET_KEY,
                    config = Config(signature_version='s3v4'))

