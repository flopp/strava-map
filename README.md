[![Build Status](https://travis-ci.org/flopp/strava-map.svg?branch=master)](https://travis-ci.org/flopp/strava-map)

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

# edit config-example.txt; fill in your Strava API credentials (from https://www.strava.com/settings/api)
...

# run
make run
```

## License
Copyright 2018 Florian Pigorsch & Contributors. All rights reserved.

Use of this source code is governed by a MIT-style license that can be found in the [LICENSE](https://github.com/flopp/strava-map/blob/master/LICENSE) file.
