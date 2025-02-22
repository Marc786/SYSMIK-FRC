#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""
import wpilib
import wpilib.drive
from rev import SparkLowLevel
from rev import SparkMax, SparkMaxConfig
from swerve import ride
from swerve import path
from swerve import auto_drive
from action import recevoir
from action import deposer
from action import elevateur
from action import attrape
from action import lancer
from action import soulever
import navx
from phoenix6.hardware.cancoder import CANcoder
from wpilib.cameraserver import CameraServer
from rev import SparkBase
import phoenix6

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.navx_device = navx.AHRS(navx._navx.AHRS.NavXComType.kMXP_SPI)
        self.navx_device.zeroYaw()
        self.navx_device.resetDisplacement()
        self.config = SparkMaxConfig()
        self.config.encoder.positionConversionFactor(16.74)
        
        CameraServer.launch("vision.py:main")

        self.motor_levage_1=SparkMax(2,SparkMax.MotorType.kBrushed)
        self.motor_levage_2=SparkMax(3,SparkMax.MotorType.kBrushed)
        self.motor_ballon_roue=SparkMax(4,SparkMax.MotorType.kBrushed)
        self.motor_balon_bras=SparkMax(5,SparkMax.MotorType.kBrushed)

        self.motor_lanceur=SparkMax(6,SparkMax.MotorType.kBrushed)
        self.limit_lanceur=wpilib.DigitalInput(2)
        self.receveur=0
        self.deposeur=0
        self.attrapper=0
        self.lancer=0
        # self.soulever=0
        self.navx_device.getYaw()
        self.motor_elevateur=SparkMax(7,SparkMax.MotorType.kBrushed)
        self.level=0
        self.encodeur_elevateur=wpilib.Encoder(0,1)
        self.encodeur_elevateur.reset()

        self.motor_drive_av_gauche = SparkMax(10, SparkLowLevel.MotorType.kBrushless)
        self.motor_rot_av_gauche = SparkMax(11, SparkLowLevel.MotorType.kBrushless)
        
        self.encodeur_drive_av_gauche=self.motor_drive_av_gauche.getEncoder()
        
        self.motor_rot_av_gauche.configure(self.config,SparkBase.ResetMode.kNoResetSafeParameters,SparkBase.PersistMode.kNoPersistParameters)
        self.encodeur_drive_av_gauche.setPosition(0)
        self.encodeur_rot_av_gauche=CANcoder(12)
        
        self.motor_drive_av_droit = SparkMax(20, SparkLowLevel.MotorType.kBrushless)
        self.motor_rot_av_droit = SparkMax(21, SparkLowLevel.MotorType.kBrushless)

        self.encodeur_drive_av_droit=self.motor_drive_av_droit.getEncoder()
        self.motor_rot_av_droit.configure(self.config,SparkBase.ResetMode.kNoResetSafeParameters,SparkBase.PersistMode.kNoPersistParameters)
        self.encodeur_drive_av_droit.setPosition(0)
        self.encodeur_rot_av_droit=CANcoder(22)
        

        self.motor_drive_ar_gauche = SparkMax(40, SparkLowLevel.MotorType.kBrushless)
        self.motor_rot_ar_gauche = SparkMax(41, SparkLowLevel.MotorType.kBrushless)

        self.encodeur_drive_ar_gauche=self.motor_drive_ar_gauche.getEncoder()
        self.motor_rot_ar_gauche.configure(self.config,SparkBase.ResetMode.kNoResetSafeParameters,SparkBase.PersistMode.kNoPersistParameters)
        self.encodeur_drive_ar_gauche.setPosition(0)
        self.encodeur_rot_ar_gauche=CANcoder(42)
        

        self.motor_drive_ar_droit = SparkMax(30, SparkLowLevel.MotorType.kBrushless)
        self.motor_rot_ar_droit = SparkMax(31, SparkLowLevel.MotorType.kBrushless)

        self.encodeur_drive_ar_droit=self.motor_drive_ar_droit.getEncoder()
        self.motor_rot_ar_droit.configure(self.config,SparkBase.ResetMode.kNoResetSafeParameters,SparkBase.PersistMode.kNoPersistParameters)
        self.encodeur_drive_ar_droit.setPosition(0)
        self.encodeur_rot_ar_droit=CANcoder(32)
        
        self.controller = wpilib.XboxController(0)

        self.a1=0
        self.a2=0
        self.a3=0
        self.a4=0
        self.x=0
        self.y=0
        self.z=0
        self.px=0
        self.py=0
        

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.navx_device.resetDisplacement()
        self.navx_device.zeroYaw()
        self.px=0
        self.py=0
        self.obj=path()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        auto_drive(self)

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        y=self.controller.getLeftY()
        x=self.controller.getLeftX()
        z=self.controller.getRawAxis(2)

        ride(self,x,y,z)

        if self.controller.getAButton():
            self.navx_device.zeroYaw()
            self.px=0
            self.py=0
        
        # if self.controller.getRawButton(10):
        # #     # print(self.picture.detect_on_robot_camera())
        # #     pass




        if self.controller.getRawButton(3):
            if (self.limit_lanceur.get()):
                self.receveur=1
            else:
                self.deposeur=1

        if self.receveur==1:
            recevoir(self)
        
        elif self.deposeur==1:
            deposer(self)


        if self.controller.getRawButtonPressed(2):
            self.attrapper=1
            self.lancer=0
            
        
        if self.attrapper>0:
            attrape(self)

        if self.controller.getRawButtonPressed(4):
            self.lancer=1
            self.attrapper=0

        if self.lancer>0:
            lancer(self)
        if self.controller.getPOV()==0:
            self.motor_levage_2.set(-0.5)
            self.motor_levage_1.set(-0.5)
        elif self.controller.getPOV()==180:
            self.motor_levage_2.set(0.5)
            self.motor_levage_1.set(0.5)
        else:
            self.motor_levage_2.set(0)
            self.motor_levage_1.set(0)
        # self.motor_levage_2.set(0)
        #     self.soulever=1
            
        # if self.controller.getRawButtonPressed(5)and self.soulever==500:
        #     self.soulever=0

        # if self.soulever!=0:
        #     soulever()
        
        if self.controller.getRawButtonPressed(8):
            self.level+=1
            if self.level>3:
                self.level=3
        if self.controller.getRawButtonPressed(7):
            self.level-=1
            if self.level<0:
                self.level=0
        elevateur(self)



# def robotAndApriltag():
#     # start the apriltag detection on a separate thread to be able to run the robot code at the same time
#     apriltag_thread = threading.Thread(target=apriltag_detection)
#     apriltag_thread.start()
    
#     wpilib.run(MyRobot)

# def robotOnly():
#     wpilib.run(MyRobot)        

if __name__ == "__main__":
    wpilib.run(MyRobot)
