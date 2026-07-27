FROM python:3.12-slim

# Cài đặt g++ cho C++20 và các thư viện cần thiết
RUN apt-get update && apt-get install -y g++ && rm -rf /var/lib/apt/lists/*

# Copy script chạy code vào image
COPY runner.sh /runner.sh
RUN chmod +x /runner.sh

WORKDIR /app
