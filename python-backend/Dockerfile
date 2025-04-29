# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask flask-cors torch torchvision transformers pillow opencv-python

EXPOSE 5001

CMD ["python", "model_api.py"]
