module execution(
    input wire          clk,
    input wire          rst,
    input wire  [7:0]   opcode,
    input wire  [255:0] code_data,
    output wire [15:0]  pc_o, // program counter out
    output wire [31:0]  gas,
    output wire         exit
);

reg  [15:0] pc_q; // current program counter
wire [15:0] pc_d; // next program counter

// tracks how much to increase the program counter by in context.
always @(posedge clk or posedge rst) begin
    if (rst) begin
        pc_q <= 0;
    end else begin
        pc_q <= pc_q + pc_d;
    end
end

assign pc_o = pc_q;

// signals between opcodes and the stack
wire [4:0]   push_num;
wire [4:0]   pop_num;
wire [255:0] stack_data_in  [0:16];
wire [255:0] stack_data_out [0:16];
wire [9:0]   stack_height;

stack stack(
    // in
    .clk(clk),
    .rst(rst),
    .exit(exit),
    .push_num(push_num),
    .pop_num(pop_num),
    .data_in(stack_data_in), //<-----------+
    // out                                 |
    .data_out(stack_data_out), //-------+  |
    .height(stack_height) //---------+  |  |
); //                                |  |  |
//                                   |  |  |
interpreter interp( //               |  |  |
    // in                            |  |  |
    .clk(clk), //                    |  |  |
    .opcode(opcode), //              |  |  |
    .stack_height(stack_height), //<-+  |  |
    .code_data(code_data), //           |  |
    .stack_data(stack_data_out), //<----+  |
    // out                                 |
    .data_out(stack_data_in), //-----------+
    .push_num(push_num),
    .pop_num(pop_num),
    .pc_nxt(pc_d),
    .gas(gas),
    .exit(exit)
);

endmodule