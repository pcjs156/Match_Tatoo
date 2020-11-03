import json, sys

def json_to_dict(filename: str, *keys):
    try:
        ret = dict()
        with open(filename) as f:
            json_file = json.loads(f.read())

    except FileNotFoundError as e:
        print(e)
        print(f"{filename}이 디렉토리에 존재하지 않습니다.")
        sys.exit()

    for key in keys:
        try:
            ret[key] = json_file[key]
        except KeyError:
            print(f"{key}는 {filename}에 존재하지 않는 key입니다.")
            sys.exit()

    return ret