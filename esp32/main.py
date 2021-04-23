from machine import Pin, I2C, freq, reset, unique_id
from AS726X import AS726X
from ubinascii import hexlify
import time, ssd1327, _thread, ujson, gc, network
import usocket as socket

freq(240000000)
gc.enable()
gc.threshold(16)

i2c = I2C(scl=Pin(21), sda=Pin(22))

button = Pin(17, Pin.IN, Pin.PULL_UP)

display = ssd1327.SSD1327_I2C(128, 128, i2c)

sensor = AS726X(i2c=i2c)
sensor.set_bulb_current(2)
sensor.set_measurement_mode(2)

class Transponder:
    def __init__(self):
        self.running = False

    def __main_loop__(self):
        self.running = True

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # setup a socket s
            s.bind(('', 65432)) # bind the socket s to port 65432
            s.listen(5) # set the socket s to listen for incoming connections, max 5 simultaneous conns

            while self.running == True:
                conn, addr = s.accept()
                spectrum = get_normalized_spectrum()
                conn.sendall(ujson.dumps(dict(device_id = hexlify(unique_id()).decode('utf-8'), spectrum = spectrum)))
                display_refresh(spectrum)
                conn.close()

            s.close()

        except Exception as e:
            print(e)
            s.close()
            self.stop()
            self.run()

    def run(self):
        self.main_thread = _thread.start_new_thread(self.__main_loop__, ())

    def stop(self):
        self.running == False

def init_network():
    for i in range(3):
        try:
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            wlan.config(dhcp_hostname=hexlify(unique_id()).decode('utf-8'))

            with open('network.credentials', 'r') as f:
                credentials = f.read()

                ssid = credentials.split('.')[0]
                password = credentials.split('.')[1]

            if not wlan.isconnected():
                print('connecting to network...')
                wlan.connect(ssid, password)
                
                while not wlan.isconnected():
                    pass

            print('network config:', wlan.ifconfig())
            break

        except Exception as e:
            if i == 2:
                print(e)
                print("network init failed after " + str(i + 1) + " attempts...")
                pass
            else:
                print(e)
                print("retrying network init...")
                continue

def get_normalized_spectrum():
    sensor.enable_bulb()
    sumSpectrum = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    for x in range(3):
        spectrum = sensor.get_calibrated_values()
        if 0 in spectrum:
            x -= 1
        else:
            sumSpectrum = [sum(i) for i in zip(sumSpectrum, spectrum)]

    sensor.disable_bulb()
    normalizedSpectrum = [i / sum(sumSpectrum) for i in sumSpectrum]
    return normalizedSpectrum

def display_refresh(spectrum):
    display.fill(0)

    display.text(hexlify(unique_id()).decode('utf-8'), 16, 0, 15)

    for i in range(len(spectrum)):
        display.framebuf.fill_rect(4+i*20, display.height-int(spectrum[i]*display.height), 19, int(spectrum[i]*display.height), 15)
    
    display.show()

init_network()

transponder = Transponder()
transponder.run()

display.text(hexlify(unique_id()).decode('utf-8'), 16, 0, 15)
display.show()
