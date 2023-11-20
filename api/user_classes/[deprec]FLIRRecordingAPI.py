from api.api import Api
import cv2
import PySpin
import numpy as np
import threading
import time

timestr = time.strftime("%Y%m%d-%H%M%S")

class CameraFLIR():
    def __init__(self):
        self.recording_thread = 0


    def record_video_in_background(self):
        def record_video():
            system = PySpin.System.GetInstance()
            cam_list = system.GetCameras()
            self.cam = cam_list.GetByIndex(0)

            self.cam.Init()

            # Get camera resolution
            width = int(self.cam.Width.GetValue())
            height = int(self.cam.Height.GetValue())

            # Create a VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(f'FLIR_videos\\{timestr}_output.avi', fourcc, 20.0, (width, height), isColor=False)

            self.cam.BeginAcquisition()

            cv2.namedWindow('FLIR', cv2.WINDOW_NORMAL)


            while cv2.getWindowProperty('FLIR', 0) >= 0:
                self.image_result = self.cam.GetNextImage()
                if self.image_result.IsIncomplete():
                    print('Image incomplete with image status %d ...' % self.image_result.GetImageStatus())
                else:
                    rows, cols = self.image_result.GetHeight(), self.image_result.GetWidth()
                    image_data = np.array(self.image_result.GetData(), dtype="uint8").reshape((rows, cols))


                    # Apply Gaussian Blur
                    #image_data_blurred = cv2.GaussianBlur(image_data, (7, 7), 0)
                    
                    # Apply binary filter
                    #_, image_data_binary = cv2.threshold(image_data_blurred, 80, 190, cv2.THRESH_BINARY_INV)
                                        
                    cv2.imshow('FLIR', image_data)

                    # Write frame to video file
                    self.out.write(image_data)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    time.sleep(1)
                    self.image_result.Release()
                    self.cam.EndAcquisition()
                    self.cam.DeInit()
                    cv2.destroyAllWindows()
                    break
        self.recording_thread = threading.Thread(target=record_video)
        self.recording_thread.daemon = True # ensure the thread will be terminated when the main program ends
        self.recording_thread.start()

    def stop_recording(self):
        self.image_result.Release()
        self.cam.EndAcquisition()
        self.cam.DeInit()
        cv2.destroyAllWindows()

class FLIRRecordingAPI(Api):
     '''API for the go_nogo_learning task to record the video.'''
     def __init__(self):
         self.flir = 0
     def run_start(self):
        self.flir = CameraFLIR()
        self.flir.record_video_in_background()
     def run_stop(self):
         self.flir.stop_recording()