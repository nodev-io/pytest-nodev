# run tests in a more reproduceble and isolated environment
#
# Build the docker image once with:
#   docker build -t pytest .
# Run the tests with:
#   docker run --rm -it -v `pwd`:/src pytest [PYTEST_OPTIONS]
#
FROM python:3

# setup pytest user
RUN adduser --disabled-password --gecos "" --uid 7357 pytest
COPY . /src
WORKDIR /src

# setup the python and pytest environments
RUN pip install --upgrade pip setuptools \
        -r requirements-dev.txt \
        -r requirements-tests.txt
RUN python setup.py develop

# setup entry point
USER pytest
ENTRYPOINT ["py.test"]
