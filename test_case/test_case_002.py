from jinja2 import Template
import allure
from common.FileDataDriver import FileReader
import pytest
import json  # 使用更安全的 json 解析
from typing import Dict, Any
from Api_Keywork.Api_Key import ApiKey
from config import *


class TestCase:
    CaseData = FileReader.read_excel() or []# 避免 None 情况
    RESULT_COLUMN  = 11
    ak = ApiKey()
    all_dict = {}


    def __dynamic_title(self, case_data: Dict[str, Any]):
        """动态生成Allure报告标题"""
        if case_data.get("caseName"):
            allure.dynamic.title(case_data["caseName"])
        if case_data.get("storyName"):
            allure.dynamic.story(case_data["storyName"])
        if case_data.get("featureName"):
            allure.dynamic.feature(case_data["featureName"])
        if case_data.get("remark"):
            allure.dynamic.description(case_data["remark"])
        if case_data.get("rank"):
            allure.dynamic.severity(case_data["rank"])

    def __safe_json_parse(self, json_str: str) -> Dict[str, Any]:
        """安全解析JSON字符串"""
        try:
            return json.loads(json_str) if json_str else {}
        except json.JSONDecodeError:
            return {}

    def __prepare_request_data(self, case_data:Dict[str, Any]) -> Dict[str, Any]:
        if case_data["data"] is None:
            data = None
        else:
            data = FileReader.encrypt_data_aes(self.__safe_json_parse(case_data.get("data")))
        # 准备请求数据
        dict_data = {
            "url": case_data["url"] + case_data["path"],
            "params": self.__safe_json_parse(case_data.get("params")),
            "headers": self.__safe_json_parse(case_data.get("headers")),
            "data": data
        }

        # 2. 处理json类型数据
        if case_data.get("type") == "json":
            dict_data["data"] = json.dumps(dict_data["data"])

        return dict_data

    def __json_extraction(self, case_data, res):
        """
        批量jsonpath提取数据
        :param case_data:
        :param res:
        :return:
        """
        try:
            if case_data["jsonExData"]:
                expect_extract_data = self.__safe_json_parse(case_data.get("jsonExData"))
                for key,value in expect_extract_data.items():
                    new_dict = self.ak.get_value(res, value)
                    self.all_dict.update(
                        {key: new_dict}
                    )
                print(f"提取出来的数据： {self.all_dict}")
            else:
                print("需要提取的数据为空")
        except Exception:
            print("请检查你需要提取数据格式的正确性")

    def __sql_extraction(self, case_data):
        try:
            if case_data["sqlExData"]:
                sql_extract_data= self.__safe_json_parse(case_data.get("sqlExData"))
                for key,value in sql_extract_data.items():
                    new_value = self.ak.get_sql_data(value)
                    self.all_dict.update(
                        {key: new_value}
                    )
                print(f"数据库提取后的数据为: {self.all_dict}")
            else:
                print("数据库需要提取的数据为空")
        except Exception:
            print("请检查你数据库需要提取数据格式的准确性")

    def __sql_assert(self, case_data):
        if not case_data.get("sqlAssertData") or not case_data.get("sqlExpectResult"):
            return
            # 解析预期结果(应该是固定值)
        try:
            expect_data = self.__safe_json_parse(case_data["sqlExpectResult"])

            # 解析SQL查询语句并执行
            reality_data_dict = {}
            sql_queries = self.__safe_json_parse(case_data["sqlAssertData"])  # 获取SQL查询字典

            for key, sql_query in sql_queries.items():
                # 确保执行SQL查询，而不是直接返回SQL字符串
                query_result = self.ak.get_sql_data(sql_query)

                # 处理查询结果(假设返回的是单行单列值)
                reality_data_dict.update(
                    {key: query_result}
                )

            print(f"数据库预期值为: {expect_data}, 数据库实际提取值为: {reality_data_dict}")

            # 比较结果
            assert expect_data == reality_data_dict, f"数据库断言失败: 预期 {expect_data} ≠ 实际 {reality_data_dict}"
        except Exception as e:
            raise AssertionError(f"数据库校验异常: {str(e)}")

    @pytest.mark.parametrize("case_data", CaseData)
    def testcase(self, case_data: Dict[str, Any]):
        self.__dynamic_title(case_data)
        case_data = eval(Template(str(case_data)).render(self.all_dict))

        test_result = "Passed"  # 默认状态
        error_msg = None

        try:

            # 1. 准备请求数据
            dict_data = self.__prepare_request_data(case_data)
            print(dict_data)
            # 2. 发送请求
            res = getattr(self.ak, case_data["method"])(**dict_data)
            res_json = res.json()
            print(res_json)

            # 3. 获取实际结果并断言
            actual_result = self.ak.get_value(res_json, case_data["actualResult"])
            print(f"actual_result: {actual_result}")
            assert actual_result == case_data["expectResult"], \
                f"断言失败: 预期[{case_data['expectResult']}], 实际: [{actual_result}]"
            self.__json_extraction(case_data, res_json)
            self.__sql_assert(case_data)

            if case_data["responseExpect"]:
                deepdiff_expect_data = self.__safe_json_parse(case_data.get("responseExpect"))
                other = eval(case_data["responseExclude"])
                print(f"得到的responseExclude: {other}")
                jsonMaxDataRes = self.ak.data_deepdiff(deepdiff_expect_data, res_json, **other)
                assert  jsonMaxDataRes, "大量数据响应断言失败，两者数据不一致"

        except AssertionError as ae:
            # 断言失败的专属处理
            test_result = "Failed"
            error_msg = str(ae)
            pytest.fail(error_msg)  # 标记测试失败

        except Exception as e:
            # 其他异常（如网络错误、JSON解析错误）
            test_result = "Failed"
            error_msg = f"请求执行失败: {str(e)}"
            pytest.fail(error_msg)

        finally:
            # 无论成功失败，最终一定会写入结果
            FileReader.write_data_excel(
                row=case_data["id"],
                column=self.RESULT_COLUMN,
                value=test_result if not error_msg else f"Failed: {error_msg}"
            )

