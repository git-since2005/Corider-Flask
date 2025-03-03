FROM python:3.12.2
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV secret=EncryptForCorider
CMD ["python", "main.py"]
