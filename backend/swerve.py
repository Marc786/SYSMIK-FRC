import math

def PID_motor(mot,enc,obj):
    p=(obj-enc.getVelocity()/6500)*5
    mot.set(p*abs(p)+enc.getVelocity()/10000)

def PID_angle(mot,enc,obj):
    s=1
    p=(360-obj)-enc.getAbsolutePosition()%360
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
    com=-p*0.006-0.0000*enc.getVelocity()
    if abs(com)>0.001:
        mot.set(com)
    else:
        mot.set(0)
    return s

def ride(robot,x,y,z):
    offcet=robot.navx_device.getAngle()/360*2*math.pi
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
    else:
        a1=robot.a1
        a2=robot.a2
        a3=robot.a3
        a4=robot.a4
        v1=0
        v2=0
        v3=0
        v4=0
    # a1=offcet
    # a2=offcet
    # a3=offcet
    # a4=offcet
    PID_motor(robot.motor_drive_ar_droit,robot.encodeur_drive_ar_droit,v3*PID_angle(robot.motor_rot_ar_droit,robot.encodeur_rot_ar_droit,a3))
    PID_motor(robot.motor_drive_av_droit,robot.encodeur_drive_av_droit,v2*PID_angle(robot.motor_rot_av_droit,robot.encodeur_rot_av_droit,a2))
    PID_motor(robot.motor_drive_ar_gauche,robot.encodeur_drive_ar_gauche,-v4*PID_angle(robot.motor_rot_ar_gauche,robot.encodeur_rot_ar_gauche,a4))
    PID_motor(robot.motor_drive_av_gauche,robot.encodeur_drive_av_gauche,v1*PID_angle(robot.motor_rot_av_gauche,robot.encodeur_rot_av_gauche,a1))

def auto_drive(robot):
    obj=robot.obj
    py=robot.navx_device.getDisplacementY()
    px=robot.navx_device.getDisplacementX()
    a=robot.navx_device.getYaw()
    if obj!=[]:
        x=(obj[0][0]-px)*1
        y=(obj[0][1]-py)*1
        z=(obj[0][2]-a)/360*1
        if x>1: x=1
        if y>1: y=1
        if z>1: z=1
        if abs(obj[0][0]-px)<obj[0][3] and abs(obj[0][1]-py)<obj[0][3] and abs(obj[0][2]-a)/360<obj[0][3]:
            obj.pop(0)
    else:
        pass

def path():
    return [[0,0,0,0.1],[0,1,90,0.1],[1,1,0,0.1],[1,0,0,0.1],[0,0,0,0.01]]