def run():

    from log_influxdb import InfluxDBLogger
    from server_sent_events import ServerSentEvent
    from influxdb_connection import InfluxDBConnection
    from receive_server import SkynetReceiveManager
    

    db = InfluxDBConnection()
    SkynetReceiveManager.init()
    logger = InfluxDBLogger(db)

    SkynetReceiveManager.srv.add_handler(logger.handler)

    # TODO: make cntl-c work!
    logger.start()

    from .web import app

    app.run(threaded=True)

    if SkynetReceiveManager.srv is not None:
        SkynetReceiveManager.srv.stop()

    logger.stop()

  
