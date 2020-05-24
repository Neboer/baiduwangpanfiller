from requests import Session
# from requests.cookies import cookiejar_from_dict, RequestsCookieJar
from http.cookiejar import MozillaCookieJar
from panapi.api import get_file_list, precreate_file, superfile2_file, create_file
from os import urandom
from json import load

# import sslkeylog
#
# sslkeylog.set_keylog("/home/neboer/ssl.log")
#
with open("secret.json") as secret_file:
    config = load(secret_file)
# sess = Session()

file_name = "/warning.expxddexpfhgdsd"

upload_id = precreate_file(config["cookie_pbc"], config["ua"], file_name, "/", config["bdstoken"])
print(upload_id)
# upload_id = "sdfsafdsdfas"
part_list = []
part_list.append(
    superfile2_file(config["cookie_cpbc"], config["ua"], urandom(0x400000), config["BDUSS"], file_name, upload_id, 0))
print("good")
part_list.append(
    superfile2_file(config["cookie_cpbc"], config["ua"], urandom(0x400000), config["BDUSS"], file_name, upload_id, 1))
part_list.append(
    superfile2_file(config["cookie_cpbc"], config["ua"], urandom(0x400000), config["BDUSS"], file_name, upload_id, 2))
create_file(config["cookie_pbc"], config["ua"], config["bdstoken"], part_list, upload_id, file_name, "/",
            0x400000 * len(part_list))

# ?order=time&desc=1&showempty=0&web=1&page=1&num=100&dir=%2Ftest&t=0.1025046789614934&channel=chunlei&web=1&app_id=250528&bdstoken=390b35fa7556994aa382d8b4ad2bd5cf&logid=MTU4OTk1Njc3MjE4NzAuMzI3ODUxNTE5NzY5NjkzMg==&clienttype=0&startLogTime=1589956772187
# ?order=time&desc=1&showempty=0&web=1&page=1&num=100&dir=%2Fgood&t=0.1025046789614934&channel=chunlei&web=1&app_id=250528&bdstoken=390b35fa7556994aa382d8b4ad2bd5cf&logid=MTU4OTk2MjA4MjY1NzYuNjAyMDAwMDAwMDAwMDAwMA==&clienttype=0&startLogTime=1589962082657
