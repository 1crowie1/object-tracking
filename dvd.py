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
    left, right, top, bottom = False, False, False, False  # store current collision state - prevents double counting

    print("Press \'Q\' to quit.")

    ret = True
    while ret:
        ret, frame = cap.read()
        height, width = frame.shape[:2]
        frame_num += 1

        (B, G, R) = cv2.split(frame)  # split frame into color channels

        enhance = cv2.bitwise_or(B, cv2.bitwise_or(G, R))  # display coloured sections as white
        returned, thresh = cv2.threshold(enhance, 150, 255, cv2.THRESH_BINARY)

        # find and contours in the thresholded image
        contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(image=frame, contours=contours, contourIdx=-1, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)

        # check if any of the contours are in the colision zone
        for cnt in contours : 
            approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)  

            n = approx.ravel() 
            i = 0

            # check each drawn coordinate of the contor
            for j in n : 
                if(i % 2 == 0): 
                    x = n[i] 
                    y = n[i + 1] 

                    # if contour coordinate in the collision zone and wall not already counted, increment collision count
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


        # display the number of collisions in the video
        cv2.putText(frame, (f"Collisions: {collisions}"), (5, 30), font, 1, (255, 255, 255), 2)
        cv2.imshow("DVD Screen", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        progress = "{:.2f}".format(frame_num/fps)  # show progress in the console
        print(f"Playback: {progress}/{duration} Seconds", end="\r")
        # if the user specified time is reached, break
        if frame_num > duration*fps:
            break

    cap.release()
    cv2.destroyAllWindows()
    
    # return the amount of collisions counted
    return collisions