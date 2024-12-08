FROM ghcr.io/ablil/gemini-code-review:latest
COPY . /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
