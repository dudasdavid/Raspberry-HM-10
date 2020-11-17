from pybleno import Characteristic
import array
import struct
import sys
import traceback
import time

from thread_wrapper import periodic

class HM10_Characteristic(Characteristic):
    
    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write', 'notify'],
            'value': None
          })
          
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None

        self.data_in = {'timestamp': 0, 'data': []}
        self.data_out = []

        # Periodic task for sending data
        self.sendThread = periodic(self.sendCommThread, 1.0, "Send")
        self.sendThread.start()
          
    def onReadRequest(self, offset, callback):
        #print('HM-10 Characteristic - %s - onReadRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data

        self.data_in['timestamp'] = time.time()
        self.data_in['data'] = [hex(c) for c in self._value]

        #print('HM-10 Characteristic - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        #print(' %s: %s' % (self['uuid'], [hex(c) for c in self._value]))

        '''
        # send data after write arrived instead of periodic task
        if self._updateValueCallback:
            self._updateValueCallback(self._value)
        '''
        callback(Characteristic.RESULT_SUCCESS)
        
    def onSubscribe(self, maxValueSize, updateValueCallback):
        print('HM-10 Characteristic - onSubscribe')
        
        self._updateValueCallback = updateValueCallback

    def onNotify(self):
        #print("buzi")
        pass

    def onUnsubscribe(self):
        print('HM-10 Characteristic - onUnsubscribe');
        
        self._updateValueCallback = None

    def sendCommThread(self):

        if self._updateValueCallback:
            #print('HM-10 Characteristic - sending data')
            array_to_send = bytearray(self.data_out)
            self._updateValueCallback(array_to_send)