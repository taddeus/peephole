CC=xgcc
CFLAGS=-O0

%.s: %.c
	$(CC) $(CFLAGS) -S $<
%.o: %.s
	$(CC) $(CFLAGS) -c $<

%: %.o
	$(CC) $(CFLAGS) $<

all: acron clinpack dhrystone pi slalom whet

asm: acron.s clinpack.s dhrystone.s pi.s slalom.s whet.s

clean:
	rm -f acron clinpack dhrystone pi slalom whet
	rm -f *.o
	rm -f *.s
	rm -f *.cycles *.output

