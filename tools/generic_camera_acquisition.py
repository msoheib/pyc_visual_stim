
#%%
import cv2

def display_real_time_video(camera_index):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Unable to open camera.")
        return

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Unable to acquire frame.")
                break

            cv2.imshow('Real-time Video', frame)

            # Press 'q' to exit the loop and close the video feed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

camera_index = 1  # Change this to the index of your USB camera
display_real_time_video(camera_index)
