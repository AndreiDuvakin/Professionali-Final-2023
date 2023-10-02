import random

from flask import Flask, make_response, jsonify, render_template, abort, request, redirect
from db.connect import Staff, connect, init_data, Utilizators, Services, OrdersServices, Orders, Reports

app = Flask(__name__)

auth = None
utiles = None


@app.route('/')
def main():
    if not auth:
        return redirect('/login')
    con = connect()
    utils = list(filter(lambda x: x.free, con.query(Utilizators).all()))
    con.close()
    return render_template('utilizators.html', utils=utils)


@app.route('/serv/<int:order_id>/<int:serv_id>')
def serv(order_id, serv_id):
    if not auth:
        return redirect('/login')
    global utiles
    con = connect()
    ut = con.query(Utilizators).filter(Utilizators.id == utiles).first()
    ut.free = False
    con.commit()
    serv = con.query(Services).filter(Services.id == serv_id).first()
    order = con.query(Orders).filter(Orders.id == order_id).first()
    con.close()
    return render_template('made_serv.html', serv=serv, order=order, type=random.choice([1, 2]),
                           tme=random.randint(10, 30))


@app.route('/<int:order_id>/<int:serv_id>/accept')
def accept_or(order_id, serv_id):
    if not auth:
        return redirect('/login')
    global utiles
    con = connect()
    ut = con.query(Utilizators).filter(Utilizators.id == utiles).first()
    ut.free = True
    con.commit()
    serv_ord = con.query(OrdersServices).filter(OrdersServices.service_id == serv_id, OrdersServices.order_id == order_id).first()
    serv_ord.status_id = 3
    con.commit()
    con.close()
    return redirect('/')


@app.route('/<int:order_id>/<int:serv_id>/reject')
def reject(order_id, serv_id):
    if not auth:
        return redirect('/login')
    global utiles
    con = connect()
    ut = con.query(Utilizators).filter(Utilizators.id == utiles).first()
    ut.free = True
    serv_ord = con.query(OrdersServices).filter(OrdersServices.service_id == serv_id,
                                                OrdersServices.order_id == order_id).first()
    serv_ord.status_id = 4
    con.commit()
    con.close()
    return redirect('/')


@app.route('/accept/<int:order_id>/<int:serv_id>')
def accept(order_id, serv_id):
    if not auth:
        return redirect('/login')
    znach = [random.randint(0, 100) for i in range(6)]
    otkl = random.randint(0, 6)

    return render_template('accept.html', znach=znach, otkl=otkl, order_id=order_id, serv_id=serv_id)


@app.route('/util/<int:u_id>')
def util(u_id):
    if not auth:
        return redirect('/login')
    global utiles
    con = connect()
    util = con.query(Utilizators).filter(Utilizators.id == u_id).first()
    if not util:
        con.close()
        abort(404)
    services = list(
        map(lambda x: [con.query(Services).filter(Services.id == x.service_id).first(),
                       con.query(Orders).filter(Orders.id == x.order_id).first()],
            con.query(OrdersServices).filter(OrdersServices.status_id == 1).all()))
    utiles = u_id
    con.close()
    return render_template('utilizator.html', ut=util, serv=services)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', message='')
    else:
        data = request.form.to_dict()
        con = connect()
        staff = con.query(Staff).filter(Staff.login == data['login'], Staff.password == data['password']).first()
        con.close()
        if staff:
            global auth
            auth = [data['login'], data['password']]
            return redirect('/')
        return render_template('login.html', message='Неверный логин или пароль')


if __name__ == '__main__':
    init_data()
    app.run('localhost', port=5001)
