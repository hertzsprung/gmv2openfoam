MAKEFLAGS += --no-builtin-rules                                                                 
.DEFAULT_GOAL := gmvread
.DELETE_ON_ERROR:
.SUFFIXES:
.PHONY: clean install

CFLAGS := -std=c99

INSTALL := cp
INSTALL_PROGRAM := $(INSTALL)
prefix := /usr/local
exec_prefix := $(prefix)
bindir := $(exec_prefix)/bin

clean:
	$(RM) gmvread gmvread.o

install: gmvread gmv2obj | $(DESTDIR)$(bindir)
	$(INSTALL_PROGRAM) gmvread $(DESTDIR)$(bindir)/
	$(INSTALL_PROGRAM) gmv2obj $(DESTDIR)$(bindir)/

$(DESTDIR)$(bindir):
	mkdir -p $@

gmvread: gmvread.c gmvread.h
	gcc -D_GNU_SOURCE -I. $(CFLAGS) -o $@ $<
