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

def run():

    from log_influxdb import InfluxDBLogger
    from influxdb_connection import InfluxDBConnection
    from receive_server import SkynetReceiveManager
    

    db = InfluxDBConnection()
    SkynetReceiveManager.init()
    logger = InfluxDBLogger(db)

    SkynetReceiveManager.srv.add_handler(logger.handler)

    # TODO: make cntl-c work!
    logger.start()

    from .web import app

    app.run(threaded=True, port=5001)

    if SkynetReceiveManager.srv is not None:
        SkynetReceiveManager.srv.stop()

    logger.stop()

  
