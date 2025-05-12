import cv2
from tracker import *

tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("Swing.mp4")

# Détection d'objet depuis la caméra stable
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=200)
while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    # Extraire la région d'intéret
    roi = frame[0:1000, 1000:1920]

    # 1. Détection d'objet
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []

    # 2. Traquer l'objet
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
   
    for cnt in contours:
        # Retirer les éléments inintéressants
        area = cv2.contourArea(cnt)
        if area > 300:
            cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, z, h = cv2.boundingRect(cnt)
            cv2.rectangle(roi, (x, y), (x + z, y + h), (0, 255, 0), 3)
            detections.append([x, y, z, h])
            
    print(detections)
    cv2.imshow("roi", roi)
    cv2.imshow("mask",mask)
    
    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
