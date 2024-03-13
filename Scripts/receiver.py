# receiver.py
import spidev
from sx127x.LoRa import LoRa
from sx127x.board_config import BOARD

BOARD.setup()

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)

# Initialize LoRa
lora = LoRa(spi=spi, verbose=False)

# Set the frequency (in Hz)
lora.set_mode(LoRa.MODE.STDBY)
lora.set_freq(433e6)

# Receive data
lora.set_mode(LoRa.MODE.RXCONT)

# Wait for data
while True:
    if lora.received():
        print("Received: ", lora.read_payload())
        break

# Cleanup
spi.close()
