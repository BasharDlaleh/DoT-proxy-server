FROM python:3.7-slim

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY server.py /app

EXPOSE 53
# During debugging, this entry point will be overridden.
CMD ["python", "server.py"]
