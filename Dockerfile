FROM python:3.8-slim-buster
# This will serve as base image on which other things can be added via commands, basically you get a lightweight operating system with Python installed on it

WORKDIR /src
#sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions, a src folder will be created in docker image

ARG BUILD_ENV
ENV FLASK_ENV $BUILD_ENV
ENV FLASK_APP autoapp.py

#RUN mkdir requirements

COPY app/ ./app
COPY autoapp.py .
COPY requirements/ ./requirements
COPY run_tests.sh .
# Copy required source code
COPY tests ./tests

RUN ls .
# just for debugging to see what's ther in the WORKDIR

RUN if [ "$BUILD_ENV" = "test" ]; then pip install -r requirements/development.txt ; fi
RUN if [ "$BUILD_ENV" = "test" ]; then export FLASK_DEBUG=true ; fi
RUN if [ "$BUILD_ENV" != "test" ]; then pip install -r requirements/production.txt ; fi

RUN chmod 777 run_tests.sh
RUN ./run_tests.sh
ENTRYPOINT flask run


# A brief about RUN, CMD, and ENTRYPOINT
# Use RUN to do the installation, making changes etc
# Use ENTRYPOINT to run a command used to start the service
# Use CMD to pass arguments to that command, they get appended automatically; You can override CMD while running docker image.
