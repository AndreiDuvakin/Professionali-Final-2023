import datetime
import random

from flask import Flask, make_response, jsonify, render_template, abort, request, redirect
from db.connect import Staff, connect, init_data, Utilizators, Services, OrdersServices, Orders, Reports
from math import sqrt
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

import numpy as np
import pandas as pd

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
    serv_ord = con.query(OrdersServices).filter(OrdersServices.service_id == serv_id,
                                                OrdersServices.order_id == order_id).first()
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


@app.route('/reports')
def reports():
    if not auth:
        return redirect('/login')
    return render_template('reports.html')


@app.route('/report/control')
def control():
    if not auth:
        return redirect('/login')
    con = connect()
    znach = sorted(con.query(Reports).all(),
                   key=lambda x: x.date)
    all_znach = list(map(lambda x: x.dispersion, znach[::-1]))
    avr = round(sum(all_znach) / len(all_znach), 2)
    otkln = round(sqrt(sum([(i - avr) ** 2 for i in all_znach]) / len(all_znach)), 2)
    variation = round(otkln / avr * 100, 2)
    s1 = avr + avr * 1
    s2 = avr + avr * 2
    s3 = avr + avr * 3
    s1_ = avr - avr * 1
    s2_ = avr - avr * 2
    s3_ = avr - avr * 3
    fig = go.Figure(layout_yaxis_range=[s3_, s3])
    fig.add_trace({"x": np.array(
        [i.date.strftime('%d.%m.%Y %h:%M') for i in
         znach]),
        "y": np.array(all_znach)})
    fig.update_layout(
        title=f"Среднее отклонение:      {str(round(otkln) / 100)}<br>Коэф. вариации       {str(variation)}%",
        plot_bgcolor='rgb(255, 255, 255)'
    )
    fig.update_traces(line_color='rgb(180, 180, 180)')
    fig.update_yaxes(
        gridcolor='Gray'
    )
    fig.update_xaxes(
        gridcolor='Gray'
    )
    fig.show()
    return '200'


@app.route('/accept/<int:order_id>/<int:serv_id>')
def accept(order_id, serv_id):
    if not auth:
        return redirect('/login')
    znach = [random.randint(0, 100) for i in range(6)]
    otkl = random.randint(0, 6)
    con = connect()
    rep = Reports(
        order_id=order_id,
        staff_id=con.query(Staff).filter(Staff.login == auth[0], Staff.password == auth[1]).first().id,
        service_id=serv_id,
        density=znach[0],
        dispersion=znach[1],
        mercury_con=znach[2],
        creosol_con=znach[3],
        potassium_con=znach[4],
        heavy_met_con=znach[5],
        date=datetime.datetime.now()
    )
    con.add(rep)
    con.commit()
    con.close()
    return render_template('accept.html', znach=znach, otkl=otkl, order_id=order_id, serv_id=serv_id)


@app.route('/util/<int:u_id>', methods=['GET', 'POST'])
def util(u_id):
    if request.method == 'GET':
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
    else:
        data = request.values.to_dict()
        print(data)


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
