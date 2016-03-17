from flask import Flask, render_template, request, Response, abort
from Queue import Queue

from skynet.web import app
from skynet.web.server_sent_events import ServerSentEvent
from skynet.receive_server import SkynetReceiveManager
import json

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