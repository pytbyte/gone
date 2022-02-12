 

# Dockerfile
FROM python:3
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        mysql-client libmysqlclient-dev
WORKDIR /
ADD ./requirements.txt ./
RUN pip3 install --upgrade pip; \
    pip3 install -r requirements.txt

 CMD ["python","wsgi.py"]