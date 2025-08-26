

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
    print(token)
    
    # 添加购物车的数据
    cart_data = {
        "goods_id": "2",
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
    
    # 添加购物车的参数
    cart_params = {
        "application": "app",
        "application_client_type": "weixin",
        "token": token
    }
    
    # 这里应该使用添加购物车的URL，而不是登录URL
    cart_url = "http://shop-xo.hctestedu.com/index.php?s=api/cart/save"
    response = ak.post(url=cart_url, params=cart_params, json=cart_data)
    response = response.json()
    print(response)
