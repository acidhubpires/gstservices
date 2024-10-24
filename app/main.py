from fastapi import FastAPI, UploadFile, File, HTTPException
from app.processing.file_processing import processar_arquivo_upload

app = FastAPI()

@app.post("/upload")
async def upload_and_process_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        resultado = processar_arquivo_upload(contents, file.filename)
        return {"resultado": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
