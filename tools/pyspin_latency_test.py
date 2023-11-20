#%%
import os
import time
import PySpin
import cv2
import numpy as np

def acquire_images(cam, save_dir, max_frames=100):

    cam.Init()
    start_time = time.time()

    cam.BeginAcquisition()

    frame_counter = 0
    first_frame_latency = None
    try:
        while frame_counter < max_frames:
            end_time = time.time()
            image_result = cam.GetNextImage()
            if frame_counter == 0:
                first_frame_latency = (end_time - start_time) * 1000  # Convert to milliseconds

            if image_result.IsIncomplete():
                print("Image incomplete with image status %d..." % image_result.GetImageStatus())
            else:
                image_np = np.array(image_result.GetNDArray())
                file_name = os.path.join(save_dir, f'frame{frame_counter:04d}.png')
                cv2.imwrite(file_name, image_np)
                frame_counter += 1
            image_result.Release()

    finally:
        cam.EndAcquisition()
        cam.DeInit()

    return first_frame_latency

save_directory = 'recorded_images'
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

system = PySpin.System.GetInstance()
cam_list = system.GetCameras()

if cam_list.GetSize() == 0:
    print("No cameras found.")
    cam_list.Clear()
    system.ReleaseInstance()
    exit()

script_start_time = time.time()
cam = cam_list.GetByIndex(0)
first_frame_latency = acquire_images(cam, save_directory)

print(f"Latency from script start to first frame acquired: {first_frame_latency:.2f} ms")

cam_list.Clear()
system.ReleaseInstance()
