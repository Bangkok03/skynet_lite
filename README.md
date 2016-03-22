# Introduction
This project is a generic data visualization and logging package.  It is meant for real time system debugging.

This software is currently set up to push into a local instance of [InfluxDB](https://influxdata.com/time-series-platform/influxdb/) time series database, as well as a live web client located at http://localhost:5001/live.

I also highly reccomend using [Grafana](http://grafana.org/) for live and post visualization.


# Installation

The following script will clone this repository, as well as install:
* **[flask](http://flask.pocoo.org/)** - A Python web framework
* **[influxdb](https://influxdata.com/time-series-platform/influxdb/)** - time series database for logging
* **[grafana](http://grafana.org/)** - data front end for influxdb

```shell
git clone https://github.com/jnutzmann/skynet_lite
sudo pip install flask
wget https://s3.amazonaws.com/influxdb/influxdb_0.10.3-1_amd64.deb
sudo dpkg -i influxdb_0.10.3-1_amd64.deb
rm influxdb_0.10.3-1_amd64.deb
sudo service influxdb start

wget https://grafanarel.s3.amazonaws.com/builds/grafana_2.6.0_amd64.deb
sudo dpkg -i grafana_2.6.0_amd64.deb
rm grafana_2.6.0_amd64.deb
sudo service grafana-server start
```

# Use

Once the repository is cloned and the influxdb service has been started (see above script), run the skynet server by running `./skynet_lite` in the root of the repository.

Pushing data into Skynet Lite is easy!  Simply send a UDP packet to `http://localhost:5002` with a JSON payload with the following form:

```json
{
	"src": "testsrc",
	"data": [
		{
			"name": "my.data.name",
			"time": 1458626312,
			"val": 42.42
		},
		{
			"name": "my.data.name2",
			"time": 1458626313,
			"val": 123
		}
	]
}

```

Total size of the serialized message must be less than 8192 bytes.