import robotpy_apriltag
import cv2

if __name__ == "__main__":
    apriltag_detector = robotpy_apriltag.AprilTagDetector()
    apriltag_detector.addFamily("tag36h11")
    
    # open camera
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = apriltag_detector.detect(gray)
        for detection in detections:
            print(detection)
            for i in range(3):
                j = (i + 1) % 4
                pt1 = (int(detection.getCorner(i).x), int(detection.getCorner(i).y))
                pt2 = (int(detection.getCorner(j).x), int(detection.getCorner(j).y))
                cv2.line(frame, pt1, pt2, (0, 255, 0), thickness=2)
            cv2.putText(frame, str(detection.getId()), (int(detection.getCenter().x), int(detection.getCenter().y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=2)
                
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()