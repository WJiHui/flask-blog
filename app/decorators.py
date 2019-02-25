import datetime 
from threading import Thread

def async(function):
    def wrapper(*args, **kwargs):
        thr = Thread(target=function, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def run_time(function):
    def handle_args(*args, **kwargs):
        start = datetime.datetime.now()
        function(*agrs, **kwagrs)
        end = datetime.datetime.now()
        print(str(end - start))
    return handle_args 
