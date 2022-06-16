import cv2
import numpy as np


def get_collisions(video_path: str, duration: int) -> int:
    """
    Return the number of collisions in the video.
    """
    cap = cv2.VideoCapture(video_path)
    ret = True
    while ret:
        ret, frame = cap.read()
        cv2.imshow("DVD Screen", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return 0