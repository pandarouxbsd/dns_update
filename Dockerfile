FROM python:3.7.3-slim

COPY script.py /app/
WORKDIR /app/
RUN pip install requests

CMD [ "python", "/app/script.py" ]