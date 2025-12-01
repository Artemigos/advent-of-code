const std = @import("std");

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
;

pub fn main() !void {
    // allocator
    var gpa = std.heap.GeneralPurposeAllocator(.{ .thread_safe = true }){};
    defer if (gpa.deinit() == .leak) {
        std.log.err("Memory leak", .{});
    };
    const allocator = gpa.allocator();

    // read file
    const argv = try std.process.argsAlloc(allocator);
    defer std.process.argsFree(allocator, argv);
    if (argv.len != 2) {
        return error.InvalidNumberOfArguments;
    }
    const path: []u8 = argv[1];
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close();
    var file_buffer: [4096]u8 = undefined;
    var r = file.reader(&file_buffer);
    var reader = &r.interface;

    // read sample
    // var reader = std.io.Reader.fixed(sample);

    // process line by line
    var result_part1: usize = 0;
    var result_part2: usize = 0;
    var state: isize = 50;
    while (try reader.takeDelimiter('\n')) |line| {
        const dir = line[0];
        const val = try std.fmt.parseInt(isize, line[1..], 10);
        if (dir == 'L') {
            if (state == 0) {
                result_part2 -= 1;
            }
            state -= val;
            while (state < 0) {
                state += 100;
                result_part2 += 1;
            }
            if (state == 0) {
                result_part2 += 1;
            }
        } else if (dir == 'R') {
            state += val;
            while (state > 99) {
                state -= 100;
                result_part2 += 1;
            }
        } else {
            return error.UnexpectedDirection;
        }

        if (state == 0) {
            result_part1 += 1;
        }
    }

    // print output
    var buf: [64]u8 = undefined;
    var writer = std.fs.File.stdout().writer(&buf);
    try writer.interface.print("{}\n{}\n", .{ result_part1, result_part2 });
    try writer.interface.flush();
}
