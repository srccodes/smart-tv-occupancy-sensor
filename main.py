import wifimgr
from hcsr04 import HCSR04
from machine import Pin,I2C
import ssd1306,time
import urequests

def init():
    i2c = I2C(scl=Pin(19), sda=Pin(18))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)
    hcsr04 = HCSR04(trigger_pin=32, echo_pin=35, echo_timeout_us=1000000)
    hcsr501Pin = Pin(26, Pin.IN)
    hcsr501Pin.irq(trigger=Pin.IRQ_FALLING, handler=interruptCallbackHandler)
    
    return oled, hcsr04


def interruptCallbackHandler(p):
    global motionDetected
    motionDetected = True
    global lastTimeMotionDetected
    lastTimeMotionDetected = time.time()
    print("$$$$Motion detected at %s" % lastTimeMotionDetected)


def log(msg, x, y):
    oled.text(msg, x, y)
    oled.show()


def clearDisplay():
    oled.fill(0)


def toggleTvPlayPause():
    try:
        response = urequests.post("http://192.168.0.20:8060/keypress/play")
        print("API Response %s" % response.status_code)
        return response.status_code == 200
    except:
        print("Error !!!")
        log("Error !!!", 0, 30)
        return False
    

def anyoneWatching():
    global motionDetected
    
    if motionDetected:
        # If no motion detected in next 15 secs
        if ((time.time() - lastTimeMotionDetected) > 15):
            motionDetected = False
            print("Not Watching at %s" % time.time())
            return False
        else:
            print("Watching at %s" % time.time())
            return True
    else:
        print(">>>Not Watching at %s" % time.time())
        return False


def play():
    global isPaused
    
    if isPaused and toggleTvPlayPause():
        isPaused = False


def pause():
    global isPaused
    
    if not isPaused and toggleTvPlayPause():
        isPaused = True


# Initialize OLED display, Distance & Motion sensor
oled, distanceSensor = init()

# Connect to WIfi
log("Connecting...", 0, 0)
wlan = wifimgr.get_connection()
if wlan is None:
    log("No wifi !!!", 0, 20)
    print("Unable to connect to Wifi")
else:
    log("Connected :-)", 0, 20)
    wifimgr.deactivate_ap()
    print("Deactivated AP mode.")

time.sleep_ms(1000)

prevDistance = -1
isPaused = False
motionDetected = True
lastTimeMotionDetected = time.time()


while True:
    currDistance = int(distanceSensor.distance_cm())
    time.sleep(1)
    
    if currDistance != prevDistance and motionDetected:
        print("Distance: %s cm" % currDistance)
        clearDisplay()
        log("Dist: %s cm" % currDistance,0, 0)
        
        prevDistance = currDistance
        
        if anyoneWatching():
            if currDistance < 100:
                pause()
            else:
                play()
        else:
            pause()
            
        print("TV -> %s" % ("Pause" if isPaused else "Play"))
        log("TV -> %s" % ("Pause" if isPaused else "Play"), 0, 30)
        print("Motion -> %s" % ("Y" if motionDetected else "N"))
        log("Motion -> %s" % ("Y" if motionDetected else "N"), 0, 40)
        print("***************************")
        
        