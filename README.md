[![Build Status](https://travis-ci.org/flopp/strava-map.svg?branch=master)](https://travis-ci.org/flopp/strava-map)
[![License MIT](https://img.shields.io/badge/license-MIT-lightgrey.svg?style=flat)](https://github.com/flopp/strava-map/blob/master/LICENSE)

# Strava Map
A map of your Strava activities. Based on Python/Flask.

## Install
```
# create virtual env
virtualenv -p python3 ENV

# activate virtual env
source ENV/bin/activate

# get PIP packages and Polyline.encoded.js
make install

# create config.py; use config_example.py as a template; fill in your Strava API credentials (from https://www.strava.com/settings/api)
...

# run
make run
```

## License
Copyright 2018 Florian Pigorsch & Contributors. All rights reserved.

Use of this source code is governed by a MIT-style license that can be found in the [LICENSE](https://github.com/flopp/strava-map/blob/master/LICENSE) file.
