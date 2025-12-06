const std = @import("std");

const buf_cap: usize = 20000;
const lines_cap: usize = 10;
const columns_cap: usize = 1000;

pub fn main() !void {
    const file = try readFileFromArg();
    defer file.close();
    var buf: [4096]u8 = undefined;
    var reader = file.reader(&buf);
    const result = try processBuf(&reader.interface);
    try printStdOutUnsafe("{}\n{}\n", .{ result.part1, result.part2 });
}

const Result = struct {
    part1: u64,
    part2: u64,
};

fn processBuf(reader: *std.io.Reader) !Result {
    var part1: u64 = 0;
    var part2: u64 = 0;

    // read data into buffer
    var data: [buf_cap]u8 = undefined;
    const len = try reader.readSliceShort(&data);
    if (len == data.len) {
        return error.BufferTooSmall;
    }
    const buf = data[0..len];

    // find lines
    var line_count: usize = 0;
    var offset: usize = 0;
    var newlines: [lines_cap]usize = undefined;
    while (offset < len) {
        const next_newline = std.mem.indexOfScalarPos(u8, buf, offset, '\n');
        if (next_newline) |val| {
            newlines[line_count] = val;
            line_count += 1;
            offset = val + 1;
        } else {
            newlines[line_count] = len;
            line_count += 1;
            break;
        }
    }

    // find columns
    var columns: [columns_cap]usize = undefined;
    var column_count: usize = 0;
    const line_len = newlines[0];
    var i: usize = 0;
    while (i < line_len) : (i += 1) {
        var l: usize = 0;
        const empty_column = while (l < line_count) : (l += 1) {
            const left = if (l == 0) 0 else newlines[l - 1] + 1;
            const c = buf[left + i];
            if (c != ' ') {
                break false;
            }
        } else true;
        if (empty_column) {
            columns[column_count] = i;
            column_count += 1;
        }
    }
    columns[column_count] = line_len;
    column_count += 1;

    // solve
    var col: usize = 0;
    while (col < column_count) : (col += 1) {
        const col_offset = if (col == 0) 0 else columns[col - 1] + 1;
        const col_end_offset = columns[col];
        const op = op: {
            const l = line_count - 1;
            const left = newlines[l - 1] + 1;
            break :op buf[left + col_offset];
        };
        std.debug.assert(op == '+' or op == '*');

        // part 1
        var acc: u64 = if (op == '+') 0 else 1;
        var l: usize = 0;
        while (l < line_count - 1) : (l += 1) {
            const left = if (l == 0) 0 else newlines[l - 1] + 1;
            const cell_start = left + col_offset;
            const cell_end = left + col_end_offset;
            const cell = buf[cell_start..cell_end];
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
            l = 0;
            var num: u64 = 0;
            while (l < line_count - 1) : (l += 1) {
                const left = if (l == 0) 0 else newlines[l - 1] + 1;
                const digit_pos = left + cell_col;
                const c = buf[digit_pos];
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

fn readFileFromArg() !std.fs.File {
    var args = std.process.args();
    _ = args.next();
    const path = args.next();
    if (path == null) {
        return error.InvalidNumberOfArguments;
    }
    return std.fs.cwd().openFile(path.?, .{});
}

fn printStdOutUnsafe(comptime fmt: []const u8, args: anytype) !void {
    var buf: [64]u8 = undefined;
    var writer = std.fs.File.stdout().writer(&buf);
    try writer.interface.print(fmt, args);
    try writer.interface.flush();
}
