import json
import sys


def parse_audit():
    if len(sys.argv) < 2:
        sys.exit("lack of arguments for parse: filename must be provided")
    source = arg_processor(sys.argv[1:])
    try:
        print(f'start parsing {source}')
        with open(source, 'r', encoding="utf-16") as in_, open('14_1_1.txt', 'w+') as out_:
            report = []
            for line in in_:
                entry = json.loads(line)
                if entry["type"] == "auditAdvisory":
                    new_entry = (f'. Package: {entry["data"]["advisory"]["module_name"]}, '
                                 f'version: {entry["data"]["advisory"]["findings"][0]["version"]}, '
                                 f'path: {entry["data"]["advisory"]["findings"][0]["paths"][0]} || '
                                 f'Title: {entry["data"]["advisory"]["title"]} || '
                                 f'CVSS score: {entry["data"]["advisory"]["cvss"]["score"]} || '
                                 f'Patched versions: {entry["data"]["advisory"]["patched_versions"]} || '
                                 f'Recommendation: {entry["data"]["advisory"]["recommendation"]} || '
                                 f'URL: {entry["data"]["advisory"]["url"]} \n')
                    if new_entry not in report:
                        report.append(new_entry)
            # here must be filter logic
            for idx, line in enumerate(report):
                out_.write(f'{idx + 1}{line}')
            print(f'Parsing {source} completed')

    except FileNotFoundError:
        sys.exit(f"file {source} doesn't exist")
    except json.decoder.JSONDecodeError as err:
        sys.exit(f'error parsing json: {err}')


def json_preparer(arg):
    filewrite = open('out.json', 'w+')

    with open(arg, 'r') as jsonFile:
        for jf in jsonFile:
            jf = jf.replace('\n', '')
            jf = jf.strip()
            filewrite.write(jf)

    filewrite.close()


def arg_processor(args):
    filename = '1'
    for arg in args:
        el = arg.split('=')
        match el[0]:
            case 'filename':
                filename = el[1]
            case _:
                break
    return f'{filename}.json'


if __name__ == '__main__':
    parse_audit()
