import json
import os
import subprocess
import sys

from packaging import version


class Package:
    def __init__(self, module_name="", patched_versions="", description=""):
        self.module_name = module_name
        self.patched_versions = patched_versions
        self.description = description

    def __str__(self):
        return f"{self.module_name}({self.patched_versions})"


def get_yarn_result(arg):
    print('yarn audit initiated')
    command = f"yarn audit --groups dependencies --json > {arg}"
    subprocess.run(command, shell=True, text=False, capture_output=False)
    print('yarn audit succeeded')


def get_npm_result(arg):
    print('npm audit started')
    command = f"npm audit --omit=dev --json > {arg}"
    subprocess.run(command, shell=True, text=False, capture_output=False)
    print('npm audit succeeded')


def cleanup(arg):
    os.remove(arg)


def parse_audit():
    source = 'temp.json'
    output = '14_1_1.txt'
    report = dict()
    try:
        print(f'start parsing', "\n", '========================')

        get_npm_result(source)
        with open(source, 'r', encoding="utf-8") as in_:
            for entry in in_:
                source_line = json.loads(entry)
                if source_line["type"] == "auditAdvisory":

                    # get the package and patched version
                    pack_name = source_line["data"]["advisory"]["module_name"]
                    package = Package(pack_name,
                                      source_line["data"]["advisory"]["patched_versions"].strip(">="),
                                      f'. Package: {pack_name}, '
                                      f'Version: {source_line["data"]["advisory"]["findings"][0]["version"]}, '
                                      f'Dependency of: '
                                      f'{source_line["data"]["advisory"]["findings"][0]["paths"][0].split(">")[0]} || '
                                      f'Patched versions: {source_line["data"]["advisory"]["patched_versions"]}'
                                      f'\n')

                    report_line = report.get(pack_name)
                    if report_line:
                        if version.parse(report_line.patched_versions) < version.parse(package.patched_versions):
                            print("for", report_line, 'package higher version', package, "founded")
                            report_line.patched_versions = package.patched_versions
                            report_line.description = package.description
                    else:
                        print('vulnerable package found:', package)
                        report[pack_name] = package
        cleanup(source)

        get_yarn_result(source)
        with open(source, 'r', encoding="utf-8") as in_:
            for entry in in_:
                source_line = json.loads(entry)
                if source_line["type"] == "auditAdvisory":

                    # get the package and patched version
                    pack_name = source_line["data"]["advisory"]["module_name"]
                    package = Package(pack_name,
                                      source_line["data"]["advisory"]["patched_versions"].strip(">="),
                                      f'. Package: {pack_name}, '
                                      f'Version: {source_line["data"]["advisory"]["findings"][0]["version"]}, '
                                      f'Dependency of: '
                                      f'{source_line["data"]["advisory"]["findings"][0]["paths"][0].split(">")[0]} || '
                                      f'Patched versions: {source_line["data"]["advisory"]["patched_versions"]}'
                                      f'\n')

                    report_line = report.get(pack_name)
                    if report_line:
                        if version.parse(report_line.patched_versions) < version.parse(package.patched_versions):
                            print("for", report_line, 'package higher version', package, "founded")
                            report_line.patched_versions = package.patched_versions
                            report_line.description = package.description
                    else:
                        print('vulnerable package found:', package)
                        report[pack_name] = package
        cleanup(source)

    except FileNotFoundError:
        sys.exit(f"file {source} doesn't exist")
    except UnicodeError as err:
        sys.exit(f"{err}")
    except PermissionError as err:
        sys.exit(f"{err}")
    except json.decoder.JSONDecodeError as err:
        sys.exit(f'error parsing json: {err}')

    # put the report in the output
    with open(output, 'w+') as out_:
        for idx, line in enumerate(report.values()):
            out_.write(f'{idx + 1}{line.description}')
    print('========================', "\n", f'Parsing completed. {len(report)} entries filed in {output}')


# call protector
if __name__ == '__main__':
    parse_audit()
