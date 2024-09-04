# Makefile

# defaults
SIM ?= verilator
TOPLEVEL_LANG ?= verilog

# PWD=$(shell pwd)

VERILOG_SOURCES = $(PWD)/../../src/stack.sv

TOPLEVEL := stack
MODULE := stack_cocotb

# VERILOG_SOURCES = $(PWD)/../src/instructions/push.v

# TOPLEVEL := push
# MODULE := push_cocotb

include $(shell cocotb-config --makefiles)/Makefile.sim