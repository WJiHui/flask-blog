# encoding:utf-8

import time
import json
import socket
import inspect
import requests


class SystemInfo(object):
    def __init__(self):
        self.data = {}

    @staticmethod 
    def get_time():
        return str(int(time.time() + 8*3600))

    @staticmethod 
    def get_host():
        return socket.gethostname()

    @staticmethod
    def get_load_avg():
        with open("/proc/loadavg") as load_open:
            a = load_open.read().split()[:3]
            return ','.join(a)

    @staticmethod
    def get_mem_total():
        with open("/proc/meminfo") as mem_open:
            a = int(mem_open.readline().split()[1])
            return a/1024

    @staticmethod
    def get_mem_usage(no_buffer_cache=True):
        if no_buffer_cache:
            with open("/proc/meminfo") as mem_open:
                total = int(mem_open.readline().split()[1])
                free = int(mem_open.readline().split()[1])
                available = int(mem_open.readline().split()[1])
                buffer = int(mem_open.readline().split()[1])
                cached = int(mem_open.readline().split()[1])
                return (total - free - available)/1024
        else:
            with open("/proc/meminfo") as mem_open:
                a = int(mem_open.readline().split()[1]) - int(mem_open.readline().split()[1])
                return a/1024

    @staticmethod
    def get_mem_free(no_buffer_cache=True):
        if no_buffer_cache:
            with open("/proc/meminfo") as mem_open:
                total = int(mem_open.readline().split()[1])
                free = int(mem_open.readline().split()[1])
                available = int(mem_open.readline().split()[1])
                buffer = int(mem_open.readline().split()[1])
                cached = int(mem_open.readline().split()[1])
                return (free + available)/1024
                # return (free + buffer + cached)/1024
        else:
            with open("/proc/meminfo") as mem_open:
                mem_open.readline()
                a = int(mem_open.readline().split()[1]) - int(mem_open.readline().split()[1])
                return a/1024

    def run_all_methods(self):
        # 自动获取所有方法
        for fun in inspect.getmembers(self, predicate=inspect.isfunction):
            function_name, self_function = fun
            if function_name[:4] == "get_":
                value = self_function()
                # print(function_name, value)
                self.data[function_name[4:]] = value

        return self.data


