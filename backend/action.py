# from robot import MyRobot

def recevoir(robot):
    robot.motor_lanceur.set(-0.7)
    print(4)
    if not robot.limit_lanceur.get():
        robot.receveur=0
        robot.motor_lanceur.set(0)

def deposer(robot):
    robot.motor_lanceur.set(-1)
    if robot.limit_lanceur.get():
        robot.deposeur=0
        robot.motor_lanceur.set(0)

def elevateur(robot):
    retenue=0.2
    if robot.level==4:
        robot.motor_elevateur.set(retenue+(robot.encodeur_elevateur.get()+11300)/1000)
    elif robot.level==3:
        robot.motor_elevateur.set(retenue+(robot.encodeur_elevateur.get()+6500)/1000)
    elif robot.level==2:
        robot.motor_elevateur.set(retenue+(robot.encodeur_elevateur.get()+3000)/1000)
    elif robot.level==1:
        robot.motor_elevateur.set(retenue+(robot.encodeur_elevateur.get()+1000)/1000)
    else:
        robot.motor_elevateur.set((robot.encodeur_elevateur.get()+000)/3000)

def attrape(robot):
    if robot.attrapper<100:
        robot.motor_ballon_roue.set(0.8)
        robot.motor_balon_bras.set(0.4)
        robot.attrapper+=1
    else:
        robot.motor_ballon_roue.set(0.2)
        robot.motor_balon_bras.set(0)
        robot.attrapper=0

def lancer(robot):
    if robot.lancer<100:
        robot.motor_ballon_roue.set(-1)
        robot.motor_balon_bras.set(0)
        robot.lancer+=1
    else:
        robot.motor_ballon_roue.set(0)
        robot.motor_balon_bras.set(0)
        robot.lancer=0

def soulever(robot):
    if robot.soulever<500:
        robot.motor_levage_1.set(0.8)
        robot.motor_levage_2.set(0.8)
        robot.soulever+=1
    else:
        robot.motor_levage_1.set(0.2)
        robot.motor_levage_2.set(0.2)