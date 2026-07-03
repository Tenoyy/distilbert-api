import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import logging
import uvicorn

# 1 создаём общий FileHandler
file_handler = logging.FileHandler("py_log.log", mode="w")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))

# 2 настраиваем корневой логгер (для наших сообщений)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)

# 3 настраиваем логгеры Uvicorn, чтобы они тоже писали в файл
for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
    uv_logger = logging.getLogger(logger_name)
    uv_logger.setLevel(logging.INFO)
    uv_logger.addHandler(file_handler)

logger = logging.getLogger(__name__)

app = FastAPI(title="ML Model API")

# Единократная загрузка модели при старте сервера
logging.info("Downloading model DistilBERT...")
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)
logging.info("Model downloaded!")

class BatchTextInput(BaseModel):
    texts: list[str]

# Схема входных данных
class TextInput(BaseModel):
    text: str


@app.get("/")
def read_root():
    return {"message": "ML Model API with DistilBERT"}

# (Health Check)
@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.post("/predict")
def predict_sentiment(data: TextInput):
    result = classifier(data.text)[0]
    return {
        "text": data.text,
        "label": result["label"],
        "score": round(result["score"], 4)
    }

class BatchTextInput(BaseModel):
    texts: list[str]

@app.post("/predict_batch")
def predict_batch(data: BatchTextInput):
    results = classifier(data.texts)
    return [
        {"text": t, "label": r["label"], "score": round(r["score"], 4)}
        for t, r in zip(data.texts, results)
    ]


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True  # включаем access-логи
    )