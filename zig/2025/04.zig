const std = @import("std");
const utils = @import("utils.zig");

// barely enough for my input, needs to fit it all
const buf_size = 20 * 1024;

pub fn main() !void {
    const file = try utils.io.readFileFromArg();
    defer file.close();
    var file_buffer: [buf_size]u8 = undefined;
    const size = try file.readAll(&file_buffer);
    if (size == file_buffer.len) {
        return error.FileTooLarge;
    }

    const result = try processBuf(&file_buffer, size);
    try utils.io.printStdOutUnsafe("{f}", .{result});
}

fn processBuf(data: []u8, size: usize) !utils.Result {
    var part1: u64 = 0;
    var part2: u64 = 0;

    const w = std.mem.indexOfScalar(u8, data, '\n').?;
    const stride: usize = w + 1;
    std.debug.assert(size % stride == 0);
    const h: usize = @divExact(size, stride);

    var removed: usize = std.math.maxInt(usize);
    const previous = data;
    var first_iter = true;

    while (removed > 0) {
        removed = 0;
        var workspace: [buf_size]u8 = undefined;
        @memmove(&workspace, previous);

        const checker = struct {
            const Self = @This();
            data: []const u8,
            stride: usize,
            w: usize,
            h: usize,

            fn isPaper(self: Self, ix: isize, iy: isize) usize {
                if (ix < 0 or ix >= self.w) {
                    return 0;
                }
                if (iy < 0 or iy >= self.h) {
                    return 0;
                }
                const x: usize = @intCast(ix);
                const y: usize = @intCast(iy);
                const coord = y * self.stride + x;
                return if (self.data[coord] == '@') 1 else 0;
            }
        }{ .data = previous, .stride = stride, .w = w, .h = h };

        var y: usize = 0;
        while (y < h) : (y += 1) {
            const iy: isize = @intCast(y);
            var x: usize = 0;
            while (x < w) : (x += 1) {
                const ix: isize = @intCast(x);
                if (checker.isPaper(ix, iy) == 0) {
                    continue;
                }

                const found: usize =
                    checker.isPaper(ix - 1, iy - 1) +
                    checker.isPaper(ix, iy - 1) +
                    checker.isPaper(ix + 1, iy - 1) +
                    checker.isPaper(ix - 1, iy) +
                    checker.isPaper(ix + 1, iy) +
                    checker.isPaper(ix - 1, iy + 1) +
                    checker.isPaper(ix, iy + 1) +
                    checker.isPaper(ix + 1, iy + 1);

                if (found < 4) {
                    removed += 1;
                    workspace[y * stride + x] = '.';
                }
            }
        }

        if (first_iter) {
            first_iter = false;
            part1 += removed;
        }

        part2 += removed;
        @memmove(previous, &workspace);
    }

    return .{
        .part1 = part1,
        .part2 = part2,
    };
}

test "sample" {
    const sample =
        \\..@@.@@@@.
        \\@@@.@.@.@@
        \\@@@@@.@.@@
        \\@.@@@@..@.
        \\@@.@@@@.@@
        \\.@@@@@@@.@
        \\.@.@.@.@@@
        \\@.@@@.@@@@
        \\.@@@@@@@@.
        \\@.@.@@@.@.
        \\
    ;
    var buf: [buf_size]u8 = undefined;
    @memcpy(buf[0..sample.len], sample);
    const result = try processBuf(&buf, sample.len);
    try std.testing.expectEqual(13, result.part1);
    try std.testing.expectEqual(43, result.part2);
}
