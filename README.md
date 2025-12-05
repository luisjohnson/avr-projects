# ATtiny85 Example Projects

This repository contains example code and projects for programming the ATtiny85 microcontroller.

## About the ATtiny85

The ATtiny85 is a low-power 8-bit AVR microcontroller with:
- 8KB of Flash memory
- 512 bytes of SRAM
- 512 bytes of EEPROM
- 6 I/O pins
- Operating voltage: 2.7V - 5.5V
- Maximum clock speed: 20MHz (internal oscillator up to 8MHz)

## Hardware Requirements

- ATtiny85 microcontroller
- USB programmer (USBasp, Arduino as ISP, or similar)
- Breadboard and jumper wires
- Components as needed per project (LEDs, resistors, sensors, etc.)

## Software Requirements

- AVR-GCC toolchain
- AVRDUDE for programming
- Optional: Arduino IDE with ATtiny board support

## Installation

### macOS
```bash
brew install avr-gcc avrdude
```

### Linux
```bash
sudo apt-get install gcc-avr avr-libc avrdude
```

## Programming the ATtiny85

Basic command to upload code:
```bash
avrdude -c usbasp -p attiny85 -U flash:w:program.hex:i
```

## Toolchain Setup

### macOS
1. Install the toolchain with Homebrew (avr-gcc now lives in the `osx-cross/avr` tap):
     ```bash
     brew update
     brew tap osx-cross/avr
     brew install osx-cross/avr/avr-gcc avrdude
     ```
2. Confirm `avr-gcc` and `avrdude` are on your `PATH` with `which avr-gcc` and `which avrdude`.

### Linux
1. Install packages using your distribution’s package manager (example for Debian/Ubuntu):
     ```bash
     sudo apt update
     sudo apt install gcc-avr avr-libc avrdude binutils-avr usbutils make
     ```
2. Verify permissions on the USBasp device (look up the device via `lsusb` and ensure you have read/write access). For persistent access, add a udev rule if needed.

Once installed, build with `avr-gcc -mmcu=attiny85 -Os -o main.elf main.c`, create a hex with `avr-objcopy -O ihex -R .eeprom main.elf main.hex`, and program the chip with `avrdude -c usbasp -p attiny85 -U flash:w:main.hex:i`. The USBasp shows up on macOS under `system_profiler SPUSBDataType` and on Linux under `lsusb`; use those commands to confirm the programmer is connected before running `avrdude`.

## Projects

### 1. LED Blink
A simple LED control project to get started with the ATtiny85.
- Location: `01-led-blink/`
- Demonstrates basic GPIO output and timing

#### LED Wiring
Connect the LED between PB0 and GND with a current-limiting resistor as shown:

```
   ATtiny85       Component
   ┌───────────┐
   │           │
 PB0│1        8│VCC
      │           │
 PB1│2        7│PB2
      │           │
 PB2│3        6│PB1
      │           │
 GND│4        5│PB0 --[330Ω]--|>-- GND
   └───────────┘
```

Use digital pin PB0 to drive the LED, and keep VCC at 5V (or 3.3V depending on your board) with GND shared. The resistor prevents overcurrent.

## Pinout Reference

```
        ATtiny85
     ┌─────┴─────┐
RESET│1  ●     8 │VCC
 PB3 │2        7 │PB2 (SCK)
 PB4 │3        6 │PB1 (MISO)
 GND │4        5 │PB0 (MOSI)
     └───────────┘
```

## Resources

- [ATtiny85 Datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2586-AVR-8-bit-Microcontroller-ATtiny25-ATtiny45-ATtiny85_Datasheet.pdf)
- [AVR Libc Reference](https://www.nongnu.org/avr-libc/)

## License

This project is open source and available for educational purposes.
