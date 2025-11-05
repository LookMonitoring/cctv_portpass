from flask import Flask, request, render_template, Response, jsonify
from flask_cors import CORS
import requests, json
import cv2,base64
import time
# from onvif import ONVIFCamera
# import zeep

app = Flask(__name__)
CORS(app)


  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

def gen_frames(USER,PASSWORD,IP):  # generate frame by frame from camera
    
    # Use GStreamer pipeline for RTSP (works when OpenCV is built with GStreamer)
    pipeline = (
        f"rtspsrc location=rtsp://{USER}:{PASSWORD}@{IP}:554 latency=200 ! "
        "rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink drop=true"
    )
    camera = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    # Fallback to plain OpenCV RTSP if GStreamer backend isn't available/open fails
    if not camera.isOpened():
        camera = cv2.VideoCapture('rtsp://' + USER + ':' + PASSWORD + '@' + IP + ':554')

    try:
        while True:
            # try reading frame with a few retries before giving up
            for attempt in range(5):
                success, frame = camera.read()
                if success and frame is not None:
                    break
                time.sleep(0.2)
            else:
                # failed several times — try re-opening the stream once
                try:
                    camera.release()
                except Exception:
                    pass
                camera = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
                if not camera.isOpened():
                    camera = cv2.VideoCapture('rtsp://' + USER + ':' + PASSWORD + '@' + IP + ':554')

                success, frame = camera.read()
                if not success or frame is None:
                    # stop streaming on repeated failure
                    break

            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        camera.release()



def gen_image(USER,PASSWORD,IP):  # generate frame by frame from camera
    camera = cv2.VideoCapture('rtsp://'+USER+':'+PASSWORD+'@'+IP+':554')

    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            break

XMAX = 0.3
XMIN = -0.3
YMAX = 0.3
YMIN = -0.3






@app.route('/video_feed',methods=['GET', 'POST'])
def video_feed():
    camera = request.args.get('camera')
    data = base64.b64decode(base64.b64decode(base64.b64decode(camera))).decode("utf-8")
    data = json.loads(data)
    ip = data.get("ip")
    user = data.get("username")
    password = data.get("password")


    return Response(gen_frames(user, password, ip), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/image_feed',methods=['GET', 'POST'])
def image_feed():
    camera = request.args.get('camera')
    data = base64.b64decode(base64.b64decode(base64.b64decode(camera))).decode("utf-8")
    data = json.loads(data)
    ip = data.get("ip")
    user = data.get("username")
    password = data.get("password")
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_image(user,password,ip), mimetype='multipart/x-mixed-replace; boundary=frame')


    


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


