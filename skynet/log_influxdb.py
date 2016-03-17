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

import json
import time
from threading import Thread
from Queue import Queue


class InfluxDBLogger(Thread):

    def __init__(self, db):

        print "init logger"
        
        Thread.__init__(self)
        
        self.q = Queue()
        self.db = db

        def log(name, timestamp_seconds, source, value):
            
            point = {
                "measurement": name,
                "time": int(timestamp_seconds*1e9),
                "tags": {
                    "source": source,
                },
                "fields": {"value": value}
            }
            print(point)
            self.q.put(point)

        self.handler = log
        self.running = False

    def stop(self):
        self.running = False

    def run(self):
        self.running = True

        try:
            while self.running:
                points = []
                time.sleep(1)  # wait for more points (only make influx call 1/sec)
                
                p = self.q.get(timeout=1)
                if p is not None:
                    points.append(p)
                
                while not self.q.empty():
                    points.append(self.q.get())
                
                try:
                    self.db.write_points(points)
                except Exception as e:
                    print(e)
                
                print(len(points))

        except Exception as e:
            print(e)
