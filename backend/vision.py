import ntcore
import robotpy_apriltag
from cscore import CameraServer
import cv2
import numpy as np

def main():
    
    detector = robotpy_apriltag.AprilTagDetector()
    detector.addFamily("tag36h11", 3)
    # poseEstConfig = robotpy_apriltag.AprilTagPoseEstimator.Config(0.1651,699.3778103158814,677.7161226393544,345.6059345433618,207.12741326228522,)
    # estimator = robotpy_apriltag.AprilTagPoseEstimator(poseEstConfig)
    camera = CameraServer.startAutomaticCapture()
    camera.setResolution(640, 480)
    cvSink = CameraServer.getVideo()
    outputStream = CameraServer.putVideo("Detected", 640, 480)
    mat = np.zeros((480, 640, 3), dtype=np.uint8)
    grayMat = np.zeros(shape=(480, 640), dtype=np.uint8)
    tags = []
    outlineColor = (0, 255, 0)  # Color of Tag Outline
    crossColor = (0, 0, 25)  # Color of Cross
    # tagsTable = ntcore.NetworkTableInstance.getDefault().getTable("apriltags")
    # pubTags = tagsTable.getIntegerArrayTopic("tags").publish()
    while True:
        # if cvSink.grabFrame(mat) == 0:
        #     outputStream.notifyError(cvSink.getError())
        #     print(2)
        #     continue
        time,mat=cvSink.grabFrame(mat)
        cv2.cvtColor(mat, cv2.COLOR_RGB2GRAY, dst=grayMat)
        detections = detector.detect(grayMat)
        # tags.clear()
        for detection in detections:
            tags.append(detection.getId())
            # for i in range(4):
                # j = (i + 1) % 4
                # point1 = (int(detection.getCorner(i).x), int(detection.getCorner(i).y))
                # point2 = (int(detection.getCorner(j).x), int(detection.getCorner(j).y))
                # mat = cv2.line(mat, point1, point2, outlineColor, 2)
            # cx = int(detection.getCenter().x)
            # cy = int(detection.getCenter().y)
            # ll = 10
            # mat = cv2.line(mat,(cx - ll, cy),(cx + ll, cy),crossColor,2,)
            # mat = cv2.line(mat,(cx, cy - ll),(cx, cy + ll),crossColor,2,)
            # mat = cv2.putText(mat,str(detection.getId()),(cx + ll, cy),cv2.FONT_HERSHEY_SIMPLEX,1,crossColor,3,)
            # pose = estimator.estimate(detection)
            # rot = pose.rotation()
            # tagsTable.getEntry(f"pose_{detection.getId()}").setDoubleArray([pose.X(), pose.Y(), pose.Z(), rot.X(), rot.Y(), rot.Z()])
        # pubTags.set(tags)
        print(1)
        # print(tags)
        outputStream.putFrame(mat)