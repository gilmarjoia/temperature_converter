FROM python:3.11-slim
WORKDIR /app
COPY temperature_converter.py ./
CMD ["python3"] 