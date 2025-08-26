# Enterprise API Test Automation Framework

一个基于 **Pytest** 和 **数据驱动** 构建的高扩展性、企业级接口自动化测试框架。本框架集成了接口测试、数据库校验、安全加密、复杂参数关联等核心能力，并支持生成精美的Allure测试报告与CI/CD无缝集成。

## 🚀 核心特性

- **🧩 混合驱动模式**: 采用 **「数据驱动」(Excel) + 「关键字驱动」** 设计，测试数据与代码逻辑彻底分离。
- **🔗 智能参数关联**: 基于 `Jinja2` 模板引擎，自动处理接口间的参数依赖（如登录Token传递）。
- **✅ 多维度断言机制**:
  - **字段断言**: 使用 `JSONPath` 进行响应字段提取与校验。
  - **数据库断言**: 直接执行SQL脚本，验证业务数据一致性。
  - **全量比对**: 使用 `DeepDiff` 进行复杂JSON响应体的深度智能比对。
- **🔐 安全测试支持**: 内置 `AES` 对称加密，自动识别并加密请求中的敏感数据。
- **📊 专业测试报告**: 集成 `Allure` 框架，生成详尽、可视化的测试报告，精准定位问题。
- **⚙️ 高度工程化**: 通过 `Pytest Fixture` 管理测试生命周期，与 `GitHub Actions` 等CI工具轻松集成。

## 📁 项目结构
api-test-framework/
├── config/ # 配置文件目录
│ ├── init.py
│ └── config.py # 全局配置（数据库、URL、密钥等）
├── data/ # 测试数据目录
│ └── excel/
│ └── api_cases_V7.xlsx # 数据驱动核心文件
├── common/ # 通用组件与工具
│ ├── init.py
│ ├── FileDataDriver.py # Excel读写、数据加密工具
│ ├── Md5_Encrypt.py # 加密模块
│ └── (其他工具类...)
├── Api_Keywork/ # 核心关键字库
│ ├── init.py
│ └── Api_Key.py # 封装的请求关键字类
├── test_case/ # 测试用例目录
│ ├── init.py
│ ├── conftest.py # Pytest全局配置、Fixture
│ └── test_case_002.py # 核心测试流程套件
├── outputs/ # 运行时输出目录（日志、报告、临时文件）
│ ├── reports/
│ ├── logs/
│ └── tmp/
├── requirements.txt # 项目依赖
├── .env.example # 环境变量示例文件
└── README.md # 项目说明

text

## ⚡ 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+ (如需数据库校验功能)

### 1. 克隆项目

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2. 安装依赖
bash
pip install -r requirements.txt
3. 配置环境
复制环境变量文件并配置您的信息：

bash
cp .env.example .env
在 .env 文件中填写您的真实配置（该文件已被 .gitignore 忽略，确保安全）：

ini
# 数据库配置
DB_HOST=your_db_host
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_strong_password
DB_NAME=your_database_name

# 应用配置
AES_KEY=your_16_24_32_length_key
BASE_URL=http://your-test-env-domain.com
4. 运行测试
方式一：运行全部测试

bash
pytest -v test_case/test_case_002.py --alluredir=./outputs/reports
方式二：运行指定模块或标签的测试

bash
pytest -v test_case/test_case_002.py -k "登录" --alluredir=./outputs/reports
5. 查看测试报告
测试完成后，生成并打开Allure报告：

bash
allure serve ./outputs/reports
📋 Excel数据驱动说明
框架的核心是 api_cases_V7.xlsx 文件，各列说明如下：

列名	说明	示例
用例名(caseName)	测试用例名称	成功登录
地址(url)	主机地址	http://shop.hctestedu.com
路径(path)	API路径	/api/user/login
请求方法(method)	HTTP方法	post
公共参数(params)	URL参数(JSON格式)	{"app": "web"}
参数(data)	请求体(JSON格式), @开头字段自动加密	{"@password": "123456"}
参数类型(type)	请求体类型	json / data
校验字段(actualResult)	JSONPath断言表达式	$.msg
预期结果(expectResult)	期望值	登录成功
JSON提取_引用名称(jsonExData)	提取响应值供后续用例使用	{"TOKEN": "$.data.token"}
SQL提取(sqlExData)	执行SQL并提取结果	{"USER_ID": "SELECT id FROM user"}
SQL校验字段名(sqlAssertData)	校验SQL查询的字段	{"USER_NAME": "SELECT name FROM user"}
SQL期望数据(sqlExpectResult)	SQL查询的预期结果	{"USER_NAME": "test_user"}
响应全量比对(responseExpect)	期望的全量响应体(JSON)	{"code":0, "msg":"success"}
响应全量条件(responseExclude)	全量比对的排除规则	{"exclude_paths": ["data"]}
是否执行(is_true)	是否启用该用例	True / False
🤝 CI/CD 集成
本项目已预置 GitHub Actions 工作流配置。每次提交代码到GitHub后，将自动触发测试流程。

查看自动化测试结果，请访问您仓库的 Actions 标签页。

如需在其他CI平台（如Jenkins、GitLab CI）上运行，请参考 .github/workflows/ci.yml 中的步骤。

🧪 示例用例
框架自动化执行以下流程：

用户登录 → 提取 Token

添加商品到购物车 → 依赖第1步的 Token，提取 CartId

提交订单 → 依赖第1步的 Token 和第2步的 CartId

数据库校验 → 验证订单数据是否成功写入数据库

📈 测试报告预览
https://via.placeholder.com/800x400.png?text=Allure+Report+Screenshot
(建议您上传一张真实的Allure报告截图到此目录，并替换此链接)

💡 常见问题
Q: 如何添加一个新的测试场景？
A: 只需在 api_cases_V7.xlsx 文件中新增一行，按要求填写各列即可，无需修改代码。

Q: 如何处理接口依赖？
A: 在 JSON提取_引用名称 列定义要提取的变量（如 {"VAR_TOKEN": "$.data.token"}），在后续用例的 params、data 或 headers 中，使用 {{VAR_TOKEN}} 语法即可直接引用。

👥 贡献
欢迎提交 Issue 和 Pull Request！

📄 许可证
本项目采用 MIT 许可证。
