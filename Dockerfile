# run tests in a more reproduceble and isolated environment
#
# Build the docker image once with:
#   docker build -t pytest .
# Run the tests with:
#   docker run --rm -it -v `pwd`:/src pytest [PYTEST_OPTIONS]
#
FROM python:3

# setup workdir
COPY . /src
WORKDIR /src

# setup the python and pytest environments
RUN pip install --upgrade pip setuptools
RUN pip install --upgrade -r requirements.txt
RUN pip install --upgrade -r requirements-tests.txt
RUN pip install -e .

# setup pytest user
RUN adduser --disabled-password --gecos "" --uid 7357 pytest
USER pytest

# setup entry point
ENTRYPOINT ["py.test"]
