#!../env/bin/python3
import logging
logging.basicConfig(level=logging.INFO,
            #format= '[%(levelname)s] [%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
            format='[%(levelname)s] (%(threadName)-10s) %(message)s')
try:
    import RPi.GPIO as GPIO
except Exception:
  logging.critical("RPi.GPIO package not found... creating None variable for testing purpose only...")
  GPIO = None
import threading
import time
import queue
import concurrent.futures

from i2c_service import init_i2c
from dist_service import init_dist
from web_service import init_web
from bus_service import init_bus
from bit_service import init_bit

from shared_module.helpers import json2dict
from shared_module.rotatequeue import RotateQueue

def get_device_names():
    deviceNames = {
        'i2c':  list(json2dict('i2c_service/config.json', __file__)['i2c']['address'].keys()),
        'dist': list(json2dict('dist_service/config.json', __file__)['dist']['pinout'].keys())
    }
    return deviceNames

if __name__ == "__main__":
    pipeline = {
    'i2c':{
            'i2c':RotateQueue(maxlen=10)
        },
        'dist':{
            'dist':RotateQueue(maxlen=5)
        },
        'bit':{
            'bit':RotateQueue(maxlen=5)
        },
        'web':{
            'web':RotateQueue(maxlen=5)
        },
        'bus':{
            'bus':RotateQueue(maxlen=5)
        }
    }

    ######## SRC --> DEST THREAD ##############
    pipeline['i2c']['bus'] = pipeline['i2c']['i2c']
    pipeline['dist']['bus'] = pipeline['dist']['dist']
    pipeline['bus']['web'] = pipeline['web']['web']
    pipeline['web']['bit'] = pipeline['bit']['bit']
    #pipeline['web']['bus'] = pipeline['bus']['bus']
    #pipeline['bus']['web'] = pipeline['web']['web']

    if not GPIO is None:
        logging.info("Changing GPIO to BOARD MODE")
        GPIO.setmode(GPIO.BOARD) # BOARD pin-numbering scheme
        GPIO.setwarnings(False)
    logging.info('Starting REACTOR CSTR - TOG Application Services...')

    logging.info(f'showing sensor names list{get_device_names()}')
    with concurrent.futures.ThreadPoolExecutor(max_workers=5, thread_name_prefix = 'app-service') as executor:
        futureException = {
              executor.submit(init_bit, pipeline): 'bit-service',
              executor.submit(init_web, pipeline): 'web-service',
              executor.submit(init_i2c, pipeline): 'i2c-service',
              executor.submit(init_dist, pipeline): 'dist-service',
              executor.submit(init_bus, pipeline, get_device_names()): 'bus-service' 
            }
        for futureErrors in concurrent.futures.as_completed(futureException):
            threadName = futureException[futureErrors]
            try:
                data = futureErrors.result()
            except Exception as exc:
                logging.error(f'<{threadName}> generated an exception: {exc}')
            else:
                logging.info(f'<{threadName}> finish without error and return \'{data}\'')
    GPIO.cleanup()
    
