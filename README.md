# IOT Collection
This is a collection of IoT applications with AI enabled.

## Project Structure
[ROOT]

|___ aiiot_gateway - agent to capture iot gateway network interfaces and protector to detect any abnormal network traffic.

|___ beats - a set of shippers for elasticsearch nd logstash.

|___ documents - a set of documents for secured IoT gateway.

|___ elasticsearch - open source, distributed and RESTful search engine.

|___ emqx - A scalabledistributed MQTT message broker for IoT in 5G Era.

|___ emqx-rel - the edge version of emqx.

|___ kibana - the GUI of elastic stack.

|___ logstash - transport and process the logs, events or other data.

|___ mainflux - Industrial IoT Messaging and Device Management Platform.

|___ ncs_aiiot_gateway - the function to capture gateway network adaptor traffic with node-red.

|___ ncs_aiiot_platform - the function to capture gateway network adaptor traffic with node-red.

|___ offensive-docker - an image with the more used offensive tools to create an environment easily and quickly to launch assessment to the targets.

|___ pyshark - a python wrapper interface for wireshark and it's used by aiiot_gateway.

|___ raspberrypi_4 - how to prepare an ubuntu 20.04 ready gateway.

|___ thingsboard - Open-source IoT Platform - Device management, data collection, processing and visualization.

|___ thingsboard-gateway - An open-source IoT Gateway - integrates devices connected to legacy and third-party systems with ThingsBoard IoT Platform using OPC-UA and MQTT protocols.

|___ Ubuntu1804-CIS - os hardening scripts.

|___ Ubuntu_core - introduction on Ubuntu hardening service.

|___ website - the official website for future secured IoT gateway.

|___ wireshark - Mainly use it's tshark network capture and analyzer.

|___ more and coming...
## How to Install
Refer to respective readme.md in each project folder.

## Get Started Quickly
The quick way to run a demonstration is based on docker.

1. run EMQX broker.
```shell script
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8883:8883 -p 8084:8084 -p 18083:18083 emqx/emqx
```

2. copy aiiot_gateway folder to any iot gateway such as Raspberry Pi.
```shell script
# remember to edit the MQTT Broker adress in nic-gateway.py
python3 nic-gateway.py
```
3. run offensive sumulator docker.
```shell script
cd offensive-docker
docker build -t offensive-docker .
docker run --rm -it --name my-offensive-docker offensive-docker /bin/zsh
```

## How to Develop

## FAQ

## Work Daily
* 2020-10-14
Completed the individual functionality of securied IoT gateway and need to write a step-by-step guide for the demonstration. 
Now create one folder "0_quick_start" to move respective documents into it.
