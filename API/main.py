from API.db.connect import init_data, connect
from db.connect import Staff
from flask import Flask, abort, request

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    data = request.values
    con = connect()
    res = con.query(Staff).filter(Staff.login == data['login']).first()
    if not res:
        abort(404)
    if not res.password == data['password']:
        abort(403)
    return [res.id, res.ip, res.name, res.surname, res.type_id]


if __name__ == '__main__':
    init_data()
    app.run('localhost', port=5000)
