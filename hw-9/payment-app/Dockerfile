FROM python:3.8

ADD requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /src
ADD src /src

CMD /usr/local/bin/gunicorn -w 2 -b :80 app.app:app --reload