Swagger находится по адресу 127.0.0.1:8000/docs

Пример запроса в /predict:
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "this is working"
}'

Ответ:
{
  "text": "this is working",
  "label": "POSITIVE",
  "score": 0.9995
}

Пример запроса в /predict_batch:
curl -X 'POST' \
  'http://127.0.0.1:8000/predict_batch' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "texts": [
    "this is fine", "this is not fine", "its alright"
  ]
}'

Ответ:
[
  {
    "text": "this is fine",
    "label": "POSITIVE",
    "score": 0.9999
  },
  {
    "text": "this is not fine",
    "label": "NEGATIVE",
    "score": 0.9998
  },
  {
    "text": "its alright",
    "label": "POSITIVE",
    "score": 0.9996
  }
]
