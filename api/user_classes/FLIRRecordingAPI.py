from api.api import Api
import cv2
import PySpin
import numpy as np
import time
import threading

timestr = time.strftime("%Y%m%d-%H%M%S")

class FLIRRecordingAPI(Api):
    '''API for the go_nogo_learning task to record the video.'''


    def __init__(self):
        self.recording_thread = 0
#    def run_start(self):
        # call
        #self.record_video_in_background()
    def record_video_in_background(self):
        def record_video():
            system = PySpin.System.GetInstance()
            cam_list = system.GetCameras()
            cam = cam_list.GetByIndex(0)

            cam.Init()

            # Get camera resolution
            width = int(cam.Width.GetValue())
            height = int(cam.Height.GetValue())

            # Create a VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(f'FLIR_videos\\{timestr}_output.avi', fourcc, 20.0, (width, height), isColor=False)

            cam.BeginAcquisition()

            cv2.namedWindow('FLIR', cv2.WINDOW_NORMAL)


            while cv2.getWindowProperty('FLIR', 0) >= 0:
                image_result = cam.GetNextImage()
                if image_result.IsIncomplete():
                    print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
                else:
                    rows, cols = image_result.GetHeight(), image_result.GetWidth()
                    image_data = np.array(image_result.GetData(), dtype="uint8").reshape((rows, cols))


                    # Apply Gaussian Blur
                    #image_data_blurred = cv2.GaussianBlur(image_data, (7, 7), 0)
                    
                    # Apply binary filter
                    #_, image_data_binary = cv2.threshold(image_data_blurred, 80, 190, cv2.THRESH_BINARY_INV)
                                        
                    cv2.imshow('FLIR', image_data)

                    # Write frame to video file
                    out.write(image_data)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    time.sleep(1)
                    image_result.Release()
                    cam.EndAcquisition()
                    cam.DeInit()
                    cv2.destroyAllWindows()
                    break
        self.recording_thread = threading.Thread(target=record_video)
        self.recording_thread.daemon = True # Ensure the thread will be terminated when the main program ends
        self.recording_thread.start()
    
    def run_start(self):
        self.record_video_in_background()

    def run_stop(self):
        self.recording_thread.join()
        