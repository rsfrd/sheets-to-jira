from python:2-wheezy
copy requirements.txt /requirements.txt
# RUN apt-get python-slugify
# RUN apk add --update gcc musl-dev libffi-dev libedit-dev bash openssl-dev readline
RUN pip install -r /requirements.txt
RUN pip install python-slugify
