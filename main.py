import os
import pytest

if __name__ == "__main__":
    pytest.main(["-v", "test_case/test_case_002.py", "--alluredir", "report", "--clean-alluredir"])
    os.system("allure generate report -o allure-report --clean")
   