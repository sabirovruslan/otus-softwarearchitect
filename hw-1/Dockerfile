FROM python:3.8

EXPOSE 8000

ADD requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /src
ADD app /src

ENTRYPOINT ["python", "/src/app.py"]