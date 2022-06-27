# version:1.0.1905.9051
import gxipy as gx
from PIL import Image
import numpy
import cv2
import _thread
import threading
import time
import sys
from queue import Queue

q = Queue(maxsize=1)
m_gLiveFlag = 1
m_gProcessFlag = 1

# thread liveview
def live_image( threadName, delay):
    print("livethread")
   # create a device manager
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return

    # open the first device
    cam = device_manager.open_device_by_index(1)

    # exit when the camera is a mono camera
    if cam.PixelColorFilter.is_implemented() is False:
        print("This sample does not support mono camera.")
        cam.close_device()
        return

    # set continuous acquisition
    cam.TriggerMode.set(gx.GxSwitchEntry.OFF)

    # set exposure
    #cam.ExposureTime.set(20000.0)

    # set auto exposure time
    cam.ExposureAuto.set(1)

    # set auto white balance
    cam.BalanceWhiteAuto.set(1)

    # set gain
    cam.Gain.set(1.0)

    # get param of improving image quality
    if cam.GammaParam.is_readable():
        gamma_value = cam.GammaParam.get()
        gamma_lut = gx.Utility.get_gamma_lut(gamma_value)
    else:
        gamma_lut = None
    if cam.ContrastParam.is_readable():
        contrast_value = cam.ContrastParam.get()
        contrast_lut = gx.Utility.get_contrast_lut(contrast_value)
    else:
        contrast_lut = None
    if cam.ColorCorrectionParam.is_readable():
        color_correction_param = cam.ColorCorrectionParam.get()
    else:
        color_correction_param = 0


    # set the acq buffer count
    cam.data_stream[0].set_acquisition_buffer_number(1)
    # start data acquisition
    cam.stream_on()
    

    # acquisition image: num is the image number
    #num = 100000
    #for i in range(num):
    while m_gLiveFlag == 1:
        # get raw image
        raw_image = cam.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed.")
            continue

        if raw_image.get_status() == gx.GxFrameStatusList.INCOMPLETE:
            pass
        # get RGB image from raw image
        rgb_image = raw_image.convert("RGB")
        if rgb_image is None:
            continue

        # improve image quality
        rgb_image.image_improvement(color_correction_param, contrast_lut, gamma_lut)

        # create numpy array with data from raw image
        numpy_image = rgb_image.get_numpy_array()
        if numpy_image is None:
            continue

        #display image with opencv
        pimg = cv2.cvtColor(numpy.asarray(numpy_image),cv2.COLOR_BGR2RGB)
        #put image date to queue
        if q.qsize() ==0:
            q.put(pimg)

	    #pimg = cv2.cvtColor(numpy.asarray(numpy_image),cv2.COLOR_BGR2RGB)
	    #cv2.imwrite("cat2.jpg", pimg)
        #resize image to hd resolution 720p

        pimg = cv2.resize(pimg, (900,600))
        cv2.imshow("Image",pimg)
        cv2.waitKey(10)



    # stop data acquisition
    cam.stream_off()

    # close device
    cam.close_device()
    cv2.destroyAllWindows()  

      
      
# thread process image
def process_image( threadName, delay):
   print("processthread")
   count = 0
   while m_gProcessFlag ==1:
      time.sleep(delay)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
      pimg = q.get()
      cv2.imwrite('image-%d.jpg'%(count),pimg,[int(cv2.IMWRITE_JPEG_QUALITY),90])


# Create threads
try:
   _thread.start_new_thread( live_image, ("live_image", 1, ) )
#value 60 below means an image is saved every 60 seconds
   _thread.start_new_thread( process_image, ("process_image", 60, ) )

except:
   print ("Error: unable to start thread")

while 1:
   pass



