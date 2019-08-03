import json
import os
import os.path
import random
from pprint import pprint

import trafaret as T

SOURCES = {
    'ryanair':
    T.Dict({
        T.Key('airports'): T.List(
            T.Dict({
                T.Key('iataCode') >> 'code': T.String(),
                T.Key('routes'): T.List(
                    T.String() >> (lambda s: s.split(':', maxsplit=1))
                ) >> (lambda seq: [b for a, b in seq if a == 'airport'])
            }).ignore_extra('*'))
    }).ignore_extra('*'),
    'wizzair':
    T.List(
        T.Dict({
            T.Key('iata') >> 'code': T.String(),
            T.Key('connections') >> 'routes': T.List(
                T.Dict({
                    T.Key('iata') >> 'code': T.String(),
                }).ignore_extra('*'))
        }).ignore_extra('*')),
    'airbaltic': T.Dict({
    })
}
СITYES = {
    'ryanair':
    T.Dict({
        T.Key('airports'): T.List(
            T.Dict({
                T.Key('iataCode') >> 'code': T.String(),
                T.Key('name') >> 'city': T.String,
            }).ignore_extra('*'))
    }).ignore_extra('*'),
    'wizzair':
    T.List(
        T.Dict({
            T.Key('connections') >> 'routes': T.List(
                T.Dict({
                    T.Key('iata') >> 'code': T.String,
                    T.Key('shortName') >> 'city': T.String,
                }).ignore_extra('*'))
        }).ignore_extra('*')),
    'airbaltic': T.Dict({
    })
}


def load_data(path):
    em_dict = {}
    for fqname in os.listdir(path):
        fname, _ = os.path.splitext(fqname) #!  fname, _?
        schema = SOURCES.get(fname)
        if schema:
            with open(os.path.join(path, fqname), 'rb') as datafile:

                if fqname == 'ryanair.json':
                    di_ryanair = {}
                    data = json.load(datafile)
                    em_ry = schema.check(data).values()
                    for i in em_ry:
                        for ii in i:
                            di_ryanair.update(dict([(str(list(ii.items())[0][1]), list(ii.items())[1][1])]))
                    em_dict.update(dict([["ryanair", di_ryanair]]))
                if fqname == 'wizzair.json':
                    di_wizzair = {}
                    data = json.load(datafile)
                    em_wiz = schema.check(data)
                    for code in em_wiz:
                        routes = []
                        for ii in [(list(code.values())) for code in (list(code.items())[1][1])]:
                            routes.append(ii[0])
                        di_wizzair.update(dict([[list(code.values())[0], routes]]))
                    em_dict.update(dict([["wizzair", di_wizzair]]))
                # if fqname == 'airbaltic.json':              #не смог осилить*(
                #     di_airbaltic = {}                       #почему-то по ключу 'destinations' выдаёт 2 города,
                #     data = json.load(datafile)              #а в конце ошибку о том что этот ключь отсутствует
                #     # return(data.keys())
                #     for f_code in data.values():
                #         for i in data.keys():
                #             print(i, list(f_code['destinations'].keys()))
                #             # di_airbaltic.update([[i, list(f_code['destinations'].keys())]])
                #         # for routes_f in data.values():
                #             # print(list(routes_f['destinations'].keys()))
                #             # routes.append(list(routes_f['destinations'].keys()))
    return em_dict

def cityes_data(path): #перевод iata в нормальные названия
    city_data = {}
    for fqname in os.listdir(path):
        fname, _ = os.path.splitext(fqname)  # !  fname, _?
        schema = СITYES.get(fname)
        if schema:
            with open(os.path.join(path, fqname), 'rb') as datafile:
                if fqname == 'ryanair.json':
                    data = json.load(datafile)
                    em_ry = schema.check(data).values()
                    for i in list(em_ry)[0]:
                        city_data.update({i['code']: i['city']})
                if fqname == 'wizzair.json':
                    data = json.load(datafile)
                    for i in data:
                        city_data.update({i['iata']: i['shortName']})
    return city_data

def direct_flight(FROM_R, TO_R):
    air_comp = list(SOURCES.keys())
    routes_dict = load_data('data')
    for i in air_comp:
        try:
            if TO_R in routes_dict[i][FROM_R]:
                return i
            else:
                pass
        except:
            pass

def transfer_flight (FROM_R, TO_R):
    em_list = []
    routes_dict = load_data('data')
    for a in routes_dict:
        for i in routes_dict.values():
            try:
                for ii in i[FROM_R]:
                    if TO_R in (i[ii]):
                        em_list.append([a, ii])
            except:
                pass
    flight = random.choice(em_list)
    return flight

def iata_translater(self):
    iata_dict = cityes_data('data')
    if self in iata_dict:
        return iata_dict[self]
    else:
        pass

def pap():                                         #cписок валидных iata
    for i in (list(load_data('data').values())):
        return list(i.keys())
