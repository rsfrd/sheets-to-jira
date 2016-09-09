from python:2-wheezy
copy requirements.txt /requirements.txt
# RUN apk add --update gcc musl-dev libffi-dev libedit-dev bash openssl-dev readline
RUN pip install -r /requirements.txt
