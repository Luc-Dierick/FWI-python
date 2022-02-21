import time
import os
import argparse
from start_lab import start_lab as start
from close_lab import close_lab as close
# from adc_measurement import measure as measure_power
from adc_measurement import measure_serial as measure_all
from program_pynq import program as program
# from measure_temperature import measure_temperature as measure_temperature
from set_pin import enable_clock as enable_clock
from set_pin import disable_clock as disable_clock
from set_pin import start_reset as start_reset
from set_pin import stop_reset as stop_reset
from matplotlib import pyplot as plt
import numpy as np
import paramiko

# shunt_r = 0.025185882
# shunt_r = 0.05957
# gain_factor = 13.195
# gain_factor = 7.089

# gain = 15.702
# shunt = 0.025122472
# def computepower(shuntvoltage,corevoltage):
#  current = shuntvoltage/(6990506.667*(gain*shunt)) #ampere
#  power = (corevoltage/6990506.667)*current #watt
#  return power

if __name__ == '__main__':

    # set machine-specific stuff
    # sopwith
    # pynq board ID
    pynq_measure = '*/xilinx_tcf/Digilent/003017A6DD49A'
    # some parameters for power calculation
    shunt_r = 0.05965
    gain_factor = 7.0976
    offset = 0.0  # ToDo: determine pls
    # address of remote-controlled power outlet
    system_code = "11111"
    unit_code = "10101"
    arduino_usb_device_id = '/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0'
    machine = "sopwith"

    # safety feature denying multiple runs at the same time
    multiple_access_deny_folder = '/home/delft/python-scripts/power-measurement/access-deny-folder'
    if not (os.path.exists(multiple_access_deny_folder)):
        os.mkdir(multiple_access_deny_folder)
    multiple_access_deny_file = f'/home/delft/python-scripts/power-measurement/access-deny-folder/{machine}_script_already_running.txt'
    if os.path.exists(multiple_access_deny_file):
        raise Exception(
            f'Another instance of this script is already running. You can start another measurement run when the folder /home/delft/python-scripts/power-measurement/access-deny-folder does not contain the file "{machine}_script_already_running.txt" anymore.')
    else:
        with open(multiple_access_deny_file, "w") as f:
            f.write("ongoing measurement run, please wait until this file is deleted when this run ends, thanks :)")
    # path to temporary tcl script file that we are using to control vivado
    tcl_script_path = '/home/delft/tcl-scripts/temp-vivado.tcl'

    try:
        print('started lab - performing measurements now...')
        s1, s2, s3 = measure_all(arduino_usb_device_id, shunt_r, gain_factor, offset)
        print(f"before: {s1} and {s2} and {s3} ")
        totalpowerarray = []
        objecttemperaturearray = []
        ambienttemperaturearray = []
        from handler import ShellHandler

        c = ShellHandler("141.51.124.98", "xilinx", "xilinx")
        print(c.execute_sudo(""))
        print(c.execute("python3 /home/xilinx/jupyter_notebooks/FWI_python/main.py -d 10x10_100CPU.txt"))
        while True:
            time.sleep(0.5)
            s1, s2, s3 = measure_all(arduino_usb_device_id, shunt_r, gain_factor, offset)
            totalpowerarray.append(s1)
            objecttemperaturearray.append(s2)
            ambienttemperaturearray.append(s3)
            res = c.output()
            print(res)
            if "END" in res:
                break
            # DEBUGGING START
        s1, s2, s3 = measure_all(arduino_usb_device_id, shunt_r, gain_factor, offset)
        # DEBUGGING END

        print(f"end: {s1} and {s2} and {s3} ")

        print(totalpowerarray)
        print(objecttemperaturearray)
        print(ambienttemperaturearray)
        # close(system_code, unit_code)
        print('finished measurements and shut down lab')
        if os.path.exists(multiple_access_deny_file):
            os.remove(multiple_access_deny_file)
    except Exception as e:
            print(f'Detected measurement failure: "{e}" - cleaning up the mess, now...')
            # close(system_code, unit_code)
            if os.path.exists(multiple_access_deny_file):
                os.remove(multiple_access_deny_file)
