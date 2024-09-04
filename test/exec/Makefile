# Makefile

# defaults
SIM ?= verilator
TOPLEVEL_LANG ?= verilog

# PWD=$(shell pwd)

VERILOG_SOURCES = $(PWD)/../../src/execution.sv
VERILOG_INCLUDE_DIRS = $(PWD)/../../src

TOPLEVEL := execution
MODULE := exec_cocotb

# VERILOG_SOURCES = $(PWD)/../src/instructions/push.v

# TOPLEVEL := push
# MODULE := push_cocotb

include $(shell cocotb-config --makefiles)/Makefile.sim