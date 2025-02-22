import robotpy_apriltag
# On peut tester avec un apriltag generator sur Google, le mettre devant la caméra et voir si l'april tag est détecté (dessiné) sur l'image
# ATTENTION : Bien utiliser la bonne famille de tag (tag36h11) et la bonne taille de tag

class AprilTagDetector:
    def __init__(self):
        self.detector = robotpy_apriltag.AprilTagDetector()
        self.detector.addFamily("tag36h11",3)
        
    def detect_april_tag(self,image):
        # april_tags=detector.detect(image)
        print(1)
        # for april_tag in april_tags:
            # print(f"april tag: {april_tag}")

    