#Modified by enmedina 17/12/2019

from json import loads as jloads, dumps as jdumps
from os import path
import datetime
import socket
#using docstring Sphinx Style


def datetime2str(obj):
    """
    Identify if an object is an instance of datetime, it does return it string representation.

    :return object obj: an unknown object data type

    :return string: datetime as string
    """
    if isinstance(obj, datetime.datetime):
        return obj.__str__()   

def abs_path(filename, root_dir = None):
    """
    Get the absolute path of relative file path in project

    :param string filename: relative path of the file with it the project tree directory file
    :param string root_dir: root for searching the desired relative path

    :return string: absolute path of the referred file
    """
    wanted_file = ""
    root_directory = root_dir
    if root_directory is None:
            root_directory = __file__
    try:
            this_file = path.abspath(root_directory)
            this_dir = path.dirname(this_file)
            wanted_file = path.join(this_dir, filename)
    except Exception as e:
            print('helper error:', str(e))
            raise
    return wanted_file

def str2hex(number):
    """
    Convert an hex based string number to int

    :param string number: string hex number to convert

    :return int: Integer value of the hex number
    """
    return int(number, 16)

def json2dict(file_path, root_dir = None):
    """
    Read json file in the project structure and casting in as dict

    :param string file_path: relative path of the json file with it the project tree directory file
    :param string root_dir: root for searching the desired relative path

    :return dict: dictionary structure of the specified json file
    """
    file_path = abs_path(file_path, root_dir)
    raw_data = str()
    try:
            with open(file_path) as file_temp:
                    raw_data = file_temp.read()
            raw_dict = jloads(raw_data)
    except Exception as e:
            print('helper error:', str(e))
            raise
    return raw_dict

def get_server_ip():
    """
    Get Server IP address

    :return string: the server IP address
    """
    serverIP = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
    if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
    s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
    socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    return serverIP
