# Copyright (c) 2016, Jonathan Nutzmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from influxdb import InfluxDBClient
from strict_rfc3339 import rfc3339_to_timestamp


class InfluxDBConnection:

    def __init__(self, server="localhost", port=8086, user='root', password='root', database='skynet_lite'):

        print "Connecting to Influx: %s@%s:%s/%s" % (user, server, port, database)

        self.client = InfluxDBClient(server, port, user, password, database)
        dbs = [x['name'] for x in self.client.get_list_database()]
        if database not in dbs:
            self.client.create_database(database)

    def write_points(self, points):
        self.client.write_points(points)

