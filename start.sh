#!/bin/bash
source /Users/mac/PycharmProjects/cctv_portpass
export FLASK_APP=/Users/mac/PycharmProjects/cctv_portpass/main.py
flask run -h 0.0.0.0 -p 5001  #--cert=cert.pem --key=priv_key.pem
