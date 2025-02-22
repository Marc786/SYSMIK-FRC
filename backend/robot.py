import wpilib
import wpilib.cameraserver

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):        
        wpilib.CameraServer.launch("vision.py:main")
    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        pass
