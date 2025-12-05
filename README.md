# AVR Projects

## AVR Projects organized by MCU

### ATtiny85

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

## Build Makefile

A reusable Makefile under `attiny85/01-blink-led/` orchestrates `avr-gcc`, `avr-objcopy`, and `avrdude` so every AVR project in this repo can share the same build/upload process. Key variables and targets include:

- `DEVICE`, `CLOCK`, and `PROGRAMMER`: define the MCU, clock frequency, and programmer interface (`usbasp` by default). Update these if you move to a different chip, clock, or programmer.
- `AVRDUDE` and `COMPILE`: helper macros that keep the actual commands readable: `AVRDUDE` runs the configured upload tool, while `COMPILE` invokes `avr-gcc` with optimizations, warning flags, and the MCU definition.
- `all` (default): builds `main.elf` and then converts it into `main.hex` via `avr-objcopy` and reports size with `avr-size`.
- `flash`: runs `avrdude` to write `main.hex` to flash; depends on `all`, so it always rebuilds before programming.
- `fuse`: locks in the fuse settings (`lfuse`, `hfuse`, `efuse`) used for the ATtiny85 project.
- `install`: convenient alias that flashes and programs the fuse settings in one command (needed by some IDEs such as Xcode).
- Debug/analysis helpers: `disasm` shows the generated assembly, `cpp` runs the C preprocessor output.
- Utility targets: `clean` removes generated artifacts; `load` is provided as an example if you use a different bootloader workflow.

Run `make` to build everything, `make flash` to program the chip, `make fuse` to write fuses, and `make clean` to wipe build artifacts. Adjust `AVRDUDE`, `COMPILE`, or `FUSES` in the Makefile only when you need a different toolchain configuration or fuse setup.

## Project Template

For each new AVR project, start by copying the shared template directory at `template/`. It contains the reusable Makefile described above plus a minimal `main.c` that toggles PB0, so you can rapidly copy/paste or branch into a new folder without retyping the build logic. When setting up a new project:

- Duplicate `template/` to a new directory (e.g., `cp -r template project-name`).
- Replace `main.c` with your new code and keep the `Makefile` unless you need MCU-specific adjustments.
- Update `DEVICE`, `CLOCK`, and `PROGRAMMER` in the copied Makefile if you switch MCUs or programmers, and set `FUSES` appropriately.

If you prefer automation, consider adding a small shell script to `create-project.sh` that copies the template and optionally initializes a git branch so every new project starts from the same baseline.

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
