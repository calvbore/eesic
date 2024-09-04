module swap (
    input wire  [7:0]   opcode,
    input wire  [9:0]   stack_height,
    input wire  [255:0] stack_data [0:16],
    output wire [255:0] data_out   [0:16],
    output wire [4:0]   push_num,
    output wire [4:0]   pop_num,
    output wire [31:0]  gas,
    output wire         exit
);
// use five bits to accomadate 17 items on stack
wire [4:0] item_sel;
assign item_sel = opcode[3:0] + 1;

genvar i;
for (i=1; i<17; i++) begin
    assign data_out[i] = (i == item_sel) ? stack_data[0] : stack_data[i];
end

// swap the first stack item
assign data_out[0] = stack_data[item_sel];

// push and pop the same number onto the stack
assign push_num    = item_sel+1;
assign pop_num     = item_sel+1;

assign gas         = 3;

// throw if stack smaller that index we want to swap
assign exit = stack_height < 10'(item_sel)+1 ? 1 : 0; 
    
endmodule