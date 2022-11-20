import csv
import sys


def main():
    if len(sys.argv) < 3:
        sys.exit("lack of arguments: the file name and key should be provided")
    sorted_list = get_list_sorted(get_file(sys.argv[1]), sys.argv[2])
    for line in sorted_list:
        print(line)


def get_list_sorted(payload, sign):
    try:
        return sorted(payload, key=lambda item: item[f'{sign}'])
    except KeyError:
        sys.exit(f'there is no such parameter as {sign}')


def get_file(name):
    data = []
    with open(name) as file:
        reader = csv.DictReader(file)
        for row in reader:
            track = {'artistName': row['artistName'], "trackName": row['trackName'], "releaseDate": row['releaseDate'],
                     "trackTimeMillis": row['trackTimeMillis']}
            data.append(track)
    return data


if __name__ == "__main__":
    main()
