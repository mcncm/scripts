#!/bin/python

# mcncm 2019

import os
import sys
import requests

# TODO: replace this with a better way of getting my coordinates
coords_file = "coords.txt"
api_key_file = "api-key.txt"
script_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))

class Report:


    def __init__(self, api_response):
        self.api_response = api_response
        self.report = ''

    def add_icon(self):
        icon_base = self.api_response['icon'] + "-icon.txt"
        icon_path = os.path.join(script_dir, icon_base)
        try:
            with open(icon_path, 'r') as f:
                icon = f.read()
        except:
            icon = self.api_response['icon'] + '\n'
        self.report += icon

    def add_item(self, title, value, unit=""):
        self.report += title + ": \t" + str(self.api_response[value]) + unit + '\n'

    def issue_report(self):
        print(self.report)
        self.report = ''


def print_report(response):
    r = Report(response)
    r.add_icon()
    r.add_item('Summary', 'summary')
    r.add_item('Temperature', 'temperature', ' F')
    r.add_item('Precipitation', 'precipProbability', '%')
    r.issue_report()

def issue_request():
    api_key_path = os.path.join(script_dir, api_key_file)
    coords_key_path = os.path.join(script_dir, coords_file)
    with open(api_key_path, 'r') as f:
        api_key = f.read().rstrip()
    with open(coords_key_path, 'r') as f:
        coords = f.read().rstrip()
        print(coords)

    request_base = 'https://api.darksky.net/forecast/' + api_key + '/' + coords
    request_query = "?exclude=minutely,hourly,daily,alerts,flags"
    r = requests.get('https://api.darksky.net/forecast/' + api_key + '/' + coords)
    return r.json()['currently']

if __name__ == '__main__':
    response = issue_request()
    print_report(response)
