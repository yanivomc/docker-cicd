# logGenerator.py 
FROM python:3.7-slim as builder
# Install dependencies from requirements.txt using pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



FROM builder as final
WORKDIR /app
COPY ./logGenerator.py ./logGenerator.py
CMD ["python", "./logGenerator.py"]