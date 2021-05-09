# NIR Scanner
## Ugly little red box that almost could
This proof of concept project originated from a course I attended during the spring of 2020. The topic was "Machine vision and sensor technology" and the goal was to explore techniques which could be used to sort textile waste. I knew that NIR-spectrum analysis was already successfully implemented to do this kind of job, and I wanted to see if I could do it myself with utilizing [scikit-learn machine learning library](https://scikit-learn.org/) and affordable components available to me.

The device is built around ESP32 devkit board running MicroPython and housed in a butt-ugly 3d printed box with an obsolete button on the side. 6-band NIR sensor was purchased from SparkFun and 1.5" OLED display module was recycled from previous projects.

- SparkFun Spectral Sensor Breakout - AS7263 NIR (Qwiic): [https://www.sparkfun.com/products/14351](https://www.sparkfun.com/products/14351)
    - Drivers used: [https://github.com/jajberni/AS726X_LoPy](https://github.com/jajberni/AS726X_LoPy)
- OLED display drivers: [https://github.com/mcauser/micropython-ssd1327](https://github.com/mcauser/micropython-ssd1327)

The device connects to WiFi and listens for incoming connections on port 65432. Once the connection is established the device sends a JSON-formatted burst of data containing unique device id and normalized spectrum intensity data and then closes the connection. All the communication and data analysis is handled with a simple console client script.

## Pics
<p align="center">
<i>Lil' red box</i><br>
<img src="img\IMG_1.jpg" width=320>
<img src="img\IMG_2.jpg" width=320><br>
</p>

## If if's and buts were candy and nuts...
There are plenty of problems here but I think the results are promising. Identifying 100% homogenous fabrics (cotton, acrylic, polyester, wool for example) was fairly consistent with a larger dataset even without any ML-model optimization. Mixed fabrics is a completely different game
    
<p align="center">
    <i>Spectrum intensity graph from another, larger dataset</i><br>
    <img src="img\Figure_1.png" width=320><br>
</p>

### Something to think about further down the road:
- Collecting clean data
    - Going through your wardrobe is one thing, collecting good quality clean data from fabrics is another. Many fabrics have some other materials or coloring agents mixed in and that affects the perceived IR-spectrum
- Optimizing the ML model
    - The device was put together fairly quickly and so far 0 effort has been put into ML-model optimization. Just some frantic googling and the first suitable example was used
- Sensor housing
    - Light noise through the current housing must have some sort of effects
