FROM python:3.8-slim

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install & use pipenv
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --system --deploy

WORKDIR /app
COPY multi_server.py /app

EXPOSE 53/tcp
EXPOSE 53/udp

CMD ["python", "multi_server.py"]
