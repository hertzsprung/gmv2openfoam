MAKEFLAGS += --no-builtin-rules                                                                 
.DEFAULT_GOAL := gmvread
.DELETE_ON_ERROR:
.SUFFIXES:
.PHONY: clean install

INSTALL := cp
INSTALL_PROGRAM := $(INSTALL)
prefix := /usr/local
exec_prefix := $(prefix)
bindir := $(exec_prefix)/bin

clean:
	$(RM) gmvread gmvread.o

install: gmvread | $(DESTDIR)$(bindir)
	cp $< $(DESTDIR)$(bindir)/

$(DESTDIR)$(bindir):
	mkdir -p $@

gmvread: gmvread.c gmvread.h
	gcc -D_GNU_SOURCE -I. -o $@ $<
