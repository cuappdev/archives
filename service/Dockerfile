FROM python:2.7
RUN mkdir -p /service
ADD src /service/src
ADD requirements.txt /service/requirements.txt
WORKDIR /service/
RUN pip install git+https://github.com/cuappdev/appdev.py.git --upgrade
RUN pip install -r requirements.txt
WORKDIR /service/src
RUN rm -rf migrations
CMD python -u run.py $DB_USERNAME $DB_PASSWORD $DB_HOST $DB_NAME
