import sys

import requests

from file_interface import write_line


# import json


def itunes_tracks():
    if len(sys.argv) < 2:
        sys.exit("lack of arguments for iTunes: limit or term should be provided")
    request_str = arg_splitter(sys.argv[1:])
    res = api_fetcher(request_str)
    # print(json.dumps(res, indent=2))
    for result in res['results']:
        print(result['trackName'])
        write_line('itunes_result.txt', result['trackName'])


def arg_splitter(args):
    count = '1'
    term = 'all'
    for arg in args:
        el = arg.split('=')
        match el[0]:
            case 'count':
                count = el[1]
            case 'term':
                term = el[1]
            case _:
                break
    return f'https://itunes.apple.com/search?limit={count}&term={term}'


def api_fetcher(req):
    response = requests.get(req)
    return response.json()


if __name__ == '__main__':
    itunes_tracks()
