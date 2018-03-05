HOST=192.168.8.172
gst-launch-1.0 videotestsrc ! jpegenc ! \
	rtpjpegpay ! udpsink host=$HOST port=9000
