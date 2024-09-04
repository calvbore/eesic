from cocotb_test.simulator import run

def test_push():
    run(
        verilog_sources=["../src/instructions/push.sv"],
        toplevel="push",
        module="push_cocotb",
    )