#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree

NODE_PREFIX = '{http://beacon.nist.gov/record/0.1/}'
REST_URL = 'https://beacon.nist.gov/rest/record'

LAST_RECORD_URL = REST_URL + '/last'
CURRENT_RECORD_URL_TEMPLATE = REST_URL + '/{}'
NEXT_RECORD_URL_TEMPLATE = REST_URL + '/next/{}'


# Send requests to Beacon API and get responses
def get_response(url):
    response = urllib.request.urlopen(url)
    response_str = response.read().decode('utf-8')
    return xml.etree.ElementTree.fromstring(response_str)


def get_node_value(response, node_name):
    return response.find(NODE_PREFIX + node_name).text


# Retrieve specific nodes from Beacon API response
def get_record(response):
    return get_node_value(response, "outputValue")


def get_timestamp(response):
    return get_node_value(response, "timeStamp")


# Call specific Beacon API methods
def get_last_record():
    url = LAST_RECORD_URL
    response = get_response(url)
    return get_record(response)


def get_current_record(timestamp):
    url = CURRENT_RECORD_URL_TEMPLATE.format(timestamp)
    response = get_response(url)
    return get_record(response)


def get_next_response(timestamp):
    url = NEXT_RECORD_URL_TEMPLATE.format(timestamp)
    response = get_response(url)
    return response
