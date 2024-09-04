# Makefile

# defaults
SIM ?= verilator
TOPLEVEL_LANG ?= verilog

# PWD=$(shell pwd)

VERILOG_SOURCES = $(PWD)/../../src/interpreter.sv
VERILOG_INCLUDE_DIRS = $(PWD)/../../src

TOPLEVEL := interpreter
MODULE := interp_cocotb

# VERILOG_SOURCES = $(PWD)/../src/instructions/push.v

# TOPLEVEL := push
# MODULE := push_cocotb

include $(shell cocotb-config --makefiles)/Makefile.sim