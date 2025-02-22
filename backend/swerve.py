import math
# from robot import MyRobot
from rev import SparkMax
from phoenix6.hardware.cancoder import CANcoder
from rev._rev import SparkRelativeEncoder

def pos(robot):
    a1=(robot.encodeur_rot_av_gauche.get_absolute_position().value_as_double*360-robot.navx_device.getYaw())/360*2*math.pi
    a2=(robot.encodeur_rot_av_droit.get_absolute_position().value_as_double*360-robot.navx_device.getYaw())/360*2*math.pi
    a3=(robot.encodeur_rot_ar_droit.get_absolute_position().value_as_double*360-robot.navx_device.getYaw())/360*2*math.pi
    a4=(robot.encodeur_rot_ar_gauche.get_absolute_position().value_as_double*360-robot.navx_device.getYaw())/360*2*math.pi
    factor=12.5/12/100000
    v1=robot.encodeur_drive_av_gauche.getVelocity()*factor
    v2=robot.encodeur_drive_av_droit.getVelocity()*factor
    v3=robot.encodeur_drive_ar_droit.getVelocity()*factor
    v4=robot.encodeur_drive_ar_gauche.getVelocity()*factor
    robot.px+=v1*math.cos(a1)+v2*math.cos(a2)+v3*math.cos(a3)-v4*math.cos(a4)
    robot.py+=v1*math.sin(a1)+v2*math.sin(a2)+v3*math.sin(a3)-v4*math.sin(a4)

def PID_motor(mot:SparkMax,enc:SparkRelativeEncoder,obj):
    p=(obj-enc.getVelocity()/10000)*2
    mot.set(p*abs(p)+enc.getVelocity()/10000)

def PID_angle(mot:SparkMax,enc:CANcoder,obj):
    s=1
    p=(360-obj)-(enc.get_absolute_position().value_as_double*360)%360
    if abs(p)>180:
        if p>0:
            p-=360
        else:
            p+=360
    if abs(p)>90:
        if p>0:
            p-=180
            s=-1
        else:
            p+=180
            s=-1
    com=-p*0.006-0.0000*enc.get_velocity().value_as_double
    if abs(com)>0.001:
        mot.set(com)
    else:
        mot.set(0)
    return s

def ride(robot,x,y,z):
    pos(robot)
    val=0.08
    if abs(x-robot.x)<val:
        robot.x=x
    else:
        x=robot.x+val*abs(x-robot.x)/(x-robot.x)
        robot.x=x
    if abs(y-robot.y)<val:
        robot.y=y
    else:
        y=robot.y+val*abs(y-robot.y)/(y-robot.y)
        robot.y=y
    if abs(z-robot.z)<val/2:
        robot.z=z
    else:
        z=robot.z+val*abs(z-robot.z)/(z-robot.z)/2
        robot.z=z

    offcet=robot.navx_device.getYaw()/360*2*math.pi
    yt=y*math.cos(offcet)-x*math.sin(offcet)
    xt=x*math.cos(offcet)+y*math.sin(offcet)
    x=xt
    y=yt
    x1=(-y+z)
    y1=(-x-z)
    x2=(-y-z)
    y2=(-x-z)
    x3=(-y-z)
    y3=(-x+z)
    x4=(-y+z)
    y4=(-x+z)
    if abs(x)+abs(y)+abs(z)>0.05:
        a1=360-math.atan2(y1,x1)*360/2/math.pi
        a2=360-math.atan2(y2,x2)*360/2/math.pi
        a3=360-math.atan2(y3,x3)*360/2/math.pi
        a4=360-math.atan2(y4,x4)*360/2/math.pi
        robot.a1=a1
        robot.a2=a2
        robot.a3=a3
        robot.a4=a4
        v1=math.sqrt(x1**2+y1**2)
        v2=math.sqrt(x2**2+y2**2)
        v3=math.sqrt(x3**2+y3**2)
        v4=math.sqrt(x4**2+y4**2)
        div=max(v1,v2,v3,v4)
        if div>=1:
            v1=v1/div
            v2=v2/div
            v3=v3/div
            v4=v4/div
        robot.v1=v1
        robot.v2=v2
        robot.v3=v3
        robot.v4=v4
        
    else:
        a1=robot.a1
        a2=robot.a2
        a3=robot.a3
        a4=robot.a4
        v1=0
        v2=0
        v3=0
        v4=0
    PID_motor(robot.motor_drive_ar_droit,robot.encodeur_drive_ar_droit,v3*PID_angle(robot.motor_rot_ar_droit,robot.encodeur_rot_ar_droit,a3))
    PID_motor(robot.motor_drive_av_droit,robot.encodeur_drive_av_droit,v2*PID_angle(robot.motor_rot_av_droit,robot.encodeur_rot_av_droit,a2))
    PID_motor(robot.motor_drive_ar_gauche,robot.encodeur_drive_ar_gauche,-v4*PID_angle(robot.motor_rot_ar_gauche,robot.encodeur_rot_ar_gauche,a4))
    PID_motor(robot.motor_drive_av_gauche,robot.encodeur_drive_av_gauche,v1*PID_angle(robot.motor_rot_av_gauche,robot.encodeur_rot_av_gauche,a1))

def auto_drive(robot):
    obj=robot.obj
    py=robot.py
    px=robot.px
    a=robot.navx_device.getYaw()
    if obj!=[]:
        y=-(obj[0][0]-px)/2
        x=-(obj[0][1]-py)/2
        if obj[0][2]-a>=180:
            z=(-360+(obj[0][2]-a))/360*5
        elif obj[0][2]-a<=-180:
            z=(360+(obj[0][2]-a))/360*5
        else:
            z=(obj[0][2]-a)/360*5
        val=0.25
        if x>val: x=val
        if y>val: y=val
        if z>val/3: z=val/3
        if -x>val: x=-val
        if -y>val: y=-val
        if -z>val/3: z=-val/3
        ride(robot,x,y,z)
        if abs(obj[0][0]-px)<obj[0][3] and abs(obj[0][1]-py)<obj[0][3] and abs(obj[0][2]-a)/36<obj[0][3] and len(obj)>1:
            obj.pop(0)
    else:
        ride(robot,0,0,0)
        pass

def path():
    # return [[0,1,0,0.1],[1,1,0,0.1],[1,0,0,0.1],[0,0,0,0.1]]
    return [[4,0,0,1],[4,-4,90,1],[0,-4,180,1],[0,0,-90,1],[0,0,0,0.1]]


