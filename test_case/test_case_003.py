# -*- coding: utf-8 -*-
# @Time : 2023/11/8 20:55
# @Author : Hami
import json
import pytest
from common.FileDataDriver import FileReader
from Api_Keywork.Api_Key import ApiKey
from config import *
import allure


class TestCase:
    # 获取对应的数据 CaseData 需要从文档当中去进行读取
    # 1. 获取数据(四要素) 2. 发送请求 3.获取响应数据 4.断言
    AllCaseData = FileReader.read_excel()
    ak = ApiKey()



    def __dynamic_title(self, CaseData):
        # # 动态生成标题
        # allure.dynamic.title(data[11])

        # 如果存在自定义标题
        if CaseData["caseName"] is not None:
            # 动态生成标题
            allure.dynamic.title(CaseData["caseName"])

        if CaseData["storyName"] is not None:
            # 动态获取story模块名
            allure.dynamic.story(CaseData["storyName"])

        if CaseData["featureName"] is not None:
            # 动态获取feature模块名
            allure.dynamic.feature(CaseData["featureName"])

        if CaseData["remark"] is not None:
            # 动态获取备注信息
            allure.dynamic.description(CaseData["remark"])

        if CaseData["rank"] is not None:
            # 动态获取级别信息(blocker、critical、normal、minor、trivial)
            allure.dynamic.severity(CaseData["rank"])

    @pytest.mark.parametrize("CaseData", AllCaseData)
    def testCase(self, CaseData):
        self.__dynamic_title(CaseData)

        # 写Excle的行和列
        row = CaseData["id"]
        column = 11

        # 初始化对应的值：
        res = None
        msg = None
        value = None

        # -------------------------发送请求-------------------------------
        try:
            # 请求数据
            dict_data = {
                "url": CaseData["url"] + CaseData["path"],
                "params": eval(CaseData["params"]),
                "headers": eval(CaseData["headers"]),
                "data": eval(CaseData["data"])
            }

            if CaseData["type"] == "json":
                dict_data["data"] = json.dumps(dict_data["data"])
        except Exception:
            value = MSG_DATA_ERROR
            FileReader.write_data_excel(row=row,column=column,value=value)
        else:
            # 得到对应的响应数据
            res = getattr(self.ak, CaseData["method"])(**dict_data)

        # -------------------------进行断言处理-------------------------------
        # 实际结果
        try:
            msg = self.ak.get_value(res.json(), CaseData["actualResult"])
        except Exception:
            value = MSG_EXDATA_ERROR
            FileReader.write_data_excel(row=row,column=column,value=value)
        else:
            # 只会是一个分支语言，但是不会造成测试结果成功或者失败，所以必须无论如何都是需要断言
            if msg == CaseData["expectResult"]:
                value = MSG_ASSERT_OK
            else:
                value = MSG_ASSERT_NO
            FileReader.write_data_excel(row=row,column=column,value=value)
        finally:
            assert msg == CaseData["expectResult"], value


