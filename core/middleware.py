#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import platform
import subprocess

from django.db import connection


# class MacAddressParser():
#     client_ip = None

#     #     client_request = None

#     def doParseMacAddress(self, client_ip):  # , client_request):
#         '''
#         Detect client mac address
#         output: result, mac-address string, message if error
#         '''
#         self.client_ip = client_ip
#         #         self.client_request = client_request

#         # detect server platform
#         sys_platform = platform.system().lower()

#         if sys_platform == "windows":
#             return self._doParseMacAddress_Win()
#         if sys_platform == "darwin" or sys_platform == "linux":
#             return self._doParseMacAddress_Linux()
#         return False, "", "System Platform %s is not supported." % sys_platform

#     def _doParseMacAddress_Win(self):
#         # get the arp list
#         p1 = subprocess.Popen(
#             ['arp', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#         out1, err1 = p1.communicate()
#         #         print "ARP:", out1

#         # split arp to array
#         mac_address = ''
#         try:
#             # get the mac address from arp list
#             arp_arr = out1.split('\n')
#             for arp_info in arp_arr:
#                 arr = arp_info.split()
#                 if (len(arr) >= 2):
#                     #                         print arr[0], 'vs', ip, arr[0] == ip
#                     if (arr[0] == self.client_ip):
#                         mac_address = arr[1]
#                         break

#             return True, mac_address, ''
#         except Exception, ex:
#             return False, '', "PrintMacAddressAndIpMiddleware. Can not split arp: %s" % ex

#     def _doParseMacAddress_Linux(self):
#         # get the arp list
#         p1 = subprocess.Popen(
#             ['arp', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#         out1, err1 = p1.communicate()
#         #         print "ARP:", out1
#         #         ? (169.254.38.115) at 60:f8:1d:c0:f2:e on en0 [ethernet]
#         #         ? (169.254.130.195) at 60:f8:1d:c0:f2:e on en0 [ethernet]
#         #         ? (169.254.203.142) at 70:f1:a1:ab:a9:38 on en0 [ethernet]
#         #         ? (192.168.2.1) at 0:d0:cb:0:0:5 on en0 ifscope [ethernet]
#         #         ? (192.168.2.101) at 60:f8:1d:c0:f2:e on en0 ifscope [ethernet]

#         # split arp to array

#         mac_address = ''
#         try:
#             # get the mac address from arp list
#             arp_arr = out1.split('\n')
#             for arp_info in arp_arr:
#                 arr = arp_info.split()
#                 if (len(arr) >= 4):
#                     if (arr[1].find(self.client_ip) != -1):
#                         mac_address = arr[3]
#                         break

#             return True, mac_address, ''
#         except Exception, ex:
#             return False, '', "PrintMacAddressAndIpMiddleware. Can not split arp: %s" % ex
#         return False, '', "Not supports"


# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip


# def check_ping(hostname):
#     response = os.system(
#         "ping " + ("-n 1 " if platform.system().lower() == "windows" else "-c 1 ") + hostname)
#     #     print response
#     # and then check the response...
#     if response == 0:
#         return True
#     return False


# class PrintMacAddressAndIpMiddleware(object):
#     """
#     This middleware will log Mac Address using subprocess module on Linux OS.
#     The idea is to use system command to ping remote device IP and get the MAC address from system ARP list.
#              STILL BUGGGGGG
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # don't try to parse mac address averytime
#         if hasattr(request, 'RPI_PHYSICAL') and request.RPI_PHYSICAL.get("MAC_ADDRESS", '') != '':
#             return

#         try:
#             client_ip = get_client_ip(request)

#             parser = MacAddressParser()
#             result, mac_address, msg = parser.doParseMacAddress(client_ip)

#             if not result:
#                 print "Process get mac fail:", msg
#             # now append data to request

#             data = {
#                 'IP': client_ip,
#                 'MAC_ADDRESS': mac_address,
#                 "PLATFORM": platform.system(),

