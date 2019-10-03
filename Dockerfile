FROM python:3.7-alpine

COPY bots/config.py   /bots/
COPY bots/reportip.py /bots/
COPY requirements.txt /
RUN pip3 install -r   /requirements.txt

WORKDIR /bots
CMD ["python3", "reportip.py"]
