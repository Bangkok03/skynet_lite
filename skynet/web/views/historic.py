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

from flask import Flask, render_template, request, Response, abort

from skynet.web import app


# Non-functional: 'difference', 'floor', 'histogram', 'celing'
aggregators = ['count', 'distinct', 'integral', 'mean', 'median', 'spread', 'sum', 'bottom',
                'first', 'last', 'max', 'min', 'percentile', 'top', 'derivative',
                'non_negative_derivative', 'stddev']


@app.route('/db/query')
def db_query():

    aggregator = request.args.get('a')
    field = request.args.get('d')
    packet = request.args.get('p')
    time = request.args.get('t')
    group = request.args.get('g')
    fill = request.args.get('f')
    board = request.args.get('b')
    name = request.args.get('n')

    query = "SELECT "

    if aggregator:
        query += aggregator.upper() + '("%s") ' % field
    else:
        query += " %s " % field

    query += 'FROM %s WHERE %s ' % (packet, time)

    if board:
        query += "AND \"board\"='%s' " % board

    if name:
        query += "AND \"name\"='%s' " % name

    if group:
        query += "GROUP BY %s " % group

        if fill:
            query += 'FILL(%s)' % fill

    print(query)
    results = db.get_results_for_plot(query)
    return json.dumps(results)

@app.route('/visualizer')
def logalyzer_view():
    meas = db.get_measurements()
    return render_template('visualizer.html', measurements=json.dumps(meas))