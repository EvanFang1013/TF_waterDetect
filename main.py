import time
import RPi.GPIO as GPIO
import time
import datetime
from FTPLIB import ftpsend
import threading
import logging
from logging.handlers import TimedRotatingFileHandler

#log init
log_filename = datetime.datetime.now().strftime("./log/%Y-%m-%d_%H_%M.log")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    handlers = [TimedRotatingFileHandler(filename =log_filename ,when="D",interval=1,backupCount=30)]
                    )

#Define ENS message file
#define GPIO pinout
Machine1_PIN = 12;Machine1_ENS = './Event/WaterLeakEvent_M1.txt'
Machine2_PIN = 16;Machine2_ENS = './Event/WaterLeakEvent_M2.txt'
Machine3_PIN = 20;Machine3_ENS = './Event/WaterLeakEvent_M3.txt'
Machine4_PIN = 21;Machine4_ENS = './Event/WaterLeakEvent_M4.txt'

GPIO.setmode(GPIO.BCM)

def detect_water(DetectPIN,message):
	
	GPIO.setup(DetectPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	pressed = False
	timetemp = time.time()
	while True:

		if not GPIO.input(DetectPIN):
			if not pressed:
				if (time.time()-timetemp)>=3:
					alarm_time = time.time()
					logging.info("[InFo] Detect water leak : GPIO %s"%DetectPIN )
					print("[InFo] Detect water leak : GPIO %s"%DetectPIN)
					pressed = True	
					try:
						ftpsend(message)
					except:
						pass
						logging.warning("[Warn] ENS FTP server connect fail" )
					
			if pressed:
				if (time.time()- alarm_time)>=600:
					alarm_time = time.time()

					print("[InFo] Detect water leak : GPIO %s"%DetectPIN)
					try:
						ftpsend(message)
					except:
						pass
						logging.warning("[Warn] ENS FTP server connect fail" )

			
				
		# DR (or released)
		else:
			timetemp = time.time()
			alarm_cnt = 0
			pressed = False
		time.sleep(1)

	
	

if __name__ == '__main__':
		
	threading.Thread(target = detect_water ,args = (Machine1_PIN,Machine1_ENS)).start()
	threading.Thread(target = detect_water ,args = (Machine2_PIN,Machine2_ENS)).start()
	# ~ threading.Thread(target = detect_water ,args = (Machine3_PIN,Machine3_ENS)).start()
	# ~ threading.Thread(target = detect_water ,args = (Machine4_PIN,Machine4_ENS)).start()


