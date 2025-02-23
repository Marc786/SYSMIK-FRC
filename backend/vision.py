from cscore import CameraServer
import cv2
import numpy as np
from photonlibpy import PhotonCamera


def main():
    camera = CameraServer.startAutomaticCapture()
    camera.setResolution(640, 480)
    cvSink = CameraServer.getVideo()
    outputStream = CameraServer.putVideo("Detected", 640, 480)
    mat = np.zeros((480, 640, 3), dtype=np.uint8)
    grayMat = np.zeros(shape=(480, 640), dtype=np.uint8)
    outlineColor = (0, 255, 0)  # Color of Tag Outline
    crossColor = (0, 0, 255)  # Color of Cross

    # Initialize PhotonVision
    photon_camera = PhotonCamera("photonvision")

    while True:
        time, mat = cvSink.grabFrame(mat)
        if time == 0:
            outputStream.notifyError(cvSink.getError())
            continue

        cv2.cvtColor(mat, cv2.COLOR_RGB2GRAY, dst=grayMat)

        # Process the image with PhotonVision
        result = photon_camera.getLatestResult()
        detections = result.getTargets()

        for detection in detections:
           # Get the bounding box coordinates
            corners = detection.getDetectedCorners()
            if len(corners) == 4:
                top_left = (int(corners[0].x), int(corners[0].y))
                top_right = (int(corners[1].x), int(corners[1].y))
                bottom_right = (int(corners[2].x), int(corners[2].y))
                bottom_left = (int(corners[3].x), int(corners[3].y))

                # Draw the outline of the tag
                cv2.line(mat, top_left, top_right, outlineColor, 2)
                cv2.line(mat, top_right, bottom_right, outlineColor, 2)
                cv2.line(mat, bottom_right, bottom_left, outlineColor, 2)
                cv2.line(mat, bottom_left, top_left, outlineColor, 2)

                # Draw the cross in the center of the tag
                center_x = int((top_left[0] + bottom_right[0]) / 2)
                center_y = int((top_left[1] + bottom_right[1]) / 2)
                cv2.drawMarker(mat, (center_x, center_y), crossColor, markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)

        outputStream.putFrame(mat)
