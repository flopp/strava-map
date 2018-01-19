run:
	APP_CONFIG=config-production.txt ENV/bin/python app.py

install:
	virtualenv -p python3 ENV
	curl \
		--silent \
		--output static/Polyline.encoded.js \
		https://raw.githubusercontent.com/jieter/Leaflet.encoded/master/Polyline.encoded.js 
	ENV/bin/pip install -r requirements.txt
