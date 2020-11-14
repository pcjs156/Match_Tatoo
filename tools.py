import json, sys
import os
from uuid import uuid4
from django.utils import timezone

#JSON 받아옴
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

# 파일을 저장할 디렉토리의 이름을 날짜 기반으로 정해줌
def date_upload_to(instance, filename):
    dir_path = instance.__class__.__name__
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return '/'.join([dir_path, ymd_path, uuid_name + extension])

# code, value 쌍을 요소로 갖는 tuple을 딕셔너리로 변환
def parse_dict_from_code_pair(pairs: tuple):
    return {pair[0]:pair[1] for pair in pairs}

# key와 value가 바뀐 dictionary를 return
def reversed_dict(d: dict):
    return {value:key for key, value in d.items()}
