from time import sleep
import sys
from SX127x.LoRa import *
from SX127x.board_config import BOARD
import RPi.GPIO as GPIO

GPIO.setwarnings(False)  # Disable GPIO warnings

BOARD.setup()


class LoRaRcvCont(LoRa):


    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.STDBY)  # Set mode to STDBY initially
        self.set_dio_mapping([0] * 6)
        print("self.mode")
        # Perform mode check here before calibration
        if self.mode not in [MODE.SLEEP, MODE.STDBY, MODE.FSK_STDBY]:
            self.set_mode(MODE.STDBY)  # Set mode to STDBY if not in the required modes

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(0.5)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.flush()

    def on_rx_done(self):
        print("\nReceived: ")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        print(bytes(payload).decode("utf-8", 'ignore'))
        print(payload)
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)


lora = LoRaRcvCont(verbose=False)
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(spreading_factor=12)

try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
