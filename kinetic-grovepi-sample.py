# Copyright (c) 2017, 2018 Cisco and/or its affiliates.
#
# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.0 (the "License"). You may obtain a copy of the
# License at
#
#                https://developer.cisco.com/docs/licenses
#
# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

from time import sleep
import paho.mqtt.client as mqtt
import ssl
import grovepi

# GrovePi configuration

light_sensor = 0
grovepi.pinMode(light_sensor, "INPUT")
sound_sensor = 1
grovepi.pinMode(sound_sensor, "INPUT")
ultrasonic_ranger = 4

# Kinetic MQTT configuration
host = 'FQDNOfMQTTBrokerComesHere'
port = 8883
username = 'yourGatwayIdOrDeviceIdComesHere'
password = 'passwordForYourGWorDeviceIsGivenByKineticPortal'
cacert = '/etc/ssl/certs/ca-certificates.crt'

topicPrefix = '/v1/yourGatewayIdOrDeviceIdComesHere/json/dev2app/'
topic = topicPrefix + 'grove'

# Starting MQTT client
def on_connect(client, userdata, flags, respons_code):
    print("CONNACK received with code %d." % (respons_code))

client = mqtt.Client(protocol=mqtt.MQTTv31)
client.username_pw_set(username, password)
client.tls_set(cacert, certfile = None, keyfile = None, tls_version = ssl.PROTOCOL_TLSv1_2)
client.on_connect = on_connect
client.connect(host, port = port, keepalive = 60)

client.loop_start()

# Main loop
while True:
    # Read sensors
    light_val = str(grovepi.analogRead(light_sensor))
#    print 'Light sensor value: ' + light_val
    sound_val = str(grovepi.analogRead(sound_sensor))
#    print 'Sound sensor value: ' + sound_val
    dist_val = str(grovepi.ultrasonicRead(ultrasonic_ranger))
#    print 'Ultrasonic Ranger value: ' + dist_val

    # Compose JSON
    message = '{"luminance": ' + light_val + ', "volume": ' + sound_val + ', "distance": ' + dist_val + '}'

    # Publish
#    print 'Topic: ' + topic
#    print 'Mesage: ' + message
    client.publish(topic, message)

    sleep(0.2)

