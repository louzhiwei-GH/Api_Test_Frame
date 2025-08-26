import logging
from Api_Keywork.Api_Key import ApiKey
import pytest
from config import *

@pytest.fixture(scope="session")
def get_token():
    ak = ApiKey()
    url = "http://shop-xo.hctestedu.com/index.php?s=api/user/login"
    public_data = PUBLIC_DATA
    data = {"accounts": USERNAME, "pwd": PASSWORD, "type": USERTYPE}
    res = ak.post(url=url, params=public_data, data=data)
    text = ak.get_value(res.json(), "$.msg")
    assert "登录成功" == text, "登录失败"
    token = ak.get_value(res.json(), "$..token")
    print(f"提取的token为: {token}")
    return token, ak

# 当执行一个case的时候会自动的调用这个方法
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    out = yield
    res = out.get_result()
    if res.when == "call":
        logging.info(f"用例ID: {res.nodeid}")
        logging.info(f"测试结果: {res.outcome}")
        logging.info(f"故障表示: {res.longrepr}")
        logging.info(f"异常: {call.excinfo}")
        logging.info(f"用例耗时: {res.duration}")
