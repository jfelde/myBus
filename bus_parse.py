#!/usr/bin/env python

"""
Scrape bus statuses
"""

import requests
from bs4 import BeautifulSoup

base_url = 'http://pugetsound.onebusaway.org/where/standard/stop.action?id=1_'
stops = ['Greenwood', 'Aurora Ave', '3rd & Virginia']
stop_dict = {'Greenwood':str(5790),
         'Aurora Ave':str(7160),
         '3rd & Virginia':str(600)}
lines = ['5', '5E', 'E Line']

for stop in stops:
    print stop
    line = ''
    for i in range(len(stop)):
        line += '-'
    print line
    r = requests.get(base_url+stop_dict[stop])
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', attrs={'class':'arrivalsTable'})
    rows = table.findAll('tr', attrs={'class':'arrivalsRow'})
    for row in rows:
        route = row.find('td', attrs={'class':'arrivalsRouteEntry'})
        route = route.get_text()
        desc = row.find('td', attrs={'class':'arrivalsDescriptionEntry'})
        dest = desc.find('div', attrs={'class':'arrivalsDestinationEntry'})
        dest = dest.get_text()
        dest = dest.replace('Seattle', '')
        dest = dest.replace('Greenwood', '- Greenwood')
        dest = dest.replace(' Transit Center', '')
        time = desc.find('div', attrs={'class':'arrivalsTimePanel'})
        time = time.get_text()
        time = time.replace('departure', '')
        mins = row.find('td', attrs={'class':'arrivalsStatusEntry'})
        mins = mins.get_text()
        if route in lines:
            print '{0:<8} {1:<25} {2:<5} {3:<}'.format(route,dest,mins,time)
    print '\n'