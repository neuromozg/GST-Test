#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst
import time

# константы
PORT = 9000

#инициализация Gstreamer
Gst.init(None)

# Создание GStreamer pipeline
pipeline = Gst.Pipeline()

# Создание элементов
src = Gst.ElementFactory.make('udpsrc')
srcCaps = Gst.Caps.from_string('application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)JPEG')
src.set_property('caps', srcCaps)
src.set_property('port', PORT)

depay = Gst.ElementFactory.make('rtpjpegdepay')
decoder = Gst.ElementFactory.make('jpegdec')
videoconvert = Gst.ElementFactory.make('videoconvert')

sink = Gst.ElementFactory.make('autovideosink')
sink.set_property('sync', False)

# Добавляем элементы в цепочку
elemList = [src, depay, decoder, videoconvert, sink]
for elem in elemList:
    pipeline.add(elem)

# Сединяем элементы
src.link(depay)
depay.link(decoder)
decoder.link(videoconvert)
videoconvert.link(sink)

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




