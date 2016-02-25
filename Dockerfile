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
RUN pip install --upgrade pip setuptools -r requirements-tests.txt
RUN python setup.py develop

# fix up broken stdlib-list permissions, see:
#   https://github.com/jackmaney/python-stdlib-list/issues/2
RUN chmod go+r -R /usr/local/lib/python3.5/site-packages/stdlib*

# setup entry point
USER pytest
ENTRYPOINT ["py.test"]