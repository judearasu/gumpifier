#!/usr/bin/python3
# -*- coding: utf-8 -*-

################################################################################
# Argon Design Ltd. Project P8010 Spock
# (c) Copyright 2018 Argon Design Ltd. All rights reserved.
#
# Module: Gumpifier
# Author : Patrick Taylor
################################################################################

"""
This CGI script takes the user tweaks to the suggested parameters, and returns a reference to the final, processed, image.
We do not parse the JSON here but pass it on directly to the server.

CGI args:
	JSON.	As specified in P8010-S-001.  User tweaked versions of original call to getScreen2Data.py.
			Keys: 'BG_segment_URLs', 'FG_cutout_URL', 'layer', 'position', 'scale'
CGI return:
	String.	URL reference to the final image.
"""

import os
import sys
from TF_interface import sendData
import traceback
import json

os.chdir("..")

# === Receive the data from the webpage === #
content_len = int(os.environ["CONTENT_LENGTH"]) # https://stackoverflow.com/questions/10718572/post-json-to-python-cgi
data = sys.stdin.read(content_len)

# === Send to the TF server === #
message = None
dataType = "application/json"

try:
	message = sendData(data, command='post')
	message = json.dumps(message)
except ConnectionAbortedError:
	message = json.dumps({"ERROR": "{}".format(traceback.format_exc())})
except ValueError:
	message = json.dumps({"ERROR": "{}".format(traceback.format_exc())})
except ConnectionRefusedError:
	message = json.dumps({"ERROR": "{}".format(traceback.format_exc())})

print("""Content-type: {}

{}""".format(dataType, message))