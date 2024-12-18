#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""
import threading
import os
import wpilib
import wpilib.drive
from apriltag_detection import apriltag_detection
from swerve import ride
from swerve import path
from swerve import auto_drive
import navx
import phoenix5._ctre.sensors as ctre # type: ignore
import math
if os.name == 'posix':
    from rev._rev import CANSparkMax
    from rev._rev import CANSparkLowLevel
else:
    from rev import CANSparkMax
    from rev import CANSparkLowLevel

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        # self.navx_device = navx.AHRS(port=navx.Port.kMXP)
        self.navx_device = navx.AHRS(i2c_port_id=wpilib.I2C.Port(1))
        self.navx_device.zeroYaw()
        self.navx_device.resetDisplacement()
        
        self.motor_drive_av_gauche = CANSparkMax(10, CANSparkLowLevel.MotorType.kBrushless)
        self.motor_rot_av_gauche = CANSparkMax(11, CANSparkLowLevel.MotorType.kBrushless)

        self.encodeur_drive_av_gauche=self.motor_drive_av_gauche.getEncoder()
        self.encodeur_drive_av_gauche.setPositionConversionFactor(16.74)
        self.encodeur_drive_av_gauche.setPosition(0)
        self.encodeur_rot_av_gauche=ctre.CANCoder(12)
        
        self.motor_drive_av_droit = CANSparkMax(20, CANSparkLowLevel.MotorType.kBrushless)
        self.motor_rot_av_droit = CANSparkMax(21, CANSparkLowLevel.MotorType.kBrushless)

        self.encodeur_drive_av_droit=self.motor_drive_av_droit.getEncoder()
        self.encodeur_drive_av_droit.setPositionConversionFactor(16.74)
        self.encodeur_drive_av_droit.setPosition(0)
        self.encodeur_rot_av_droit=ctre.CANCoder(22)
        

        self.motor_drive_ar_gauche = CANSparkMax(40, CANSparkLowLevel.MotorType.kBrushless)
        self.motor_rot_ar_gauche = CANSparkMax(41, CANSparkLowLevel.MotorType.kBrushless)

        self.encodeur_drive_ar_gauche=self.motor_drive_ar_gauche.getEncoder()
        self.encodeur_drive_ar_gauche.setPositionConversionFactor(16.74)
        self.encodeur_drive_ar_gauche.setPosition(0)
        self.encodeur_rot_ar_gauche=ctre.CANCoder(42)
        

        self.motor_drive_ar_droit = CANSparkMax(30, CANSparkLowLevel.MotorType.kBrushless)
        self.motor_rot_ar_droit = CANSparkMax(31, CANSparkLowLevel.MotorType.kBrushless)

        self.encodeur_drive_ar_droit=self.motor_drive_ar_droit.getEncoder()
        self.encodeur_drive_ar_droit.setPositionConversionFactor(16.74)
        self.encodeur_drive_ar_droit.setPosition(0)
        self.encodeur_rot_ar_droit=ctre.CANCoder(32)
        
        self.controller = wpilib.XboxController(0)

        self.a1=0
        self.a2=0
        self.a3=0
        self.a4=0
        self.obj=path()

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        auto_drive(self)
        # self.timer.reset()
        # self.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass
        # # Drive for two seconds
        # if self.timer.get() < 2.0:
        #     self.drive.arcadeDrive(-0.5, 0)  # Drive forwards at half speed
        # else:
        #     self.drive.arcadeDrive(0, 0)  # Stop robot

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        y=self.controller.getLeftY()/math.sqrt(2)*1.5
        x=self.controller.getLeftX()/math.sqrt(2)*1.5
        z=self.controller.getRawAxis(2)/2/2
        ride(self,x,y,z)
        

if __name__ == "__main__":
    # start the apriltag detection on a separate thread to be able to run the robot code at the same time
    apriltag_thread = threading.Thread(target=apriltag_detection)
    apriltag_thread.start()
    
    wpilib.run(MyRobot)
    