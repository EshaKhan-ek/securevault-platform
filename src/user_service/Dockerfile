FROM python:3.12-slim

# Code ke liye root par required folder banayein
RUN mkdir /auth_service

WORKDIR /app

# Requirements install karein (Tsinghua mirror ke sath)
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=1000 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# Baqi ka saara code copy karein
COPY . .

# Nayi generate ki gayi key ko uski required jagah par place karein
COPY keys/public.pem /auth_service/public.pem

EXPOSE 8000

# App start karein
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
