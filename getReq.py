import csv
import sys

import requests


# import json


def itunes_tracks():
    if len(sys.argv) < 2:
        sys.exit("lack of arguments for iTunes: limit or term should be provided")
    request_str = arg_splitter(sys.argv[1:])
    res = api_fetcher(request_str)
    with open('itunes_result.csv', 'a+', newline='') as file:
        header_values = ["artistName", "trackName", "releaseDate", "trackTimeMillis"]
        writer = csv.DictWriter(file, fieldnames=header_values)

        reader = csv.DictReader(file)
        for row in reader:
            if row != (','.join(header_values)):
                writer.writeheader()
            else:
                print('HEADER ISN\'T DETECTED')
                break

        for result in res['results']:
            try:
                writer.writerow(
                    {"artistName": result["artistName"], "trackName": result["trackName"],
                     "releaseDate": result["releaseDate"],
                     "trackTimeMillis": result["trackTimeMillis"]})
            except UnicodeEncodeError:
                sys.exit('encode error')


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
