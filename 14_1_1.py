import json
import sys

from packaging import version


class Package:
    def __init__(self, module_name="", patched_versions="", description=""):
        self.module_name = module_name
        self.patched_versions = patched_versions
        self.description = description

    def __str__(self):
        return f"{self.module_name}({self.patched_versions})"


def parse_audit():
    if len(sys.argv) < 2:
        sys.exit("lack of arguments for parse: filename must be provided")
    source = arg_processor(sys.argv[1:])
    try:
        print(f'start parsing {source}')
        print('========================')
        with open(source, 'r', encoding="utf-16") as in_, open('14_1_1.txt', 'w+') as out_:
            report = dict()
            for entry in in_:
                source_line = json.loads(entry)
                if source_line["type"] == "auditAdvisory":
                    # get the package and patched
                    pack_name = source_line["data"]["advisory"]["module_name"]
                    package = Package(source_line["data"]["advisory"]["module_name"],
                                      source_line["data"]["advisory"]["patched_versions"].strip(">="),
                                      f'. Package: {source_line["data"]["advisory"]["module_name"]}, '
                                      f'Version: {source_line["data"]["advisory"]["findings"][0]["version"]}, '
                                      f'Dependency of: '
                                      f'{source_line["data"]["advisory"]["findings"][0]["paths"][0].split(">")[0]} || '
                                      f'Patched versions: {source_line["data"]["advisory"]["patched_versions"]}'
                                      f'\n')
                    report_line = report.get(pack_name)

                    if report_line:
                        print("for", report_line, 'same package found', package)
                        if version.parse(report_line.patched_versions) < version.parse(package.patched_versions):
                            print(package, "higher versions found")
                            report_line.patched_versions = package.patched_versions
                            report_line.description = package.description
                    else:
                        print('new package found, append', package)
                        report[pack_name] = package

            # put the report in the output
            for idx, line in enumerate(report.values()):
                out_.write(f'{idx + 1}{line.description}')
            print('========================')
            print(f'Parsing {source} completed. {len(report)} entries filed')

    except FileNotFoundError:
        sys.exit(f"file {source} doesn't exist")
    except json.decoder.JSONDecodeError as err:
        sys.exit(f'error parsing json: {err}')


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


# trash stack
def json_preparer(arg):
    filewrite = open('out.json', 'w+')

    with open(arg, 'r') as jsonFile:
        for jf in jsonFile:
            jf = jf.replace('\n', '')
            jf = jf.strip()
            filewrite.write(jf)

    filewrite.close()


# call protector
if __name__ == '__main__':
    parse_audit()
