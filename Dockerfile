# Using the Ubuntu image (our OS)
FROM ubuntu:20.04
# Maintainer
MAINTAINER Aleksandr Dubrovin <dubrovinmail@gmail.com>
ENV PROJECT_DIR=app
# Copy files from github repo to app folder
COPY . /${PROJECT_DIR}
WORKDIR /${PROJECT_DIR}

# Copy kaggle .json
RUN mv app/.kaggle /root && chmod 600 root/.kaggle/kaggle.json


# Python and Pip
# Update package manager (apt-get) and install (with the yes flag `-y`)
RUN apt-get update
RUN apt-get install -y \
    python3.8 \
    python3-pip
RUN pip install pipenv

# Add .venv folder inside project
ENV PIPENV_VENV_IN_PROJECT=1
#You need to use --deploy flag, so your build will fail if your Pipfile.lock is out of date
#You need to use --ignore-pipfile when we ignore Pipfile and use Pipfile.lock
RUN pipenv install --deploy --ignore-pipfile
# Add PATH to find python belong to .venv
ENV PATH=/${PROJECT_DIR}/.venv/bin

# Open ports
EXPOSE 8000

# Run make_datasets.py
ENTRYPOINT ["python", "src/data/make_datasets.py"]