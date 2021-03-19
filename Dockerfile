FROM python:3.7.9
RUN pip install pipenv
COPY Pipfile* /tmp


RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/myapp
WORKDIR  /tmp/myapp
# RUN pip install /tmp/myapp
ENV FLASK_APP=Main
CMD ["flask","run","--host=0.0.0.0"]
EXPOSE 5000