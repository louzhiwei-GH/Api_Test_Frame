import requests
import allure
import jsonpath
import json
import pymysql
from deepdiff import DeepDiff

from config import *
import deepdiff

class ApiKey:
    @allure.step("发送get请求")
    def get(self, url, params=None, **kwargs):
        """
        发送get请求
        :param url: 请求的URL
        :param params: 查询参数
        :param kwargs: 其他 requests.get 支持的参数
        :return: requests.Response 对象
        """
        response = requests.get(url=url, params=params, **kwargs)
        return response
    
    @allure.step("发送post请求")
    def post(self, url, data=None, json=None, **kwargs):
        """
        发送post请求
        :param url: 请求的URL
        :param kwargs: 其他 requests.get 支持的参数
        :return: requests.Response 对象
        """
        response = requests.post(url=url, data=data, json=json, **kwargs)
        return response

    @allure.step("jsonpath提取数据")
    def get_value(self, data, key):
        """
        jsonpath提取数据
        : 数据远data
        : jsonpath 例如：$.msg
        jsonpath提取后的是一个列表
        """
        if key is None:
            return None
        if isinstance(data, str):
            data = json.loads(data)
        # jsonpath不能是json的字符串格式，需要通过json.loads()转化为python的字典或列表格式
        value = jsonpath.jsonpath(data, key)[0]
        return value

    @allure.step("提取数据库的值")
    def get_sql_data(self, sql_value):
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(sql_value)
        result = cursor.fetchone()
        cursor.close()
        return result[0]

    @allure.step("大量响应数据对比")
    def data_deepdiff(self, json1, json2, **other):
        """
        大量响应数据对比
        :param json1:
        :param json2:
        :param other:过滤条件
        :return:
        """
        res = DeepDiff(json1, json2, **other)
        if res == {}:
            return  True
        else:
            return False

