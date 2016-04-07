#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

class StepperMotor:
        HALF_STEPS = 8; 
        A       = [1, 0, 0, 0]
        AB      = [1, 0, 1, 0]
        B       = [0, 0, 1, 0]
        _AB     = [0, 1, 1, 0]
        _A      = [0, 1, 0, 0]
        _A_B    = [0, 1, 0, 1]
        _B      = [0, 0, 0, 1]
        A_B     = [1, 0, 0, 1]
        steps2coils = [A, AB,  B, _AB, _A, _A_B, _B, A_B]
        HALF_STEP_DELAY = 0.25
	
	def __init__(self, controller, num, steps=200):
		self.MC = controller
		self.revsteps = steps
		self.motornum = num
		self.sec_per_step = 0.1
		self.steppingcounter = 0
		self.currentstep = 0

		num -= 1

		if (num == 0):
			self.PWMA = 8
			self.AIN2 = 9
			self.AIN1 = 10
			self.PWMB = 13
			self.BIN2 = 12
			self.BIN1 = 11
		elif (num == 1):
			self.PWMA = 2
			self.AIN2 = 3
			self.AIN1 = 4
			self.PWMB = 7
			self.BIN2 = 6
			self.BIN1 = 5
		else:
			raise NameError('MotorHAT Stepper must be between 1 and 2 inclusive')

	def setSpeed(self, rpm):
		self.sec_per_step = 60.0 / (self.revsteps * rpm)
		self.steppingcounter = 0
        
        def halfStep(self, dir):
            pwm_a = pwm_b = 255
            
            # Move to next half step
            if dir is MotorShield.CW:
                self.currentstep += 1
            else:
                self.currentstep -= 1
            self.currentstep %= HALF_STEPS 
            
            # only really used for microstepping, otherwise always on!
            self.MC._pwm.setPWM(self.PWMA, 0, pwm_a*16)
            self.MC._pwm.setPWM(self.PWMB, 0, pwm_b*16)
            
            coils = steps2coils[self.currentstep]
            
            self.MC.setPin(self.AIN1, coils[0])
            self.MC.setPin(self.AIN2, coils[1])
            self.MC.setPin(self.BIN1, coils[2])
            self.MC.setPin(self.BIN2, coils[3])
            

	def oneStep(self, dir):
                
                # First Half Step
                self.halfStep(dir) 
                time.sleep(self.secs_per_step * HALF_STEP_DELAY)

                # Second Half Step
                self.halfStep(dir) 

                return self.currentstep


	def step(self, steps, direction, stepstyle):
		s_per_s = self.sec_per_step
		
		for s in range(steps):
			self.oneStep(direction)
			time.sleep(s_per_s)

class DCMotor:
	def __init__(self, controller, num):
		self.MC = controller
		self.motornum = num
                pwm = in1 = in2 = 0

                if (num == 0):
                         pwm = 8
                         in2 = 9
                         in1 = 10
                elif (num == 1):
                         pwm = 13
                         in2 = 12
                         in1 = 11
                elif (num == 2):
                         pwm = 2
                         in2 = 3
                         in1 = 4
                elif (num == 3):
                         pwm = 7
                         in2 = 6
                         in1 = 5
		else:
			raise NameError('MotorHAT Motor must be between 1 and 4 inclusive')
                self.PWMpin = pwm
                self.IN1pin = in1
                self.IN2pin = in2

	def run(self, command):
		if not self.MC:
			return
		if (command == MotorShield.FORWARD):
			self.MC.setPin(self.IN2pin, 0)
			self.MC.setPin(self.IN1pin, 1)
		if (command == MotorShield.BACKWARD):
			self.MC.setPin(self.IN1pin, 0)
			self.MC.setPin(self.IN2pin, 1)
		if (command == MotorShield.RELEASE):
			self.MC.setPin(self.IN1pin, 0)
			self.MC.setPin(self.IN2pin, 0)
	def setSpeed(self, speed):
		if (speed < 0):
			speed = 0
		if (speed > 255):
			speed = 255
		self.MC._pwm.setPWM(self.PWMpin, 0, speed*16)

class MotorShield:
	CW = 1
	COUNTER_CW = 2
	BRAKE = 3
	RELEASE = 4

	SINGLE = 1
	DOUBLE = 2
	INTERLEAVE = 3
	MICROSTEP = 4

	def __init__(self, addr = 0x60, freq = 1600):
		self._i2caddr = addr            # default addr on HAT
		self._frequency = freq		# default @1600Hz PWM freq
		self.motors = [ DCMotor(self, m) for m in range(4) ]
		self.steppers = [ MotorShield(self, 1), MotorShield(self, 2) ]
		self._pwm =  PWM(addr, debug=False)
		self._pwm.setPWMFreq(self._frequency)

	def setPin(self, pin, value):
		if (pin < 0) or (pin > 15):
			raise NameError('PWM pin must be between 0 and 15 inclusive')
		if (value != 0) and (value != 1):
			raise NameError('Pin value must be 0 or 1!')
		if (value == 0):
			self._pwm.setPWM(pin, 0, 4096)
		if (value == 1):
			self._pwm.setPWM(pin, 4096, 0)

	def getStepper(self, steps, num):
                if (num < 1) or (num > 2):
                        raise NameError('MotorHAT Stepper must be between 1 and 2 inclusive')
                self.steppers[num - 1] = MotorShield(self, 1, steps)
		return self.steppers[num-1]

	def getMotor(self, num):
		if (num < 1) or (num > 4):
			raise NameError('MotorHAT Motor must be between 1 and 4 inclusive')
		return self.motors[num-1]
