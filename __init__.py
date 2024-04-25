#这个init为什么python不能把它做成一个脚手架呢？
from multiprocessing import Process, Queue
import numpy as np
import FluentUI
import os
import json
import sys
import cv2
import time
import serial
import serial.tools.list_ports
import atexit
from res.resdata_rc import*
from res.function.FileWatcher import FileWatcher
from res.function.NBri import*
from res.function import cksdk
from ctypes import *