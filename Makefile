BUILD=build/

# Fix pdflatex search path
TGT_DIR :=
TGT_DOC :=

# Default target is 'all'. The 'build' target is defined here so that all
# sub rules.mk can add prerequisites to the 'build' target.
all:
build:

d := tests/
include base.mk
include $(d)/rules.mk

.PHONY: doc

all: doc build

clean:
	rm -rf $(CLEAN)

$(TGT_DIR):
	mkdir -p $(TGT_DIR)
