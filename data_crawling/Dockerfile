# Sử dụng base image chứa Python
FROM python:3.9-slim

# Thiết lập thư mục làm việc mặc định trong container
WORKDIR /data

RUN pip install requests
RUN pip install unidecode
RUN pip install fastapi uvicorn
RUN pip install schedule

COPY . /data/

# Command để chạy ứng dụng data_crawling khi container được khởi chạy
CMD ["uvicorn", "crawData:app", "--host", "0.0.0.0", "--port", "5555"]




