FROM python:3.7-alpine

COPY myipbot.py       /
COPY requirements.txt /
RUN pip3 install -r   /requirements.txt

WORKDIR /
CMD ["python3", "myipbot.py"]
