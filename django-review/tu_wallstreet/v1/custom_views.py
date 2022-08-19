from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Users
from .serializers import SignupSerializer, UserSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

import multiprocessing
import urllib
import datetime
from collections import OrderedDict
from functools import partial

def calculate_time_points(time_stamp):
    new_time_stamp = (int(time_stamp) // 1000) // 60
    new_time_stamp -= (new_time_stamp % 15)
    new_time_stamp *= 1000 * 60
    begin_time_stamp = datetime.datetime.fromtimestamp(int(new_time_stamp)/1000.0)
    end_time_stamp = begin_time_stamp + datetime.timedelta(minutes=15)
    return str(begin_time_stamp), str(end_time_stamp)

def f(ns, manager_lock, filename):
    my_request = urllib.request.urlopen(filename)
    data = my_request.read().decode("utf8")
    file = data.splitlines()
    with manager_lock:
        for line in file:
            _, time_stamp, order_name = line.split(" ")
            begin_point, end_point = calculate_time_points(time_stamp)
            time_key = begin_point + " / " + end_point

            if time_key not in ns.keys():
                ns[time_key] = {}
            inner_dict = ns[time_key]

            if order_name not in inner_dict:
                inner_dict[order_name] = 0

            inner_dict[order_name] += 1
            ns[time_key] = inner_dict

class LogProcessor(APIView):
    def post(self, request):
        file_count = request.data['parallelFileProcessingCount']
        file_list = request.data['logFiles']

        if file_count == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        manager = multiprocessing.Manager()
        processors = []
        ns = manager.dict()

        manager_pool = multiprocessing.Pool(processes=file_count)
        manager_lock = manager.Lock()
        partial_function = partial(f, ns, manager_lock)
        manager_pool.map(partial_function, file_list)
        manager_pool.close()
        manager_pool.join()

        # for i in range(len(file_list)):
        #     p = multiprocessing.Process(target=f, args=(ns, manager, file_list[i]))
        #     processors.append(p)
        #     p.start()

        # for i in range(len(file_list)):
        #     processors[i].join()
        #     # processors[i].close()
        sorted_ns = ns
        
        final_response = []
        checker = {}
        for key, value in sorted_ns.items():
            begin, end = key.split("/")
            begin = ":".join(begin.split(" ")[1].split(":")[:2])
            end = ":".join(end.split(" ")[2].split(":")[:2])

            new_value = {"timestamp":begin + "-" + end, "logs":[]}
            for order_name, order_count in value.items():
                if order_name in checker.keys():
                    checker[order_name] += order_count
                else:
                    checker[order_name] = order_count 
                new_value["logs"].append({"order": order_name, "count": order_count})
            final_response.append(new_value)

        return Response({"response":final_response}, status=status.HTTP_200_OK)
