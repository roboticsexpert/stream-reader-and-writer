import cv2
from threading import Thread
import time


class StreamReader:
    def __init__(self,source,maxWidth):
        # store the value
        self.stream = cv2.VideoCapture(source)
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*"MJPG"))
        width=self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        height= self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)

        
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH,maxWidth)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT,maxWidth / width * height)

        width=self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        height= self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)

        fps = self.stream.get(cv2.CAP_PROP_FPS)
        fps = fps if fps > 0 else 10
    
        
        ret, frame = self.stream.read()
        self.FPS = fps
        self.realFPS=fps
        self.width=width
        self.height=height
        self.img=frame
        thread = Thread(target=self.update, args=([]), daemon=True)
        thread.start()
        print(f"Stream reader initilized with FPS : { fps } width: {width} height: {height}")

    # override the run function
    def update(self):
        capturedFramed=0;
        lastFPSCalculatedAt=time.time()
        while True:
            ret, self.img = self.stream.read()
            capturedFramed+=1

            if time.time()-lastFPSCalculatedAt >=1:
                fps=capturedFramed/(time.time()-lastFPSCalculatedAt)
                capturedFramed=0
                lastFPSCalculatedAt=time.time()
                print (f"Real read FPS: {fps}")

            
class StreamViewer:
    def __init__(self, streamReader:StreamReader,maxWidth=None):
        self.streamReader=streamReader
        
        if maxWidth==None:
            maxWidth=streamReader.width

        ratio=maxWidth/streamReader.width
        self.height=int(ratio*streamReader.height)
        self.width=int(maxWidth)
        thread = Thread(target=self.update, args=([]), daemon=True)
        thread.start()
        print(f"Stream viewer initilized with FPS : { streamReader.FPS } width: {self.width} height: {self.height}")

    def update(self):
        capturedFramed=0
        lastFPSCalculatedAt=time.time()
        while(True):
            
            # Capture the video frame
            # by frame
            frame = streamReader.img
            
            # Display the resulting frame
            cv2.imshow('frame', cv2.resize(frame,(self.width,self.height)))

            capturedFramed+=1

            if time.time()-lastFPSCalculatedAt >=1:
                fps=capturedFramed/(time.time()-lastFPSCalculatedAt)
                capturedFramed=0
                lastFPSCalculatedAt=time.time()
                print (f"Show read FPS: {fps}")
            
            time.sleep(1/streamReader.FPS)
            # the 'q' button is set as the````````````````````````````````````````````````````````````````````````````````````````````````````````````
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        # Destroy all the windows
        cv2.destroyAllWindows()


            


        


streamReader=StreamReader("/dev/video1",1920)
streamViewer=StreamViewer(streamReader,1920)


while True:

    time.sleep(1)
