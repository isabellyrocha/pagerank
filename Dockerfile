FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python python-pip wget
RUN python -m pip install influxdb
# Copy the static binary over to the final image
ADD ./InfluxDB.py /usr/local/bin
ADD ./__init__.py /usr/local/bin
ADD ./page.py /usr/local/bin
ADD ./pagerank.input /usr/local/bin
ADD ./pagerank.py /usr/local/bin
ADD ./Dummy.py /usr/local/bin

ENTRYPOINT ["python", "/usr/local/bin/pagerank.py" ]
