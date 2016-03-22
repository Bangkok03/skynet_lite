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

from flask import Flask, render_template, request, Response, abort
from Queue import Queue
from skynet.receive_server import SkynetReceiveManager
from skynet.web import app
from skynet.web.server_sent_events import ServerSentEvent


@app.route('/stream/<filter>')
def stream(filter):

    q = Queue()

    def handler(name, timestamp_seconds, source, value):
        if filter == '*' or filter in name:
            o = {
                "name": name,
                "timestamp": timestamp_seconds,
                "source": source,
                "value": value
            }

            q.put(o)

    def gen():
        SkynetReceiveManager.srv.add_handler(handler)
        try:
            while True:
                r = q.get()
                ev = ServerSentEvent(json.dumps(r))
                yield ev.encode()
        except:
            print('removing handler')
            SkynetReceiveManager.srv.remove_handler(handler)

    return Response(gen(), mimetype="text/event-stream")

@app.route('/live')
def live():

    return render_template('default.html')