#                 # extra info
#                 "HTTP_HOST": request.META.get("HTTP_HOST", ''),
#                 "COMPUTERNAME": request.META.get("COMPUTERNAME", ''),
#                 "USERDOMAIN": request.META.get("USERDOMAIN", ''),
#                 "HTTP_ACCEPT": request.META.get("HTTP_ACCEPT", ''),
#                 "HTTP_USER_AGENT": request.META.get("HTTP_USER_AGENT", ''),
#                 "NUMBER_OF_PROCESSORS": request.META.get("NUMBER_OF_PROCESSORS", ''),
#                 "PATH_INFO": request.META.get("PATH_INFO", '')

#             }
#             request.RPI_PHYSICAL = data

#         except Exception, ex:
#             print "PrintMacAddressAndIpMiddleware:", ex

#         response = self.get_response(request)

#         return response


class QueryCountDebugMiddleware(object):
    """
    This middleware will log the number of queries run
    and the total time taken for each request (with a
    status code of 200). It does not currently support
    multi-db setups.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # call before views
        response = self.get_response(request)
        # call after views
        try:
            if response.status_code == 200:
                total_time = 0
                for query in connection.queries:
                    query_time = query.get('time')
                    if query_time is None:
                        # django-debug-toolbar  the connection
                        # cursor wrapper and adds extra information in each
                        # item in connection.queries. The query time is stored
                        # under the key "duration" rather than "time" and is
                        # in milliseconds, not seconds.
                        query_time = query.get('duration', 0) / 1000
                    total_time += float(query_time)

                # logger.info('%s queries run, total %s seconds' % (len(connection.queries), total_time))
                print('%s queries run, total %s seconds' %
                      (len(connection.queries), total_time))
        except Exception as e:
            print e
            pass
        return response


class cfgWebsiteMiddleware(object):
    """
    This middleware load cfgWebsite setting and pass to each request
    """

    def process_request(self, request):
        from core.models import cfgWebsite, Customer
        from django.conf import settings
        if not hasattr(request, 'cfgWebsite'):
            cf = cfgWebsite.objects.get(pk=1)  # static and only one setting
            request.cfgWebsite = cf
            request.DEBUG = settings.DEBUG

        #         print request.cfgWebsite.site_name
        # current customer info
        if request.user is None or not request.user.is_authenticated():
            request.customer = None
        else:
            if not hasattr(request, 'customer') or request.customer is None:
                customers = Customer.objects.filter(user=request.user)
                if (customers and len(customers) == 1):
                    request.customer = customers[0]
                else:
                    request.customer = None

#         print cf.site_name


#
# class MemoryUsageMiddleware(object):
#     import psutil
# #     from psutil import  Process as psutilProcess
#
#     if settings.py.DEBUG:
#
#
#         ''' Hiển thị memory usage từng request bằng cách tính memory trước khi request và sau khi request '''
#         """
#         Measure memory taken by requested view, and response
#         """
#         def _is_media_request(self, request):
#             path = request.META['PATH_INFO']
#             return "media" in path or (settings.py.MEDIA_URL and settings.py.MEDIA_URL in path)
#
#         def _sizeof_fmt(self, num, suffix='B'):
#             for unit in ['','K','M','G','T']:
#                 if abs(num) < 1024.0:
#                     return "%3.1f%s%s" % (num, unit, suffix)
#                 num /= 1024.0
#             return "%.1f%s%s" % (num, 'Yi', suffix)
#
#         def process_request(self, request):
#             if self._is_media_request(request):
#                 return None
#             # lưu thông tin trước request
#             request._mem = psutil.Process(os.getpid()).memory_info()
#
#
#         def process_response(self, request, response):
#             if self._is_media_request(request):
#                 return response
#
#             mem = psutil.Process(os.getpid()).memory_info()
#             diff = mem.rss - request._mem.rss
#
#             print(
#                 "PROCESSED %s: memory used %s (%s -> %s), response size: %s" %
#                 (request.path,
#                 self._sizeof_fmt(diff),
#                 self._sizeof_fmt(request._mem.rss),
#                 self._sizeof_fmt(mem.rss),
#                 self._sizeof_fmt(len(response.content)),)
#             )
#
#             return response
