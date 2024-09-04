# Makefile

# defaults
SIM ?= verilator
TOPLEVEL_LANG ?= verilog

# PWD=$(shell pwd)

# VERILOG_SOURCES = $(PWD)/../src/stack.v

# TOPLEVEL := stack
# MODULE := stack/stack_cocotb

VERILOG_SOURCES = $(PWD)/../../src/instructions/push.sv

TOPLEVEL := push
MODULE := push_cocotb

include $(shell cocotb-config --makefiles)/Makefile.sim