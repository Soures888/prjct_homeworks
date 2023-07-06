#!/bin/bash

# Adjust the permissions of the Docker socket
chmod 666 /var/run/docker.sock

# Start Telegraf
/usr/bin/telegraf