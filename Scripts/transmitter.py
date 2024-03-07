# transmitter.py
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

# Send data
lora.set_mode(LoRa.MODE.TX)
lora.send(b'Hello, receiver!')

# Cleanup
spi.close()
