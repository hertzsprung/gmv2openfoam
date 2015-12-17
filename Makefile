MAKEFLAGS += --no-builtin-rules                                                                 
.DEFAULT_GOAL := gmvread
.DELETE_ON_ERROR:
.SUFFIXES:
.PHONY: clean

clean:
	$(RM) gmvread gmvread.o

gmvread: gmvread.c gmvread.h
	gcc -D_GNU_SOURCE -I. -o $@ $<
