from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pdf_services.services import create_pdf


app = FastAPI()


@app.get("/")
def index():
    return {
        "status": True
    }


@app.get("/file")
def file_response():
    fileBytes = create_pdf()
    response = StreamingResponse(fileBytes, media_type="application/pdf")
    response.headers["Content-Disposition"] = "attachment; filename=test.pdf"
    return response
