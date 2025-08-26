"""
    添加收货地址
"""


from Api_Keywork import ApiKey
import jsonpath

ak = ApiKey()

def test_case_001():
    url = "http://shop-xo.hctestedu.com/index.php?s=api/user/login"
    public_data = {"application": "app", "applicaiton_client_type": "weixin"}
    data = {"accounts": "17803002428", "pwd": "123456", "type": "username"}
    response = ak.post(url=url, params=public_data, json=data)
    response = response.json()
    SJDATA = jsonpath.jsonpath(response, "$.msg")[0]
    EXdata = "登录成功"
    assert SJDATA == EXdata, "登录失败，返回信息：{}".format(SJDATA)
    print("登录成功，返回信息：{}".format(SJDATA))
    token = jsonpath.jsonpath(response, "$.data.token")[0]
    
    # 添加购物车的数据
    cart_data = {
        "address": "浦江科技广场",
        "alias": "单位",
        "city": "152",
        "county": "1896",
        "id": 0,
        "idcard_back": "https://xxx/1633946364142699.png",
        "idcard_front": "https://xxx/1633946357974689.png",
        "idcard_name": "张飞",
        "idcard_number": "522228666655556666",
        "is_default": 1,
        "lat": 31.11889286405114,
        "lng": 121.38867189063298,
        "name": "龚哥哥",
        "province": "9",
        "tel": "13222223333"
}
    
    # 添加购物车的参数  
    cart_params = {
        "application": "app",
        "application_client_type": "weixin",
        "token": token
    }
    
    # 这里应该使用添加购物车的URL，而不是登录URL
    cart_url = "http://shop-xo.hctestedu.com/index.php?s=api/useraddress/save"
    response = ak.post(url=cart_url, params=cart_params, json=cart_data)
    response = response.json()
    msg = jsonpath.jsonpath(response, "$.msg")
    print(msg)
    assert "新增成功" == response["msg"], "添加地址失败,msg: {}".format(msg)
