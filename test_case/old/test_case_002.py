"""
    浏览商品-直接提交订单
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
    assert SJDATA == EXdata, "登录失败， 返回信息：{}".format(SJDATA)
    print("登录成功，返回信息：{}".format(SJDATA))
    token = jsonpath.jsonpath(response, "$.data.token")[0]
    print(token)
    
    # 订单确认的数据
    cart_data = {
        "buy_type": "goods",
        "goods_id": "2",
        "address_id": 0,
        "payment_id": 0,
        "site_model": 0,
        "is_points": 0,
        "spec": [
            {
                "type": "套餐",
                "value": "套餐二"
            },
             {
                "type": "颜色",
                "value": "银色"
            },
             {
                "type": "容量",
                "value": "64G"
            }
        ],
        "stock": 2
    }
    
    # 直接提价订单的数据
    cart_params = {
        "application": "app",
        "application_client_type": "weixin",
        "token": token
    }
    
    # 这里应该使用添加购物车的URL，而不是登录URL
    cart_url = "http://shop-xo.hctestedu.com/index.php?s=api/buy/index"
    response = ak.post(url=cart_url, params=cart_params, json=cart_data)
    response = response.json()
    print(response)
