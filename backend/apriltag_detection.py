import robotpy_apriltag
import cv2
import cv2
import numpy as np

from cscore import CameraServer as CS


# On peut tester avec un apriltag generator sur Google, le mettre devant la caméra et voir si l'april tag est détecté (dessiné) sur l'image
# ATTENTION : Bien utiliser la bonne famille de tag (tag36h11) et la bonne taille de tag

class AprilTagDetector:
    def __init__(self):
        self.detector = robotpy_apriltag.AprilTagDetector()
        self.detector.addFamily("tag36h11")
        
    def detect_on_robot_camera(self):
        ####### Just copied from the example code #######
        ####### Still need to be adapted to detect the tags #######
        
        # TODO: Add the code to detect the tags
        
        CS.enableLogging()

        # Get the UsbCamera from CameraServer
        camera = CS.startAutomaticCapture()
        # Set the resolution
        camera.setResolution(640, 480)

        # Get a CvSink. This will capture images from the camera
        cvSink = CS.getVideo()
        # Setup a CvSource. This will send images back to the Dashboard
        outputStream = CS.putVideo("Rectangle", 640, 480)

        # Allocating new images is very expensive, always try to preallocate
        mat = np.zeros(shape=(480, 640, 3), dtype=np.uint8)

        while True:
            # Tell the CvSink to grab a frame from the camera and put it
            # in the source image.  If there is an error notify the output.
            time, mat = cvSink.grabFrame(mat)
            if time == 0:
                # Send the output the error.
                outputStream.notifyError(cvSink.getError())
                # skip the rest of the current iteration
                continue

            # Put a rectangle on the image
            cv2.rectangle(mat, (100, 100), (400, 400), (255, 255, 255), 5)

            # Give the output stream a new image to display
            outputStream.putFrame(mat)
    
    def detect_on_pc_camera(self):
        # Open the camera (on a classic computer)
        cap = cv2.VideoCapture(0)
        
        # analyse the video stream frame by frame
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            self.detect_on_frame(frame)
            
            # Display the frame
            cv2.imshow('frame', frame)
            
            # Exit if the user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def detect_on_frame(self, image: cv2.typing.MatLike):
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect the tags
        detections = self.detector.detect(gray)
        
        # Draw the tags
        for detection in detections:
            self.draw_dectection(image, detection)
        
        return image
    
    def draw_dectection(self, image: cv2.typing.MatLike, detection: robotpy_apriltag.AprilTagDetection):
        for i in range(3):
            j = (i + 1) % 4
            pt1 = (int(detection.getCorner(i).x), int(detection.getCorner(i).y))
            pt2 = (int(detection.getCorner(j).x), int(detection.getCorner(j).y))
            cv2.line(image, pt1, pt2, (0, 255, 0), thickness=2)
        cv2.putText(image, str(detection.getId()), (int(detection.getCenter().x), int(detection.getCenter().y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=2)
        return image


def apriltag_detection():
    detector = AprilTagDetector()
    detector.detect_on_robot_camera()

if __name__ == "__main__":
    apriltag_detection()
    