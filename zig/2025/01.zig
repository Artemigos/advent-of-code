const std = @import("std");

pub fn main() !void {
    const file = try readFileFromArg();
    defer file.close();
    var file_buffer: [4096]u8 = undefined;
    var file_reader = file.reader(&file_buffer);
    const result = try processBuf(&file_reader.interface);
    try printStdOutUnsafe("{}\n{}\n", .{ result.part1, result.part2 });
}

const Result = struct {
    part1: u64,
    part2: u64,
};

fn processBuf(reader: *std.io.Reader) !Result {
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
