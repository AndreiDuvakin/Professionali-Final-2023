import sqlalchemy.ext.declarative as dec
from sqlalchemy.orm import Session
import sqlalchemy.orm as orm
from sqlalchemy import create_engine
import sqlalchemy as sq

__factory = None
base = dec.declarative_base()


class Services(base):
    __tablename__ = 'services'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String, nullable=False)
    price = sq.Column(sq.Float, nullable=False)
    time_exe = sq.Column(sq.Integer)
    sr_otklon = sq.Column(sq.Float)
    archive = sq.Column(sq.Boolean, default=False)


class Organizations(base):
    __tablename__ = 'organizations'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String, nullable=False)
    address = sq.Column(sq.String, nullable=False)
    inn = sq.Column(sq.String, nullable=False)
    pay_acc = sq.Column(sq.String, nullable=False)
    bik = sq.Column(sq.String)


class Clients(base):
    __tablename__ = 'clients'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    login = sq.Column(sq.String, nullable=False)
    password = sq.Column(sq.String, nullable=False)
    name = sq.Column(sq.String, nullable=False)
    surname = sq.Column(sq.String, nullable=False)
    patronymic = sq.Column(sq.String)
    birthday = sq.Column(sq.Date, nullable=False)
    serial = sq.Column(sq.VARCHAR(4), nullable=False)
    number = sq.Column(sq.VARCHAR(6), nullable=False)
    organization_id = sq.Column(sq.Integer, sq.ForeignKey('organizations.id'))


class Statuses(base):
    __tablename__ = 'statuses'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String)


class Orders(base):
    __tablename__ = 'orders'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    date = sq.Column(sq.Date, nullable=False)
    time_executable = sq.Column(sq.Integer)
    status_id = sq.Column(sq.Integer, sq.ForeignKey('statuses.id'))
    client_id = sq.Column(sq.Integer, sq.ForeignKey('clients.id'))
    archive = sq.Column(sq.Boolean, default=False)


class Utilizators(base):
    __tablename__ = 'utilizators'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String)
    free = sq.Column(sq.Boolean, default=True)


class Types(base):
    __tablename__ = 'types'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String)


class Staff(base):
    __tablename__ = 'staff'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    login = sq.Column(sq.String, nullable=False)
    password = sq.Column(sq.String, nullable=False)
    ip = sq.Column(sq.String, nullable=False)
    name = sq.Column(sq.String, nullable=False)
    surname = sq.Column(sq.String, nullable=False)
    patronymic = sq.Column(sq.String)
    lastenter = sq.Column(sq.Date)
    birthday = sq.Column(sq.Date)
    type_id = sq.Column(sq.Integer, sq.ForeignKey('types.id'))


class StaffServices(base):
    __tablename__ = 'staff_services'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    staff_id = sq.Column(sq.Integer, sq.ForeignKey('staff.id'))
    service_id = sq.Column(sq.Integer, sq.ForeignKey('services.id'))
    archive = sq.Column(sq.Boolean, default=False)


class ServiceExecutable(base):
    __tablename__ = 'service_executable'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    time_executable = sq.Column(sq.DateTime, nullable=False)
    service_id = sq.Column(sq.Integer, sq.ForeignKey('services.id'))
    staff_id = sq.Column(sq.Integer, sq.ForeignKey('staff.id'))
    utilizator_id = sq.Column(sq.Integer, sq.ForeignKey('utilizators.id'))
    archive = sq.Column(sq.Boolean, default=False)


class UtilizatorData(base):
    __tablename__ = 'utilizator_data'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    date_order = sq.Column(sq.DateTime, nullable=False)
    date_executable = sq.Column(sq.Date, nullable=False)
    time_executable = sq.Column(sq.Integer)
    utilizator_id = sq.Column(sq.Integer, sq.ForeignKey('utilizators.id'))
    archive = sq.Column(sq.Boolean, default=False)


class OrdersServices(base):
    __tablename__ = 'orders_services'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    service_id = sq.Column(sq.Integer, sq.ForeignKey('services.id'))
    order_id = sq.Column(sq.Integer, sq.ForeignKey('orders.id'))
    archive = sq.Column(sq.Boolean, default=False)
    status_id = sq.Column(sq.Integer, sq.ForeignKey('service_statuses.id'))


class PayReciept(base):
    __tablename__ = 'pay_reciept'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String, nullable=False)
    date = sq.Column(sq.Date, nullable=False)
    staff_id = sq.Column(sq.Integer, sq.ForeignKey('staff.id'))
    archive = sq.Column(sq.Boolean, default=False)


class UtilizatorHistories(base):
    __tablename__ = 'utilizator_histories'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    result = sq.Column(sq.TEXT)
    type_utilizatoin = sq.Column(sq.Boolean)
    order_id = sq.Column(sq.Integer, sq.ForeignKey('orders.id'))
    staff_id = sq.Column(sq.Integer, sq.ForeignKey('staff.id'))


class ServiceStatuses(base):
    __tablename__ = 'service_statuses'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name = sq.Column(sq.TEXT)


class Reports(base):
    __tablename__ = 'reports'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    order_id = sq.Column(sq.Integer, sq.ForeignKey('orders.id'))
    staff_id = sq.Column(sq.Integer, sq.ForeignKey('staff.id'))
    service_id = sq.Column(sq.Integer, sq.ForeignKey('services.id'))
    density = sq.Column(sq.Float)
    dispersion = sq.Column(sq.Float)
    mercury_con = sq.Column(sq.Float)
    creosol_con = sq.Column(sq.Float)
    potassium_con = sq.Column(sq.Float)
    heavy_met_con = sq.Column(sq.Float)


def init_data():
    global __factory
    eng = create_engine('postgresql+pg8000://postgres:4951@localhost:5432/professionals')
    __factory = orm.sessionmaker(bind=eng)
    base.metadata.create_all(eng)


def connect() -> Session:
    global __factory
    return __factory()
