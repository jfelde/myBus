#!/usr/bin/env python

"""
Scrape bus statuses
"""

import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask, render_template, Markup

testing = False

app = Flask(__name__, static_folder=os.path.join(os.getcwd(),'static'))

@app.route('/')
@app.route('/index')
def index():
    """
    Scrape the current bus info and deliver the data to the template
    """
    base_url = 'http://pugetsound.onebusaway.org/where/standard/stop.action?id=1_'
    stops = ['Greenwood', 'Aurora Ave', '3rd & Virginia']
    if datetime.now().hour > 12:
        stops.reverse()
    stop_dict = {'Greenwood':str(5790),
                 'Aurora Ave':str(7160),
                 '3rd & Virginia':str(600)}
    lines = ['5', '5E', 'E Line']
    curtime = datetime.now().strftime('%I-%M')
    data = []
    for stop in stops:
        r = requests.get(base_url+stop_dict[stop])
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table', attrs={'class':'arrivalsTable'})
        rows = table.findAll('tr', attrs={'class':'arrivalsRow'})
        first_row = True
        for row in rows:
            line = row.find('td', attrs={'class':'arrivalsRouteEntry'})
            line = line.get_text()
            desc = row.find('td', attrs={'class':'arrivalsDescriptionEntry'})
            time = desc.find('div', attrs={'class':'arrivalsTimePanel'})
            time = time.get_text()
            time = time.replace('departure', '')
            mins = row.find('td', attrs={'class':'arrivalsStatusEntry'})
            mins = mins.get_text()
            if line in lines and (mins=='NOW' or int(mins) <= 15):
                if first_row:
                    data.append([stop, line, mins, time])
                    first_row = False
                else:
                    data.append(['', line, mins, time])
    if testing:
        return [curtime, data]
    else:
        return render_template('myBus.html', curtime=curtime, data=data)

if __name__ == '__main__':
    if testing:
        print index()
    else:
        app.run()