#!/usr/bin/env python3

import RPi.GPIO as GPIO
import drivers
import requests
import time
import datetime
import threading
import board
import adafruit_dht

# establish GPIO setup
GPIO.setmode(GPIO.BCM)

# initialize buttons with their pins
BTN_R = 5 # 29 - heating button
BTN_B = 6 # 31 - cooling button
BTN_Y = 13 # 33 - indicates opening/closing of door/window

# initialize LEDs with their pins
LED_R = 23 # 16 - heater indicator
LED_B = 24 # 18 - AC indicator
LED_G = 25 # 2 - indicates human presence and turns on the lights

# initialize PIR sensor pin
PIN_PIR = 17 # 11 - for motion detection

# initialize DHT pin
#PIN_DHT = 32 # G12 - for humidity and temperature detection
temperature_dht = adafruit_dht.DHT11(board.D12)

# Load the driver and set it to "display"
display = drivers.Lcd()

# other storing variables
weather_index = 72
temperature_desired = 69
temperature_avg = 0 
weather_index = 0
track_time = 0      # use as counter
display_updated = 0 , 
state_security =  state_hvac, state_light

# obtaining CIMIS data
dateToday = date.today() - timedelta(days=1)
dateToday = dateToday.strftime("%Y-%m-%d")
cimis = 'http://et.water.ca.gov/api/data?appKey=6013a099-06cf-49a7-8f45-2e93c69edc05&targets=75&dataItems=hly-rel-hum&startDate='+dateToday+'&endDate='+dateToday

# setup
def setup():
    print("Initializing GPIO I/O")
    GPIO.setwarnings(False) 
    GPIO.setup(BTN_R, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BTN_B, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    GPIO.setup(BTN_Y, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LED_R, GPIO.OUT, initial=GPIO.LOW)          
    GPIO.setup(LED_B, GPIO.OUT, initial=GPIO.LOW) 
    GPIO.setup(LED_G, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(PIN_PIR, GPIO.IN)

# function to release resources 
def clean():
    GPIO.cleanup()

### ambient light control and human detection functionality ###
def ambient_light():
    if (GPIO.input(PIN_PIR) == GPIO.HIGH):
        GPIO.output(LED_G, GPIO.HIGH)
        display.lcd_clear()
        display.lcd_display_string("Person detected...", 1)
        display.lcd_display_string("Light on!", 2)
        # turn off the light once no movement is detected in 10s
        time.sleep(10)
        GPIO.output(LED_G,GPIO.LOW)
        print("No person detected, turning off light...", 1)
        time.sleep(2)
    
### room temperature (HVAC) functionality ###
# retrieve dht temp once every 10s
# average the last three measurements to eliminate mistakes
# calculate weather index

# compare weather index with user input temp; enable HVAC accordingly

# allow user to set temp within range of 65-85 degrees using the buttons
def get_dht_temperature():
    global temperature_ave
    while True:
        try:
            # Print the values to the serial port
            temperature_c = temperature_dht.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = temperature_dht.humidity
            print(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )
            )

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            temperature_dht.exit()
            raise error

        time.sleep(2.0)

def get_cimis_humidity():
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data, headers = header)
    try:
        resp = urllib.request.urlopen(req)
        data2 = json.load(resp)
    except:
        return 72
    return int(data2["Data"]["Providers"][0]["Records"][0]["DayRelHumAvg"]["Value"])

def get_weather_index(CIMISHumidity, DHTTemp):
    # weather_index = temperature + (0.05 * humidity)

