# Using the Ubuntu image (our OS)
FROM ubuntu:latest
# Maintainer
MAINTAINER Aleksandr Dubrovin <dubrovinmail@gmail.com>
ENV PROJECT_DIR=/app
RUN echo 'Hi, I am in your container'

WORKDIR ${PROJECT_DIR}
# Copy files from github repo to app folder
COPY . ${PROJECT_DIR}
RUN ls -la ${PROJECT_DIR}
# Python and Pip
# Update package manager (apt-get)
# and install (with the yes flag `-y`)
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip

#You need to use --deploy flag, so your build will fail if your Pipfile.lock is out of date
#You need to use --ignore-pipfile when we ignore Pipfile and use Pipfile.lock
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile
# Run make_datasets.py
ENTRYPOINT ["python", "./app/src/data/make_datasets.py"]
# Open ports
EXPOSE 8000