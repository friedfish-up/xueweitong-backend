from flask import Flask, request, Response
from flask_mysqldb import MySQL
import json
from datetime import datetime

app = Flask(__name__)

# 数据库配置
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'xueweitong'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# 自定义JSON序列化：自动处理datetime类型
def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError(f'Type {type(obj)} not serializable')

# 统一响应工具：处理中文+时间序列化
def make_response(data):
    return Response(
        json.dumps(data, ensure_ascii=False, default=json_serial),
        mimetype='application/json;charset=utf-8'
    )

# ----------------------
# 测试接口
# ----------------------
@app.route('/test-db', methods=['GET', 'POST'])
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT 1')
        return make_response({"code":0, "msg":"数据库连接成功！"})
    except Exception as e:
        return make_response({"code":-1, "msg":f"数据库连接失败：{str(e)}"})

# ----------------------
# 用户模块（微信登录）
# ----------------------
@app.route('/api/user/login', methods=['GET', 'POST'])
def user_login():
    openid = request.values.get('openid')
    nickname = request.values.get('nickname', '用户')
    avatar = request.values.get('avatar', '')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE openid=%s", (openid,))
    user = cur.fetchone()

    if user:
        return make_response({"code":0, "msg":"登录成功", "user":user})
    else:
        cur.execute("INSERT INTO user(openid,nickname,avatar) VALUES(%s,%s,%s)",
                    (openid, nickname, avatar))
        mysql.connection.commit()
        return make_response({"code":0, "msg":"注册并登录成功"})

# ----------------------
# 案件创建
# ----------------------
@app.route('/api/case/create', methods=['GET', 'POST'])
def case_create():
    user_id = request.values.get('user_id')
    title = request.values.get('title')
    content = request.values.get('content','')

    if not user_id or not title:
        return make_response({"code":-1,"msg":"用户ID和标题不能为空"})
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO case_info(user_id,title,content) VALUES(%s,%s,%s)",
                (user_id, title, content))
    mysql.connection.commit()
    return make_response({"code":0,"msg":"案件创建成功"})

# ----------------------
# 案件列表
# ----------------------
@app.route('/api/case/list', methods=['GET', 'POST'])
def case_list():
    user_id = request.values.get('user_id')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM case_info WHERE user_id=%s", (user_id,))
    data = cur.fetchall()
    return make_response({"code":0,"data":data})

# ----------------------
# 结果生成（四关规则）
# ----------------------
@app.route('/api/result/generate', methods=['GET', 'POST'])
def result_generate():
    case_id = request.values.get('case_id')
    result = {
        "关1":"通过",
        "关2":"通过",
        "关3":"待审核",
        "关4":"未开始",
        "结论":"符合条件"
    }

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO case_result(case_id,result_data) VALUES(%s,%s)",
                (case_id, json.dumps(result, ensure_ascii=False, default=json_serial)))
    mysql.connection.commit()

    return make_response({"code":0,"data":result})

# ----------------------
# 证据上传
# ----------------------
@app.route('/api/evidence/upload', methods=['GET', 'POST'])
def evidence_upload():
    case_id = request.values.get('case_id')
    file_name = request.values.get('file_name')
    file_url = request.values.get('file_url')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO evidence(case_id,file_name,file_url) VALUES(%s,%s,%s)",
                (case_id, file_name, file_url))
    mysql.connection.commit()

    return make_response({"code":0,"msg":"证据上传成功"})

# ----------------------
# 联系人保存
# ----------------------
@app.route('/api/contact/save', methods=['GET', 'POST'])
def contact_save():
    user_id = request.values.get('user_id')
    name = request.values.get('name')
    phone = request.values.get('phone')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO emergency_contact(user_id,name,phone) VALUES(%s,%s,%s)",
                (user_id, name, phone))
    mysql.connection.commit()

    return make_response({"code":0,"msg":"联系人保存成功"})

# ----------------------
# 委托函生成
# ----------------------
@app.route('/api/letter/create', methods=['GET', 'POST'])
def letter_create():
    user_id = request.values.get('user_id')
    case_id = request.values.get('case_id')
    content = request.values.get('content')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO letter_record(user_id,case_id,content) VALUES(%s,%s,%s)",
                (user_id, case_id, content))
    mysql.connection.commit()

    return make_response({"code":0,"msg":"委托函生成成功"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')