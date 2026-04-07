# xueweitong-backend
学维通微信小程序后端
## 项目介绍
基于 Flask + MySQL 的法律援助小程序后端，
实现用户管理、案件提交、四关审核规则、证据上传、紧急联系人、委托函生成等完整接口。

## 技术栈
- Python 3.8+
- Flask
- MySQL 8.0
- flask-mysqldb

## 数据库初始化
执行 init.sql 自动创建6张核心表：
- user 用户表
- case_info 案件表
- case_result 审核结果表
- evidence 证据表
- emergency_contact 紧急联系人表
- letter_record 委托函表

## 启动方式
1. 安装依赖
pip install flask flask-mysqldb

2. 修改 app.py 中的 MySQL 密码

3. 启动服务
python app.py

4. 访问测试
http://127.0.0.1:5000/test-db

后端接口说明：
基础地址：http://100.65.156.80:5000

完整接口列表：
1.  数据库测试：http://100.65.156.80:5000/test-db
2.  用户登录：http://100.65.156.80:5000/api/user/login
3.  创建案件：http://100.65.156.80:5000/api/case/create
4.  案件列表：http://100.65.156.80:5000/api/case/list
5.  生成四关结果：http://100.65.156.80:5000/api/result/generate
6.  上传证据：http://100.65.156.80:5000/api/evidence/upload
7.  保存联系人：http://100.65.156.80:5000/api/contact/save
8.  生成委托函：http://100.65.156.80:5000/api/letter/create
