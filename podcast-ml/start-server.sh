#!/bin/bash
export $(cat /etc/secret-volume/.env | xargs)
python run.py
