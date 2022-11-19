def main():
    filename = input('filename:')
    mode = input('read (r) or write (w):')
    match mode:
        case 'w':
            while True:
                payload = input('payload:')
                if not write_line(filename, payload):
                    break
                if input('type x for exit:') == 'x':
                    break
        case 'r':
            res = read_file(filename)
            if len(res) > 0:
                for line in res:
                    print(line.rstrip())
            else:
                print('empty result')
        case _:
            print('unknown mode')


def write_line(file_name, payload):
    try:
        with open(file_name, 'a') as file:
            file.write(f'{payload}\n')
        return True
    except FileNotFoundError:
        print("FileNotFound")
        return False


def read_file(file_name):
    lines = []
    try:
        with open(file_name) as file:
            for line in file:
                lines.append(line.rstrip())
    except FileNotFoundError:
        lines.append(f'file {file_name} doesn\'t exist')
    return lines


if __name__ == '__main__':
    main()
