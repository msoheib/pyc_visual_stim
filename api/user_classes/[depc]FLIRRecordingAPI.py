#from api.api import Api
import cv2
import PySpin
import numpy as np
import threading
import time

timestr = time.strftime("%Y%m%d-%H%M%S")

class CameraFLIR():


    def __init__(self):
        self.cam = 0
        self.out  = 0
        self.image_result = 0
        system = PySpin.System.GetInstance()
        cam_list = system.GetCameras()
        CameraFLIR.cam = cam_list.GetByIndex(0)

        CameraFLIR.cam.Init()

        # Get camera resolution
        width = int(CameraFLIR.cam.Width.GetValue())
        height = int(CameraFLIR.cam.Height.GetValue())

        # Create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        CameraFLIR.out = cv2.VideoWriter(f'FLIR_videos\\{timestr}_output.avi', fourcc, 20.0, (width, height), isColor=False)

    def start_recording(self):
        CameraFLIR.cam.BeginAcquisition()
        cv2.namedWindow('FLIR', cv2.WINDOW_NORMAL)

        while cv2.getWindowProperty('FLIR', 0) >= 0:
            CameraFLIR.image_result = CameraFLIR.cam.GetNextImage()
            if CameraFLIR.image_result.IsIncomplete():
                print('Image incomplete with image status %d ...' % CameraFLIR.image_result.GetImageStatus())
            else:
                rows, cols = CameraFLIR.image_result.GetHeight(), CameraFLIR.image_result.GetWidth()
                image_data = np.array(CameraFLIR.image_result.GetData(), dtype="uint8").reshape((rows, cols))
                cv2.imshow('FLIR', image_data)
                CameraFLIR.out.write(image_data)
        

    def stop_recording(self):
        CameraFLIR.image_result.Release()
        CameraFLIR.cam.EndAcquisition()
        CameraFLIR.cam.DeInit()
        cv2.destroyAllWindows()

class FLIRRecordingAPI(Api):
     '''API for the go_nogo_learning task to record the video.'''
     flir = 0
     def __init__(self):
         flir = CameraFLIR()
     def run_start(self):
        recording_thread = threading.Thread(target=flir.start_recording)
        recording_thread.daemon = True # Ensure the thread will be terminated when the main program ends
        recording_thread.start()
     def run_stop(self):
         flir.stop_recording()