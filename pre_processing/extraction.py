from PyPDF2 import PdfReader
from fastapi import UploadFile
import pandas as pd
import docx2txt

def extract_text_from_pdf(file: UploadFile) -> str:
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text().replace("\n","")
    return text

def extract_text_from_xlsx(file: UploadFile) -> str:
    data = pd.read_excel(file.file,sheet_name=None)
    text = ""
    # for i in range(len(df)):
    #     text += " ".join([str(x) for x in df.iloc[i].values])
    # return text
    for sheet_name, df in data.items():
        text +=df.fillna("").to_string(index=False, header=True).replace("\n", "")
    return text

def extract_text_from_docx(file: UploadFile) -> str:
    return docx2txt.process(file.file)