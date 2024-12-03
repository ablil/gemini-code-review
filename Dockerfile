FROM python:3.12

COPY requirements.txt /requirements.txt
RUN pip install -q -r /requirements.txt

COPY . /

ENTRYPOINT ["/entrypoint.sh"]
