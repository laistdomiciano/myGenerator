from dotenv import load_dotenv
from fpdf import FPDF
from datetime import datetime
import boto3
import os

load_dotenv()

AWS_S3_BUCKET_NAME = 'pdfcontracts'
AWS_REGION = 'eu-north-1'
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')


def generate_pdf(contract_content, contract_id, employee_name):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Contract Document', 0, 1, 'C')

    pdf.set_font('Arial', '', 12)
    pdf.ln(10)  # Add a line break
    pdf.multi_cell(0, 10, contract_content)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"contract_{employee_name}_{contract_id}_{timestamp}.pdf"
    pdf_output_path = f"/tmp/{filename}"

    pdf.output(pdf_output_path)

    return pdf_output_path, filename


def connect_aws():
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )
    s3 = session.resource('s3')
    return s3


def upload_to_s3(file_path, s3_filename):
    s3 = connect_aws()
    bucket = s3.Bucket(AWS_S3_BUCKET_NAME)
    try:
        bucket.upload_file(file_path, s3_filename)
        return f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_filename}"
    except Exception as e:
        return str(e)

