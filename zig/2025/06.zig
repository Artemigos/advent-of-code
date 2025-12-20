const std = @import("std");
const utils = @import("utils.zig");

const buf_cap: usize = 20000;
const lines_cap: usize = 10;
const columns_cap: usize = 1000;

pub fn main() !void {
    const file = try utils.io.readFileFromArg();
    defer file.close();
    var buf: [4096]u8 = undefined;
    var reader = file.reader(&buf);
    const result = try processBuf(&reader.interface);
    try utils.io.printStdOutUnsafe("{f}", .{result});
}

fn processBuf(reader: *std.io.Reader) !utils.Result {
    var part1: u64 = 0;
    var part2: u64 = 0;

    var data: [buf_cap]u8 = undefined;
    const buf = try utils.io.readAllToBuffer(&data, reader);
    var lines_buf: [lines_cap][]u8 = undefined;
    const lines = try utils.buf.findLines(buf, &lines_buf);
    const w = lines[0].len;

    // find columns
    var columns: [columns_cap]usize = undefined;
    var column_count: usize = 0;
    var i: usize = 0;
    while (i < w) : (i += 1) {
        const empty_column = for (lines) |line| {
            if (line[i] != ' ') {
                break false;
            }
        } else true;
        if (empty_column) {
            columns[column_count] = i;
            column_count += 1;
        }
    }
    columns[column_count] = w;
    column_count += 1;

    // solve
    var col: usize = 0;
    while (col < column_count) : (col += 1) {
        const col_offset = if (col == 0) 0 else columns[col - 1] + 1;
        const col_end_offset = columns[col];
        const op = op: {
            const l = lines.len - 1;
            break :op lines[l][col_offset];
        };
        std.debug.assert(op == '+' or op == '*');
        const num_lines = lines[0 .. lines.len - 1];

        // part 1
        var acc: u64 = if (op == '+') 0 else 1;
        for (num_lines) |line| {
            const cell = line[col_offset..col_end_offset];
            const trimmed = std.mem.trim(u8, cell, " ");
            const num = try std.fmt.parseInt(u64, trimmed, 10);
            if (op == '+') {
                acc += num;
            } else {
                acc *= num;
            }
        }
        part1 += acc;

        // part 2
        acc = if (op == '+') 0 else 1;
        var cell_col: usize = col_end_offset - 1;
        while (cell_col >= col_offset) : (cell_col -= 1) {
            var num: u64 = 0;
            for (num_lines) |line| {
                const c = line[cell_col];
                if (c != ' ') {
                    num *= 10;
                    num += c - '0';
                }
            }
            if (op == '+') {
                acc += num;
            } else {
                acc *= num;
            }
            if (cell_col == 0) {
                // avoid underflow, we're about to end the loop anyway
                break;
            }
        }
        part2 += acc;
    }

    return .{
        .part1 = part1,
        .part2 = part2,
    };
}

test "sample" {
    const sample =
        \\123 328  51 64 
        \\ 45 64  387 23 
        \\  6 98  215 314
        \\*   +   *   +  
        \\
    ;
    var reader = std.io.Reader.fixed(sample);
    const result = try processBuf(&reader);
    try std.testing.expectEqual(4277556, result.part1);
    try std.testing.expectEqual(3263827, result.part2);
}
