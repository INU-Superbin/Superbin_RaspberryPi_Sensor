# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
import signal
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('./sexman.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://world-best-bin-default-rtdb.firebaseio.com'})

#GPIO 핀
TRIG_1 = 13 # 트리거
TRIG_2 = 19 
ECHO_1 = 16 # 에코
ECHO_2 = 26

#거리 타임 아웃 용
MAX_DISTANCE_CM = 300
MAX_DURATION_TIMEOUT = (MAX_DISTANCE_CM * 2 * 29.1) #17460 # 17460us = 300cm

# 키보드 CTRL + C 누르면 종료 되게 처리
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        GPIO.cleanup()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# cm 환산 함수
# 아두이노 UltraDistSensor 코드에서 가져옴
def distanceInCm(duration):
    # 물체에 도착후 돌아오는 시간 계산
    # 시간 = cm / 음속 * 왕복
    # t   = 0.01/340 * 2= 0.000058824초 (58.824us)

    # 인식까지의 시간
    # t = 0.01/340 = 0.000029412초 (29.412us)

    # duration은 왕복 시간이니 인식까지의 시간에서 2로 나눔
    return (duration/2)/29.1


# 거리 표시
def print_distance(TRIG,ECHO):
    if distance == 0:
        distanceMsg = 'Distance : out of range                   \r'
    else:
        distanceMsg = 'Distance : ' + str(distance) + 'cm' + '        \r'
    sys.stdout.write(distanceMsg)
    sys.stdout.flush()
    
    
def operation(TRIG,ECHO):
    
    time.sleep(0.25)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    timeout = time.time()
    while GPIO.input(ECHO) == 0:
            #들어왔으면 시작 시간을 변수에 저장
        pulse_start = time.time()
        if ((pulse_start - timeout)*1000000) >= MAX_DURATION_TIMEOUT:
                #171206 중간에 통신 안되는 문제 개선용        
                #continue
            fail = True
            break
                
        
        #ECHO로 인식 종료 시점까지 대기
    timeout = time.time()
    while GPIO.input(ECHO) == 1:
            #종료 시간 변수에 저장
        pulse_end = time.time()
        if ((pulse_end - pulse_start)*1000000) >= MAX_DURATION_TIMEOUT:
            #print_distance(0) 
                #171206 중간에 통신 안되는 문제 개선용        
                #continue
            fail = True
            break
        
 

        #인식 시작부터 종료까지의 차가 바로 거리 인식 시간
    pulse_duration = (pulse_end - pulse_start) * 1000000

        # 시간을 cm로 환산
    distance = distanceInCm(pulse_duration)
        #print(pulse_duration)
        #print('')
        # 자리수 반올림
    distance = round(distance, 2)
    return distance



def main():
    # 파이썬 GPIO 모드
    GPIO.setmode(GPIO.BCM)

    # 핀 설정
    GPIO.setup(TRIG_1, GPIO.OUT) # 트리거 출력
    GPIO.setup(TRIG_2, GPIO.OUT)
    GPIO.setup(ECHO_1, GPIO.IN)  # 에코 입력
    GPIO.setup(ECHO_2, GPIO.IN)

    print('To Exit, Press the CTRL+C Keys')

    # HC-SR04 시작 전 잠시 대기
    GPIO.output(TRIG_1, False)
    GPIO.output(TRIG_2, False)
    print('Waiting For Sensor To Ready')
    time.sleep(1) # 1초

    #시작
    print('Start!!')
    while True:



        right = operation(TRIG_1,ECHO_1)
        
        if right < 5 :
            ref = db.reference()
            ref.update({'pet' : 1})
            
        else:
            ref = db.reference()
            ref.update({'pet' : 0})
        
        
        left = operation(TRIG_2,ECHO_2)
        
        if left < 5 :
            ref = db.reference()
            ref.update({'can' : 1})
            
        else:
            ref = db.reference()
            ref.update({'can' : 0})
            
        print("left side(pet) : {}, right side(can) : {}".format(right,left))

    GPIO.cleanup()



if __name__ == '__main__':
    main()
