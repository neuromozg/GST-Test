#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst
import time

# константы
DEVICE = '/dev/video0'
WIDTH = 640
HEIGHT = 480
FRAMERATE = 30
HOST = '127.0.0.1'
PORT = 9000

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

pipeline.set_state(Gst.State.PLAYING)
print('GST pipeline PLAYING')

#главный цикл программы    
try:
    while True:
        time.sleep(0.1)
except (KeyboardInterrupt, SystemExit):
    print('Ctrl+C pressed')
    
pipeline.set_state(Gst.State.NULL)
print('GST pipeline NULL')




