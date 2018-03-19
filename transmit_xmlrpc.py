#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst
import time
from xmlrpc.server import SimpleXMLRPCServer
import subprocess

PORT = 8000

# константы
DEVICE = '/dev/video0'
WIDTH = 640
HEIGHT = 480
FRAMERATE = 30
HOST = '127.0.0.1'
PORT = 9000
XMLRPC_PORT = 8000

#инициализация Gstreamer
Gst.init(None)

# Создание GStreamer pipeline
pipeline = Gst.Pipeline()

# Создание элементов
src = Gst.ElementFactory.make('v4l2src')
src.set_property('device', DEVICE)

srcFilter = Gst.ElementFactory.make('capsfilter')
srcCaps = Gst.caps_from_string('image/jpeg, width=%d, height=%d, framerate=%d/1' %
                               (WIDTH, HEIGHT, FRAMERATE))
srcFilter.set_property('caps', srcCaps)

pay = Gst.ElementFactory.make('rtpjpegpay')

sink = Gst.ElementFactory.make('udpsink')
sink.set_property('host', HOST)
sink.set_property('port', PORT)

# Добавляем элементы в цепочку
pipeline.add(src)
pipeline.add(srcFilter)
pipeline.add(pay)
pipeline.add(sink)

# Сединяем элементы
src.link(srcFilter)
srcFilter.link(pay)
pay.link(sink)

cmd = 'hostname -I | cut -d\' \' -f1'
IP = subprocess.check_output(cmd, shell = True) #получаем IP
IP = IP.rstrip().decode("utf-8") #удаляем \n, переводим в текст

server = SimpleXMLRPCServer((IP, XMLRPC_PORT))
print('Listening on %s:%d' % (IP, XMLRPC_PORT))

def play(host):
    sink.set_property('host', host)
    pipeline.set_state(Gst.State.PLAYING)
    print('GST pipeline PLAYING')
    return 0

def stop():
    pipeline.set_state(Gst.State.PAUSED)
    print('GST pipeline PAUSED')
    pipeline.set_state(Gst.State.READY)
    print('GST pipeline READY')
    return 0

# register our functions
server.register_function(play)
server.register_function(stop)

#главный цикл программы    
try:
    # Run the server's main loop
    server.serve_forever()
except (KeyboardInterrupt, SystemExit):
    print('Ctrl+C pressed')
    
pipeline.set_state(Gst.State.NULL)
print('GST pipeline NULL')




