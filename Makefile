BUILD=build/
CLEAN=*.pyc src/*.pyc src/optimize/*.pyc parser.out parsetab.py in.s out.s

# Fix pdflatex search path
TGT_DIR := report

# Default target is 'all'. The 'build' target is defined here so that all
# sub rules.mk can add prerequisites to the 'build' target.
all:
build:

d := report/
include base.mk
include $(d)/rules.mk

d := tests/
include base.mk
include $(d)/rules.mk

all: report

clean:
	rm -rf $(CLEAN)

$(TGT_DIR):
	mkdir -p $(TGT_DIR)
