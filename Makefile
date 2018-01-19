ROOT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

run:
	APP_CONFIG=${ROOT_DIR}/config-production.txt ENV/bin/python run.py

install:
	virtualenv -p python3 ENV
	curl \
		--silent \
		--output strava_map/static/Polyline.encoded.js \
		https://raw.githubusercontent.com/jieter/Leaflet.encoded/master/Polyline.encoded.js 
	ENV/bin/pip install -r requirements.txt
