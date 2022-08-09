import RPi.GPIO as GPIO

class DcMotor:
  PWM_FREQUENCY = 1000 # [Hz]
  SLOWEST_DUTY_CYCLE = 60

  def __init__(self, name, ccwPin, cwPin):
    self._name = name
    self._ccwPin = ccwPin
    self._cwPin = cwPin
    self._ccwPwm = None
    self._cwPwm = None
    self._cwDirection = True
    self._dutyCycle = 0

  def setup(self):
    GPIO.setup(self._ccwPin, GPIO.OUT)
    GPIO.setup(self._cwPin, GPIO.OUT)
    self._ccwPwm = GPIO.PWM(self._ccwPin, DcMotor.PWM_FREQUENCY)
    self._cwPwm = GPIO.PWM(self._cwPin,DcMotor.PWM_FREQUENCY)
    self._ccwPwm.start(0)
    self._cwPwm.start(0)

  def move(self, cw = True):
    self._cw = cw
    self._dutyCycle = max(DcMotor.SLOWEST_DUTY_CYCLE, self._dutyCycle)
    print("Move ", self._name)
    print("  cw: ", self._cw)
    print("  dc: ", self._dutyCycle)
    otherPwm = self._ccwPwm if self._cw else self._cwPwm
    otherPwm.ChangeDutyCycle(0)    
    pwm = self._cwPwm if self._cw else self._ccwPwm
    pwm.ChangeDutyCycle(self._dutyCycle)
        
  def stop(self):
    print("Stop", self._name)
    self._cwPwm.ChangeDutyCycle(0)
    self._ccwPwm.ChangeDutyCycle(0)
    self._dutyCycle = 0
    self._cw = True        
    
  def changeSpeed(self, stepSize = 1):
    print("CHANGE SPEED", self._name)
    print("  Step: ", stepSize)    
    self._dutyCycle = min(max(self._dutyCycle + stepSize, 0), 100)
    print("   DutyCycle: ", self._dutyCycle)
    _pwm = self._cwPwm if self._cw else self._ccwPwm
    _pwm.ChangeDutyCycle(self._dutyCycle)
