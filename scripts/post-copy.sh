#!/bin/bash

cd ~/projects/strava-map/

mkdir -p ~/html/strava-map/
cp ./scripts/.htaccess ~/html/strava-map/

mkdir -p ~/fcgi-bin/
cp ./scripts/strava-map.fcgi ~/fcgi-bin/

./scripts/kill-server.sh

virtualenv -p python3 ENV
PATH=./ENV/bin:$PATH make install
