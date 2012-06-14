CC=gcc
CFLAGS=-I.
BINDIR=/usr/local/bin

dnsmap: dnsmap.c dnsmap.h
	$(CC) $(CFLAGS) -o dnsmap dnsmap.c

install: dnsmap
	mkdir -p $(DESTDIR)$(BINDIR)
	install -m 0755 dnsmap $(DESTDIR)$(BINDIR)
	install -m 0755 dnsmap-bulk.sh $(DESTDIR)$(BINDIR)/dnsmap-bulk

