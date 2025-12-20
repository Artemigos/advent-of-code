const std = @import("std");
const utils = @import("utils.zig");

pub fn main() !void {
    const file = try utils.io.readFileFromArg();
    defer file.close();
    var file_buffer: [4096]u8 = undefined;
    var file_reader = file.reader(&file_buffer);
    const result = try processBuf(&file_reader.interface);
    try utils.io.printStdOutUnsafe("{f}", .{result});
}

fn processBuf(reader: *std.io.Reader) !utils.Result {
    var part1: usize = 0;
    var part2: usize = 0;
    var state: isize = 50;
    while (try reader.takeDelimiter('\n')) |line| {
        const dir = line[0];
        const val = try std.fmt.parseInt(isize, line[1..], 10);
        if (dir == 'L') {
            if (state == 0) {
                part2 -= 1;
            }
            state -= val;
            while (state < 0) {
                state += 100;
                part2 += 1;
            }
            if (state == 0) {
                part2 += 1;
            }
        } else if (dir == 'R') {
            state += val;
            while (state > 99) {
                state -= 100;
                part2 += 1;
            }
        } else {
            return error.UnexpectedDirection;
        }

        if (state == 0) {
            part1 += 1;
        }
    }
    return .{
        .part1 = part1,
        .part2 = part2,
    };
}

test "sample" {
    const sample =
        \\L68
        \\L30
        \\R48
        \\L5
        \\R60
        \\L55
        \\L1
        \\L99
        \\R14
        \\L82
        \\
    ;
    var reader = std.io.Reader.fixed(sample);
    const result = try processBuf(&reader);
    try std.testing.expectEqual(3, result.part1);
    try std.testing.expectEqual(6, result.part2);
}
