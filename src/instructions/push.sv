module push(
    input wire  [7:0]   opcode,
    input wire  [255:0] data_in,
    output reg  [255:0] data_out,
    output wire [4:0]   push_num,
    output wire [5:0]   pc_nxt,
    output wire [31:0]  gas
);

wire [4:0] push_bytes = opcode[4:0];

reg [255:0] masked_data;

always @(*) begin
    if (opcode == 8'h5f) begin
        // PUSH0
        masked_data = 0;
        data_out    = 0;
        // pc_nxt   = 16'b1;
    end else begin
        // PUSH1 - PUSH32
        // Mask data_in by bytes specified in the opcode
        masked_data = data_in & ({256{1'b1}} << (8*(32-(push_bytes+1))));
        data_out    = masked_data >> (8*(32-(push_bytes+1)));
    end
end

assign push_num = 1;
assign pc_nxt   = opcode == 8'h5f ? 1 : (push_bytes)+1;
assign gas      = opcode == 8'h5f ? 2 : 3;

endmodule