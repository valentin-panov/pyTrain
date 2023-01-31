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
            for entry in in_:
                source_line = json.loads(entry)
                if source_line["type"] == "auditAdvisory":
                    # get the package and patched
                    report.append([source_line["data"]["advisory"]["module_name"],
                                   source_line["data"]["advisory"]["patched_versions"].strip(">="),
                                   f'. Package: {source_line["data"]["advisory"]["module_name"]}, '
                                   f'Version: {source_line["data"]["advisory"]["findings"][0]["version"]}, '
                                   f'Dependency of: '
                                   f'{source_line["data"]["advisory"]["findings"][0]["paths"][0].split(">")[0]} || '
                                   # f'Title: {entry["data"]["advisory"]["title"]} || '
                                   # f'CVSS score: {entry["data"]["advisory"]["cvss"]["score"]} || '
                                   f'Patched versions: {source_line["data"]["advisory"]["patched_versions"]} || '
                                   # f'Recommendation: {source_line["data"]["advisory"]["recommendation"]} || '
                                   # f'URL: {entry["data"]["advisory"]["url"]} '
                                   f'\n'])

            # go over the array and sort it
            # for item in report:
            #     print(item[1], "<=", new_report_line[1], (item[1] <= new_report_line[1]))
            #     if (item[0] == new_report_line[0]) & (item[1] <= new_report_line[1]):
            #         print('HAVE', item[0], item[1])
            #     else:
            #         add_entry(report, source_line, new_report_line)

            # put the report in the output
            for idx, line in enumerate(report):
                out_.write(f'{idx + 1}{line[2]}')
            print(f'Parsing {source} completed. {len(report)} entries filed')

    except FileNotFoundError:
        sys.exit(f"file {source} doesn't exist")
    except json.decoder.JSONDecodeError as err:
        sys.exit(f'error parsing json: {err}')


# def add_entry(arr, source_line, new_report_line):
#     # create the report message and append it to the report line
#
#     # append the new line to the report
#     arr.append(new_report_line)
#     return arr


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
