#Deriving the latest base image
FROM python:latest


#Labels as key value pair
LABEL Maintainer="unahur/arqsw"


# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app

#to COPY the remote file at working directory in container
COPY requirements.txt ./

# Now the structure looks like this '/usr/app/src/test.py'
RUN pip install -r  /usr/app/requirements.txt

COPY setup.json ./

CMD [ "pymodbus.simulator", "--json_file", "/usr/app/setup.json", "--modbus_server", "server_try_serial"]