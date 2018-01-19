ROOT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

run:
	APP_CONFIG=${ROOT_DIR}/config-production.txt run.py

install:
	curl \
	    --silent \
	    --output strava_map/static/Polyline.encoded.js \
	    https://raw.githubusercontent.com/jieter/Leaflet.encoded/master/Polyline.encoded.js 
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

lint:
	flake8 \
	    --exclude strava_app/static/external \
	    run.py strava_map
