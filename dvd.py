import cv2
import numpy as np


def get_collisions(video_path: str, duration: int) -> int:
    """
    Return the number of collisions in the video.
    """
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    font = cv2.FONT_HERSHEY_SIMPLEX
    collisions = 0
    frame_num = 0
    left, right, top, bottom = False, False, False, False
    
    ret = True
    while ret:
        ret, frame = cap.read()
        height, width = frame.shape[:2]
        frame_num += 1

        (B, G, R) = cv2.split(frame)

        enhance = cv2.bitwise_or(B, cv2.bitwise_or(G, R))
        returned, thresh = cv2.threshold(enhance, 150, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(image=frame, contours=contours, contourIdx=-1, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)

        for cnt in contours : 
            approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)  

            n = approx.ravel() 
            i = 0

            for j in n : 
                if(i % 2 == 0): 
                    x = n[i] 
                    y = n[i + 1] 

                    if x < 5 and left == False:
                        collisions += 1
                        left = True
                        right, top, bottom = False, False, False
                    if y < 5 and top == False:
                        collisions += 1
                        top = True
                        right, left, bottom = False, False, False
                    if x > width-5 and right == False:
                        collisions += 1
                        right = True
                        left, top, bottom = False, False, False
                    if y > height-5 and bottom == False:
                        collisions += 1
                        bottom = True
                        right, left, top = False, False, False
                i = i + 1


        cv2.putText(frame, (f"Collisions: {collisions}"), (5, 30), font, 1, (255, 255, 255), 2)
        cv2.imshow("DVD Screen", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        progress = "{:.2f}".format(frame_num/fps)
        print(f"Playback: {progress}/{duration} Seconds", end="\r")
        if frame_num > duration*fps:
            break

    cap.release()
    cv2.destroyAllWindows()

    return collisions