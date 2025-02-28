import boto3
import psycopg2
import pandas as pd
import json

# AWS Configurations
S3_BUCKET = "saurav1129"
S3_KEY = "data.csv"
RDS_HOST = "godigital-test1.cmhowge4gh37.us-east-1.rds.amazonaws.com"
RDS_DB = "godigital-test1"
RDS_USER = "admin"
RDS_PASSWORD = "9823954722"
GLUE_DATABASE = ""
GLUE_TABLE = ""

# Initialize AWS Clients
s3 = boto3.client('s3')
import os
import boto3

region = os.getenv("AWS_REGION", "us-east-1")  # Default to us-east-1 if env variable is not set
glue = boto3.client('glue', region_name=region)


def read_from_s3():
    """ Read CSV file from S3 and return as DataFrame """
    obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
    df = pd.read_csv(obj['Body'])
    return df

def push_to_rds(df):
    """ Insert DataFrame into RDS """
    try:
        conn = psycopg2.connect(
            host=RDS_HOST,
            database=RDS_DB,
            user=RDS_USER,
            password=RDS_PASSWORD
        )
        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO your_table (column1, column2) VALUES (%s, %s)",
                (row['column1'], row['column2'])
            )
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Data successfully pushed to RDS")
    except Exception as e:
        print(f"⚠️ RDS Insertion Failed: {e}")
        return False
    return True

def push_to_glue(df):
    """ Convert DataFrame to JSON and push to Glue """
    try:
        records = df.to_dict(orient='records')
        glue.put_record(
            DatabaseName=GLUE_DATABASE,
            TableName=GLUE_TABLE,
            Records=[{"Data": json.dumps(record)} for record in records]
        )
        print("✅ Data successfully stored in Glue")
    except Exception as e:
        print(f"⚠️ Glue Insertion Failed: {e}")

if __name__ == "__main__":
    df = read_from_s3()
    if not push_to_rds(df):
        push_to_glue(df)
