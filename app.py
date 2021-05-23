import gevent
from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
from flask import Flask, request
from flask_restful import Resource, Api
import math,os
import multiprocessing
from multiprocessing import Process, current_process, Pool
from threading import *
import zlib,binascii
import sys
import queue



app = Flask(__name__)
api = Api(app)

def fac(N,q):
    result = math.factorial(int(N))
    #print(current_thread().getName())
    #print(os.getpid())
    q.put(result)


class Hello(Resource):
    def get(self):
        return {'hello': 'world'}

class mt(Resource):
    def get(self, mt_number):
        qout = multiprocessing.Queue()
        threads = []
        for i in range(1):
            thread = Thread(target=fac, args=(mt_number, qout))
            threads.append(thread)
        for thread in threads:
            thread.start()
            thread.join()
        return {'factorial': str(qout.get())}


class mp(Resource):
    def get(self, mp_number):
        qout = multiprocessing.Queue()
        processes = []
        for i in range(1):
            p = Process(target=fac, args=(mp_number, qout))
            processes.append(p)
        for p in processes:
            p.start()
            p.join()
        return {'factorial': str(qout.get())}


class ge(Resource):
    def get(self, ge_number):
        qout = multiprocessing.Queue()
        g = gevent.spawn(fac,ge_number,qout)
        g.join()
        return {'factorial': str(qout.get())}



##################################################################################

def buffer(bu_number,bq):
    buffer = bytearray(int(bu_number))
    compressed_value = zlib.compress(buffer,1)
    bq.put(compressed_value)


class mt_buffer(Resource):
    def get(self, mt_buffer_number):
        qout = multiprocessing.Queue()
        threads = []
        for i in range(1):
            thread = Thread(target=buffer, args=(mt_buffer_number, qout))
            threads.append(thread)
        for thread in threads:
            thread.start()
            thread.join()
        return {'compressed_value': str(qout.get())}


class mp_buffer(Resource):
    def get(self, mp_buffer_number):
        qout = multiprocessing.Queue()
        processes = []
        for i in range(2):
            process = Process(target=buffer, args=(mp_buffer_number, qout))
            processes.append(process)
        for process in processes:
            process.start()
            process.join()
        return {'compressed_value': str(qout.get())}



class ge_buffer(Resource):
    def get(self, ge_buffer_number):
        qout = multiprocessing.Queue()
        g = gevent.spawn(buffer,ge_buffer_number,qout)
        g.join()
        #gevent.sleep(0.05)
        return {'compressed_value': str(qout.get())}


api.add_resource(Hello, '/')

#factorial
api.add_resource(mt, '/mt/<int:mt_number>')
api.add_resource(mp, '/mp/<int:mp_number>')
api.add_resource(ge, '/ge/<int:ge_number>')


#buffer
api.add_resource(mt_buffer, '/mt_buffer/<int:mt_buffer_number>')
api.add_resource(mp_buffer, '/mp_buffer/<int:mp_buffer_number>')
api.add_resource(ge_buffer, '/ge_buffer/<int:ge_buffer_number>')


if __name__ == '__main__':
    app.run(debug=True)
