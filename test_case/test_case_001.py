from Api_Keywork.Api_Key import ApiKey
import allure
from config import *

@allure.title("测试用例：加入购物车")
def test_login(get_token):
    token, ak = get_token
    url = "http://shop-xo.hctestedu.com/index.php?s=api/cart/save"
    public_data = {"application": "app", "applicaiton_client_type": "weixin", "token": token}
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
    res = ak.post(url=url, params=public_data, data=cart_data)
    text = ak.get_value(res.json(), "$.msg")
    assert "加入成功" == text, "加入购物车失败！"
   