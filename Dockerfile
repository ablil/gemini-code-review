FROM ghcr.io/ablil/gemini-code-review:latest

COPY *.py prompt.txt enrypoint.sh /

RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
