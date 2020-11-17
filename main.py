from pybleno import *
import sys
import signal
from hm10_characteristic import *

print('raspberrypi - echo');

bleno = Bleno()
hm10 = HM10_Characteristic('ffe1')

def onStateChange(state):
   print('on -> stateChange: ' + state);

   if (state == 'poweredOn'):
     bleno.startAdvertising('raspberrypi', ['ffe0'])
   else:
     bleno.stopAdvertising();

bleno.on('stateChange', onStateChange)
    
def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'));

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': 'ffe0',
                'characteristics': [ 
                    hm10
                    ]
            })
        ])
bleno.on('advertisingStart', onAdvertisingStart)

bleno.start()

i = 0
timestamp = 0
lastTimestamp = 0

while True:
    try:
        i += 1
        timestamp = hm10.data_in['timestamp']
        if timestamp != lastTimestamp:
            print(hm10.data_in)
            lastTimestamp = timestamp
        hm10.data_out = [i%256]
        time.sleep(0.1)
    except:
        break



bleno.stopAdvertising()
bleno.disconnect()
hm10.sendThread.exit()

print ('terminated.')
sys.exit(1)