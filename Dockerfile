FROM python:3.12

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY entrypoint.sh /entrypoint.sh
COPY gh.py /gh.py
COPY ai.py /ai.py
COPY app.py /app.py

ENTRYPOINT ["/entrypoint.sh"]
