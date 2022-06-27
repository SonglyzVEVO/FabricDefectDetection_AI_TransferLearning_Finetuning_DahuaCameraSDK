import gxipy as gx
import numpy
import cv2
import threading
import time
from queue import Queue
from datetime import datetime


class ThreadCamera:

    def __init__(self):

        # set state early in constructor object
        self.state_live_cam = False
        self.state_process_img = False
        self.loop_state_break = False
        # use Queue for communicate thread1<----->thread2
        self.q = Queue(maxsize=1)
        self.store = 0
        self.m_gLiveFlag = False
        self.m_gProcessFlag = False
        self.thread_live_cam = threading.Thread(target=self.live_image, args=("live_cam", 1,))
        # value 5 below means a process is run every 5 seconds
        self.thread_process_img = threading.Thread(target=self.process_image, args=("process_img", 5,))
        
    @staticmethod
    def get_time():
        now = datetime.now()
        # setting time format that can save in Window os
        time_now = now.strftime("m%md%dy%Yh%Hm%Ms%S")
        return time_now

    def start_program(self):
        if self.q.qsize() == 1:
            self.store = self.q.get()
            del self.store
            # clear q memory in queue on before start

        print("System start.............................")
        self.loop_state_break = False
        self.state_live_cam = True
        self.state_process_img = True
        self.m_gLiveFlag = True
        self.m_gProcessFlag = True

        self.thread_live_cam.start()
        self.thread_process_img.start()

    def stop_program(self):
        print("System stop..............................")
        self.loop_state_break = True
        self.state_live_cam = False
        self.state_process_img = False
        self.m_gLiveFlag = False
        self.m_gProcessFlag = False

    def live_image(self, thread_name, delay):
        if self.state_live_cam:

            # create a device manager
            print(str(thread_name) + " is starting" + " delay " + str(delay))

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

            # set continuous acquisition white balancing
            red_ratio = 2.0547
            green_ratio = 1
            blue_ratio = 1.8633

            # Red channel
            cam.BalanceRatioSelector.set(0)
            cam.BalanceRatio.set(red_ratio)

            # Green channel
            cam.BalanceRatioSelector.set(1)
            cam.BalanceRatio.set(green_ratio)

            # Blue channel
            cam.BalanceRatioSelector.set(2)
            cam.BalanceRatio.set(blue_ratio)

            # set continuous acquisition
            cam.TriggerMode.set(gx.GxSwitchEntry.OFF)

            # set exposure = 400
            cam.ExposureTime.set(400.0)

            # set gain
            cam.Gain.set(0.0)

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

            while self.m_gLiveFlag:
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

                # display image with opencv
                pimg = cv2.cvtColor(numpy.asarray(numpy_image), cv2.COLOR_BGR2RGB)
                # put image date to queue
                if self.q.qsize() == 0:
                    self.q.put(pimg)

                # resize image to hd resolution 720p
                pimg = cv2.resize(pimg, (900, 600))

                text = str(self.get_time())

                pimg = cv2.putText(
                    img=pimg,
                    text=text,
                    org=(200, 100),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX,
                    fontScale=1.0,
                    color=(0, 0, 0),
                    thickness=2
                )

                pimg = cv2.putText(
                    img=pimg,
                    text="predict result: Bad",
                    org=(200, 200),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX,
                    fontScale=1.0,
                    color=(0, 0, 0),
                    thickness=2
                )

                cv2.imshow("Image", pimg)
                cv2.waitKey(10)

                if self.loop_state_break:
                    # stop data acquisition
                    cam.stream_off()

                    # close device
                    cam.close_device()
                    cv2.destroyAllWindows()
                    break

    def process_image(self, thread_name, delay):
        if self.state_process_img:
            print("process thread" + str(thread_name))
            while self.m_gProcessFlag:
                time.sleep(delay)
                pimg = self.q.get()
                time_now = self.get_time()
                print("process_image" + str(self.get_time()))
                path_filename = '../path_save/Frame_' + str(time_now) + '.jpg'
                # Save the images in given path
                cv2.imwrite(path_filename, pimg, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                # deploy model prediction over here !!

                if self.loop_state_break:
                    break


if __name__ == '__main__':
    x = ThreadCamera()

    # Test user input
    while True:
        print('Send User command here:')
        btn = input()
        if btn == 'start':
            x.start_program()
        elif btn == "stop":
            x.stop_program()
        else:
            print("That command does not exist in the system.")
