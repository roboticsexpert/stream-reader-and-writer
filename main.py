import cv2
from threading import Thread
import time


class StreamReader:
    def __init__(self, source, maxWidth):
        # store the value
        self.stream = cv2.VideoCapture(source)
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*"MJPG"))
        width = self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)

        
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, maxWidth)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, maxWidth / width * height)

        width = self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)

        fps = self.stream.get(cv2.CAP_PROP_FPS)
        fps = fps if fps > 0 else 10

        
        # if you increase buffer size it helps to consistent frames but if you reduece it it helps to get real time stream
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        ret, frame = self.stream.read()
        self.FPS = fps
        self.realFPS = fps
        self.width = width
        self.height = height
        self.img = frame
        self.frameId = 1
        thread = Thread(target=self.update, args=([]), daemon=True)
        thread.start()
        print(f"Stream reader started with FPS : {fps} width: {width} height: {height}")

    # override the run function
    def update(self):
        last_fps_calculated_at = time.time()
        while True:
            ret, self.img = self.stream.read()
            self.frameId += 1

            if time.time() - last_fps_calculated_at >= 1:
                fps = self.frameId / (time.time() - last_fps_calculated_at)
                self.frameId = 0
                last_fps_calculated_at = time.time()
                print(f"Real read FPS: {fps}")


class StreamViewer:
    def __init__(self, streamReader: StreamReader, max_width=None):
        self.streamReader = streamReader

        if max_width == None:
            max_width = streamReader.width

        ratio = max_width / streamReader.width
        self.height = int(ratio * streamReader.height)
        self.width = int(max_width)
        thread = Thread(target=self.update, args=([]), daemon=True)
        thread.start()
        print(f"Stream viewer initilized with FPS : {streamReader.FPS} width: {self.width} height: {self.height}")

    def update(self):
        captured_framed = 0
        last_frame_id = 0
        last_fps_calculated_at = time.time()
        while True:

            # Capture the video frame
            # by frame

            while last_frame_id == self.streamReader.frameId:
                time.sleep(0.5 / stream_reader.FPS)

            frame = self.streamReader.img
            last_frame_id = self.streamReader.frameId

            # Display the resulting frame
            cv2.imshow('frame', cv2.resize(frame, (self.width, self.height)))

            captured_framed += 1

            if time.time() - last_fps_calculated_at >= 1:
                fps = captured_framed / (time.time() - last_fps_calculated_at)
                captured_framed = 0
                last_fps_calculated_at = time.time()
                print(f"Show read FPS: {fps}")

            time.sleep(0.5 / stream_reader.FPS)
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Destroy all the windows
        cv2.destroyAllWindows()


stream_reader = StreamReader("/dev/video1", 1024)
stream_viewer = StreamViewer(stream_reader, 1024)

while True:
    time.sleep(5)
