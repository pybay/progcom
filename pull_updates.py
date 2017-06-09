#!/usr/bin/env python
import os
from hashlib import sha1
from calendar import timegm
from datetime import datetime
import sys

import pytz
import requests
from raven import Client
from simplejson import JSONDecodeError
from requests.exceptions import RequestException

import logic as l

API_KEY = os.environ['PYCON_API_KEY']
API_SECRET = os.environ['PYCON_API_SECRET']
API_HOST = os.environ['PYCON_API_HOST']

PYBAY_API_TOKEN = "test"
API_TOKEN_PATH = '/home/pybay/api_token.txt'

if os.path.exists(API_TOKEN_PATH):
    with open(API_TOKEN_PATH) as f:
        token = f.read().strip()
        PYBAY_API_TOKEN = token


def api_call(api_suffix):
    return requests.get(
        "http://pybay.com/api/{}".format(api_suffix),
        params={'token': PYBAY_API_TOKEN},
    ).json()


def fetch_ids():
    raw = api_call('undecided_proposals')
    rv = [x['id'] for x in raw['data']]
    return list(set(rv + l.get_all_proposal_ids()))


def fetch_talk(id):
    rv = api_call('proposals/{}/'.format(id))
    if not rv or 'data' not in rv:
        return {}
    rv = rv['data']
    rv['authors'] = rv['speakers']
    del rv['speakers']
    rv.update(rv['details'])
    del rv['details']
    return rv

def main():
    for id in fetch_ids():
        #print 'FETCHING {}'.format(id)
        proposal = fetch_talk(id)
        if proposal:
            l.add_proposal(proposal)


if __name__ == '__main__':
    main()
