
gst-launch-1.0 v4l2src device="/dev/video0" ! image/jpeg,width=640,height=480,framerate=30/1 ! \
	jpegdec ! autovideosink sync=false
