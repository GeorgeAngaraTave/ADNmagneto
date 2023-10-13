FROM python:3.7-slim-buster

LABEL maintainer="Jorge Brunal <diniremix@gmail.com>"

RUN mkdir /app

#Set flask_app as working directory
WORKDIR /app

#copy data from current dir into flask_app
COPY . /app

#install dependencies
RUN apt-get update
RUN apt-get install -y nano curl wget
RUN pip install --trusted-host pypi.python.org -r requirements.txt

#create container environment name
ENV VERSION 3.0.b

# set path to Google service-account
ENV GOOGLE_APPLICATION_CREDENTIALS /root/google-account.json
ENV FLASK_APP main.py
ENV FLASK_ENV production
ENV FLASK_DEBUG false
ENV FLASK_RUN_PORT 8080

#Use this ports
EXPOSE 6969
EXPOSE 80
EXPOSE 8080

# run main.py with gunicorn
# CMD ["gunicorn", "-w 4", "main:app"]

#run main.py with python
# CMD ["flask","run"]
CMD ["python","main.py"]