def set_heat():
# red button heats/raises the temperature
    if (GPIO.input(BTN_R) == GPIO.HIGH) and (temperature_desired < 85):
        if (temperature_desired >= 85):
            display.lcd_clear()
            display.lcd_display_string("HVAC OFF", 1)
            print("Temperature can't go any higher!\n")

        # set AC on ONLY if weather index is 3 degrees below desired temperature
        elif ( weather_index <= (temperature_desired + 3) ):
            display.lcd_clear()
            display.lcd_display_string("HVAC OFF", 1)
            print("The weather surpasses the desired temperature!\n")

        # turn off HVAC temporarily if doors and windows are open
        elif (GPIO.output(LED_G) == GPIO.HIGH):
            display.lcd_clear()
            display.lcd_display_string("DOOR/WINDOW OPEN", 1)
            display.lcd_display_string("HVAC HALTED", 2)

        else:
            display.lcd_clear()
            display.lcd_display_string("HVAC HEAT", 1)
            temperature_desired += 1
            print("Heating up! Current Temperature: %d\n"%temperature_desired)
            GPIO.output(LED_R,GPIO.HIGH)
            GPIO.output(LED_B,GPIO.LOW)
    else:
        display.lcd_display_string("HVAC OFF", 1)

def set_ac():
    # blue button cools/lowers the temperature
    if (GPIO.input(BTN_B) == GPIO.HIGH) and (temperature_desired > 65):
        if (temperature_desired <= 65):
            display.lcd_clear()
            display.lcd_display_string("HVAC OFF", 1)
            print("Temperature can't go any lower!\n")

        # set AC on ONLY if weather index is 3 degrees above desired temperature
        elif ( weather_index >= (temperature_desired + 3) ):
            display.lcd_clear()
            display.lcd_display_string("HVAC OFF", 1)
            print("The weather surpasses the desired temperature!\n")
        
        # turn off HVAC temporarily if doors and windows are open
        elif (GPIO.output(LED_G) == GPIO.HIGH):
            display.lcd_clear()
            display.lcd_display_string("DOOR/WINDOW OPEN", 1)
            display.lcd_display_string("HVAC HALTED", 2)

        else:
            display.lcd_clear()
            display.lcd_display_string("HVAC AC", 1)
            temperature_desired -= 1
            print("Cooling down! Current Temperature: %d\n"%temperature_desired)
            GPIO.output(LED_B,GPIO.HIGH)
            GPIO.output(LED_R,GPIO.LOW)
    else:
        display.lcd_display_string("HVAC OFF", 1)

### energy bill generator functionality ###
def get_energy_bill():
    display.lcd_display_string("HVAC OFF", 1)


### security system functionality ###
def security_system():
    display.lcd_display_string("HVAC OFF", 1)

### standard LCD screen ###
def lcd_standard():
    global display_updated, temperature_dht, weather_index
    global state_security, state_hvac, state_light

    if (display_updated == 0):
        display.lcd_clear()
        display.lcd_display_string("%d/%d     D:%s"%(temperature_dht, weather_index, state_security), 1) 
        display.lcd_display_string("H:%s     L:%s"%(state_hvac, state_light), 2)

### button functionality for any given moment ###
def detect_button():
    GPIO.add_event_detect(BTN_R, GPIO.FALLING, callback=heat_up, bouncetime=300)
    GPIO.add_event_detect(BTN_B, GPIO.FALLING, callback=cool_down, bouncetime=300)
    GPIO.add_event_detect(BTN_Y, GPIO.FALLING, callback=security_system, bouncetime=300)

### main function implementing everything above ###
def main():
    
    # while True:
    detect_button()

    # thread for lcd display updates
    thread_display = threading.Thread(target=lcd_standard)
    thread_display.setDaemon(True)
    thread_display.start()

    # threads for heat/ac updates
    thread_set_heat = threading.Thread(target=set_heat)
    thread_set_heat.setDaemon(True)
    thread_set_heat.start()

    thread_set_ac = threading.Thread(target=set_ac)
    thread_set_ac.setDaemon(True)
    thread_set_ac.start()

    # thread for dht temperature updates
    thread_dht_temperature = threading.Thread(target=get_dht_temperature)
    thread_dht_temperature.setDaemon(True)
    thread_dht_temperature.start()

    # check for ambient light/human detection functionality 
    try: 
        ambient_light()
    except KeyboardInterrupt:
        # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
        print("Cleaning up!")
        display.lcd_clear()

        
### project execution ###
setup()
main()
