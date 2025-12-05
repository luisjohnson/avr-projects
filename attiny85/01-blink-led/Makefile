# Makefile for ATiny85 projects with a USBasp programmer
DEVICE      = attiny85
CLOCK       = 8000000
PROGRAMMER  = -c usbasp
OBJDIR      = build
OBJECTS     = $(OBJDIR)/main.o
ELF         = $(OBJDIR)/main.elf
HEX         = $(OBJDIR)/main.hex

# for ATTiny85
# see http://www.engbedded.com/fusecalc/
FUSES       = -U lfuse:w:0x62:m -U hfuse:w:0xdf:m -U efuse:w:0xff:m

# Tune the lines below only if you know what you are doing:
AVRDUDE     = avrdude $(PROGRAMMER) -p $(DEVICE)
COMPILE     = avr-gcc -Wall -Os -DF_CPU=$(CLOCK) -mmcu=$(DEVICE)

# Symbolic targets:
all: main.hex

$(OBJDIR):
	mkdir -p $@

$(OBJDIR)/%.o: %.c | $(OBJDIR)
	$(COMPILE) -c $< -o $@

$(OBJDIR)/%.o: %.S | $(OBJDIR)
	$(COMPILE) -x assembler-with-cpp -c $< -o $@

.c.s:
	$(COMPILE) -S $< -o $@

flash: main.hex
	$(AVRDUDE) -U flash:w:main.hex:i

fuse:
	$(AVRDUDE) $(FUSES)

# Xcode uses the Makefile targets "", "clean" and "install"
install: flash fuse

# if you use a bootloader, change the command below appropriately:
load: main.hex
	bootloadHID main.hex

clean:
	rm -rf $(OBJDIR)
	rm -f main.hex main.elf

# File targets:
$(ELF): $(OBJECTS)
	$(COMPILE) -o $@ $^

$(HEX): $(ELF)
	rm -f $@
	avr-objcopy -j .text -j .data -O ihex $< $@
	avr-size --format=avr --mcu=$(DEVICE) $<

main.elf: $(ELF)
	ln -sf $(ELF) $@

main.hex: $(HEX)
	ln -sf $(HEX) $@

# If you have an EEPROM section, you must also create a hex file for the
# EEPROM and add it to the "flash" target.

# Targets for code debugging and analysis:
disasm: main.elf
	avr-objdump -d main.elf

cpp:
	$(COMPILE) -E main.c
