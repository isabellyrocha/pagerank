FROM python:2.7

#RUN apt-get update
#RUN apt-get install -y python python-pip wget
#RUN python -m pip install influxdb
RUN pip install influxdb
# Copy the static binary over to the final image
ADD ./InfluxDB.py /usr/local/bin
ADD ./__init__.py /usr/local/bin
ADD ./page.py /usr/local/bin
ADD ./pagerank.10k /usr/local/bin
ADD ./pagerank.py /usr/local/bin
ADD ./Dummy.py /usr/local/bin
#RUN mkdir -p /pagerank
#WORKDIR /pagerank
#ONBUILD COPY . /pagerank

CMD ["python", "/usr/local/bin/pagerank.py" ]
