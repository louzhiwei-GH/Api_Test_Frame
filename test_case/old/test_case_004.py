from common.Md5_Encrypt import EncrypyDate
from Api_Keywork.Api_Key import ApiKey

key = "1234567812345678"
ak = ApiKey()
eg = EncrypyDate(key)

def test_encrypt_data():
    url = "http://127.0.0.1:8080/login_safe"
    headers = {"Contect-Type": "applicaiton/x-www-form-urlencoded"}
    name = eg.encrypt("tony")
    print(f"加密后的用户名为：{name}，用户名的格式为: {type(name)}")
    pw = eg.encrypt("123456")
    print(f"加密后的密码为：{pw}, 密码的格式为: {type(pw)}")
    data = {"username": name, "password": pw}
    res = ak.post(url=url, data=data, headers=headers)
    print(res.json())
