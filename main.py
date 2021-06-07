import time
import RPi.GPIO as GPIO
import time
from FTPLIB import ftpsend
import threading

#Define ENS message file
#define GPIO pinout

Machine_PIN = 21;Machine_ENS = 'CUSOVTLeakEvent_SubGrp_20200728.txt'

GPIO.setmode(GPIO.BCM)

def detect_water(DetectPIN,message):
	
	GPIO.setup(DetectPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	pressed = False
	timetemp = time.time()
	while True:

		if not GPIO.input(DetectPIN):
			if not pressed:
				if (time.time()-timetemp)>=5:
					print(DetectPIN,"Detect water!")
					ftpsend(message)
					pressed = True	
		# DR(or released)
		else:
			timetemp = time.time()
			print(DetectPIN,"dry")
			pressed = False
		time.sleep(0.5)

	
	

if __name__ == '__main__':
		
	threading.Thread(target = detect_water ,args = (12,Machine_ENS)).start()
	threading.Thread(target = detect_water ,args = (16,Machine_ENS)).start()
	threading.Thread(target = detect_water ,args = (20,Machine_ENS)).start()
	threading.Thread(target = detect_water ,args = (Machine_PIN,Machine_ENS)).start()


