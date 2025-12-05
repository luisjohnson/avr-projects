# Shared Makefile for AVR projects
# Adjust DEVICE, CLOCK, PROGRAMMER, and FUSES as needed for each MCU or programmer
DEVICE      = attiny85
CLOCK       = 8000000
PROGRAMMER  = -c usbasp
OBJDIR      = build
OBJECTS     = $(OBJDIR)/main.o
ELF         = $(OBJDIR)/main.elf
HEX         = $(OBJDIR)/main.hex

# Fuse settings for ATtiny85; update for other chips
FUSES       = -U lfuse:w:0x62:m -U hfuse:w:0xdf:m -U efuse:w:0xff:m

AVRDUDE     = avrdude $(PROGRAMMER) -p $(DEVICE)
COMPILE     = avr-gcc -Wall -Os -DF_CPU=$(CLOCK) -mmcu=$(DEVICE)

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

install: flash fuse

load: main.hex
	bootloadHID main.hex

clean:
	rm -rf $(OBJDIR)
	rm -f main.hex main.elf

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

disasm: main.elf
	avr-objdump -d main.elf

cpp:
	$(COMPILE) -E main.c
