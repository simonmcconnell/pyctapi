#! /usr/bin/env python
#
# PyCtAPI
#
# A plain ctypes wrapper around the CitectSCADA CtAPI DLLs
# only compatible with Windows.
#
# You must have the following DLLs on hand
# - CiDebugHelp.dll
# - Ct_ipc.dll
# - CtApi.dll
# - CtEng32.dll
# - CtRes32.DLL
# - CtUtil32.dll
# - CtUtilManagedHelper.dll - new in v7.50 aka 2015

__title__ = 'pyctapi'
__version__ = '0.1'
__author__ = 'Mitchell Gayner'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2017 Gayner Technical Services'

import platform
if platform.system() != "Windows":
    raise OSError

from datetime import datetime
from ctypes import CDLL, windll, create_string_buffer, byref, sizeof, GetLastError
from ast import literal_eval

ERROR_USER_DEFINED_BASE = 0x10000000

def CT_TO_WIN32_ERROR(dwStatus): return ((dwStatus) + ERROR_USER_DEFINED_BASE)
def WIN32_TO_CT_ERROR(dwStatus): return ((dwStatus) - ERROR_USER_DEFINED_BASE)
def IsCitectError(dwStatus): return (ERROR_USER_DEFINED_BASE < dwStatus)

CT_SUCCESS = True
CT_ERROR = False

CT_SCALE_RANGE_CHECK = 0x00000001
CT_SCALE_CLAMP_LIMIT = 0x00000002
CT_SCALE_NOISE_FACTOR = 0x00000004

CT_FMT_NO_SCALE = 0x00000001
CT_FMT_NO_FORMAT = 0x00000002
CT_FMT_LAST = 0x00000004
CT_FMT_RANGE_CHECK = 0x00000008

CT_FIND_SCROLL_NEXT = 0x00000001
CT_FIND_SCROLL_PREV = 0x00000002
CT_FIND_SCROLL_FIRST = 0x00000003
CT_FIND_SCROLL_LAST = 0x00000004
CT_FIND_SCROLL_ABSOLUTE = 0x00000005
CT_FIND_SCROLL_RELATIVE = 0x00000006

CT_OPEN_NO_OPTION = 0x00000000
CT_OPEN_CRYPT = 0x00000001
CT_OPEN_RECONNECT = 0x00000002
CT_OPEN_READ_ONLY = 0x00000004
CT_OPEN_BATCH = 0x00000008

CT_LIST_EVENT = 0x00000001
CT_LIST_LIGHTWEIGHT_MODE = 0x00000002

CT_LIST_EVENT_NEW = 0x00000001
CT_LIST_EVENT_STATUS = 0x00000002

CT_LIST_VALUE = 0x00000001
CT_LIST_TIMESTAMP = 0x00000002
CT_LIST_VALUE_TIMESTAMP = 0x00000003
CT_LIST_QUALITY_TIMESTAMP = 0x00000004
CT_LIST_QUALITY_GENERAL = 0x00000005
CT_LIST_QUALITY_SUBSTATUS = 0x00000006
CT_LIST_QUALITY_LIMIT = 0x00000007
CT_LIST_QUALITY_EXTENDED_SUBSTATUS = 0x00000008
CT_LIST_QUALITY_DATASOURCE_ERROR = 0x00000009
CT_LIST_QUALITY_OVERRIDE = 0x0000000A
CT_LIST_QUALITY_CONTROL_MODE = 0x0000000B

PROPERTY_NAME_LEN = 256

COMMON_WIN32_ERRORS = {
    "21" : "ERROR_INVALID_ACCESS",  # Tag doesnt exist??
    "111" : "ERROR_BUFFER_OVERFLOW",  # Result buffer not big enough",
    "233" : "ERROR_PIPE_NOT_CONNECTED",  # Connection to client is not established or client has not logged in correctly.
}

CITECT_ERRORS = {
    "424" : "Tag not found"
}

class CTAPIWrapper:
    '''A plain ctypes wrapper around the CitectSCADA CtAPI DLLs'''
    def __init__(self, dll_path):
        CDLL(dll_path + '/CiDebugHelp')
        CDLL(dll_path + '/CtUtil32')
        CDLL(dll_path + '/Ct_ipc')
        CDLL(dll_path + '/CtApi')
        CDLL(dll_path + '/CtEng32')
        CDLL(dll_path + '/CtRes32')
        CDLL(dll_path + '/CtUtilManagedHelper')

    def ctOpen(self, host_address, username, password, mode=0):
        return windll.CtApi.ctOpen(host_address.encode("ascii"), username.encode("ascii"), password.encode("ascii"), mode)

    def ctClose(self, connection):
        return windll.CtApi.ctClose(connection)

    def ctCicode(self, connection, function, buff, hWin=0, overlapped=None):
        return windll.CtApi.ctCicode(connection, function.encode("ascii"), hWin, 0, byref(buff), sizeof(buff), overlapped)

    def ctTagWrite(self, connection, tag_name, value):
        return windll.CtApi.ctTagWrite(connection, tag_name.encode("ascii"), str(value).encode("ascii"))

    def ctTagRead(self, connection, tag_name, buff):
        return windll.CtApi.ctTagRead(connection, tag_name.encode("ascii"), byref(buff), sizeof(buff))

    def ctListNew(self, connection, mode):
        return windll.CtApi.ctListNew(connection, mode)

    def ctListFree(self, _list):
        return windll.CtApi.ctListFree(_list)

    def ctListAdd(self, _list, tag_name):
        return windll.CtApi.ctListAdd(_list, tag_name.encode("ascii"))

    def ctListDelete(self, tag_handle):
        return windll.CtApi.ctListDelete(tag_handle)

    def ctListRead(self, _list, overlapped=None):
        return windll.CtApi.ctListRead(_list, overlapped)

    def ctListWrite(self, tag_handle, value, overlapped=None):
        return windll.CtApi.ctListWrite(tag_handle, str(value).encode("ascii"), overlapped)

    def ctListData(self, tag_handle, buff):
        return windll.CtApi.ctListData(tag_handle, byref(buff), sizeof(buff), 0)

    def ctListEvent(self, connection, mode):
        return windll.CtApi.ctListEvent(connection, mode)

    def getErrorCode(self):
         return GetLastError()

