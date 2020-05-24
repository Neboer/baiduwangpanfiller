from urllib.parse import quote_plus
from time import time
from base64 import b64encode
from random import choice
from string import ascii_letters, digits
from json import dumps, loads
from requests import get, post


def generate_logid():
    return b64encode(str(time() * 10000).ljust(31, '0').encode('ascii')).decode('ascii')


def get_attribute(request, attr, name):
    if request.status_code == 200:
        result_obj = loads(request.text)
        if "errno" not in result_obj or result_obj["errno"] == 0:
            return result_obj[attr]
        else:
            print(f"{name} error {request.text}")
            raise Exception
    else:
        print(f"HTTP {name} error {request.text}")
        raise Exception


def get_file_list(cookie_pbc, ua, bdstoken, path, order="time", page=1, num=100, desc=True):
    url = "https://pan.baidu.com/api/list"
    paramt = f"?order={order}&" \
             f"desc={int(desc)}&" \
             "showempty=0&" \
             "web=1&" \
             f"page={page}&" \
             f"num={num}&" \
             f"dir={quote_plus(path)}&" \
             "t=0.1025046789614934&" \
             "channel=chunlei&" \
             "web=1&" \
             "app_id=250528&" \
             f"bdstoken={bdstoken}&" \
             f"logid={generate_logid()}&" \
             "clienttype=0&" \
             f"startLogTime={int(time() * 1000)}"
    # print(paramt)
    headers = {"Cookie": cookie_pbc, "User-Agent": ua}
    get(url + paramt, headers=headers)


# if successful, return upload id
def precreate_file(cookie_pbc, ua, filename, target_path, bdstoken):
    url = "https://pan.baidu.com/api/precreate"
    paramt = "?channel=chunlei&" \
             f"web=1&" \
             f"app_id=250528&" \
             f"bdstoken={bdstoken}&" \
             f"logid={generate_logid()}&" \
             f"clienttype=0&" \
             f"startLogTime={int(time() * 1000)}"
    form_data = f"path={quote_plus(filename)}&" \
                f"autoinit=1&" \
                f"target_path={quote_plus(target_path)}&" \
                "block_list=%5B%225910a591dd8fc18c32a8f3df4fdc1761%22%2C%22a5fc157d78e6ad1c7e114b056c92821e%22%5D&" \
                f"local_mtime={int(time())}"
    headers = {"Cookie": cookie_pbc, "User-Agent": ua}

    result = post(url + paramt, headers=headers, data=form_data)
    return get_attribute(result, "uploadid", "precreate")


def randomString(stringLength=16):
    letters = ascii_letters + digits
    return ''.join(choice(letters) for i in range(stringLength))


class FakeFile():
    name = 'blob'

    def __init__(self, data):
        self.content = data

    def read(self):
        return self.content


def superfile2_file(cookie_cpbc, ua, data, BDUSS, file_path, upload_id, part_sequence):
    url = "https://c3.pcs.baidu.com/rest/2.0/pcs/superfile2"
    # url = "http://localhost:8000/rest/2.0/pcs/superfile2"
    paramt = "?method=upload&" \
             "app_id=250528&" \
             "channel=chunlei&" \
             "clienttype=0&" \
             "web=1&" \
             f"BDUSS={BDUSS}&" \
             f"logid={generate_logid()}&" \
             f"path={quote_plus(file_path)}&" \
             f"uploadid={upload_id}&" \
             "uploadsign=0&" \
             f"partseq={part_sequence}"
    extra_headers = {
        "Origin": "https://pan.baidu.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://pan.baidu.com/disk/home?"
    }
    headers = {"Cookie": cookie_cpbc, "User-Agent": ua}
    extra_headers.update(headers)
    result = post(url + paramt, headers=extra_headers,
                  files={'file': ('blob', FakeFile(data), 'application/octet-stream')})
    return get_attribute(result, "md5", "superfile2")


def create_file(cookie_pbc, ua, bdstoken, block_list, upload_id, file_path, target_path, file_size):
    url = "https://pan.baidu.com/api/create"
    paramt = "isdir=0&" \
             f"rtype=1&" \
             f"channel=chunlei&" \
             f"web=1&" \
             f"app_id=250528&" \
             f"bdstoken={bdstoken}&" \
             f"logid={generate_logid()}&" \
             f"clienttype=0"

    post_data = f"path={quote_plus(file_path)}&" \
                f"size={file_size}&" \
                f"uploadid={quote_plus(upload_id)}&" \
                f"target_path={quote_plus(target_path)}&" \
                f"block_list={quote_plus(dumps(block_list))}&" \
                f"local_mtime={int(time())}"
    headers = {"Cookie": cookie_pbc, "User-Agent": ua}

    result = post(url + paramt, headers=headers, data=post_data)
    return get_attribute(result, "errno", "superfile2")
