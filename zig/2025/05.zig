const std = @import("std");
const utils = @import("utils.zig");

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

    var in_ranges = true;
    var ranges_buf: [200]Range = undefined;
    var ranges = std.ArrayList(Range){
        .items = ranges_buf[0..0],
        .capacity = ranges_buf.len,
    };

    while (try reader.takeDelimiter('\n')) |line| {
        if (in_ranges) {
            if (line.len == 0) {
                in_ranges = false;
                continue;
            }
            const hyphen_i = std.mem.indexOf(u8, line, "-").?;
            try ranges.appendBounded(.{
                .left = try std.fmt.parseInt(usize, line[0..hyphen_i], 10),
                .right = try std.fmt.parseInt(usize, line[hyphen_i + 1 ..], 10),
            });
        } else {
            const num = try std.fmt.parseInt(usize, line, 10);
            for (ranges.items) |rng| {
                if (rng.contains(num)) {
                    part1 += 1;
                    break;
                }
            }
        }
    }

    var reduced_ranges_buf: [200]Range = undefined;
    var reduced_ranges = std.ArrayList(Range){
        .items = reduced_ranges_buf[0..0],
        .capacity = reduced_ranges_buf.len,
    };

    for (ranges.items) |rng| {
        var i: usize = 0;
        while (i < reduced_ranges.items.len) : (i += 1) {
            if (reduced_ranges.items[i].remove(rng)) |second_part| {
                try reduced_ranges.appendBounded(second_part);
            }
        }
        try reduced_ranges.appendBounded(rng);
    }

    for (reduced_ranges.items) |rng| {
        part2 += rng.len();
    }

    return .{
        .part1 = part1,
        .part2 = part2,
    };
}

const Range = struct {
    const zero: Range = .{ .left = 1, .right = 0 };

    left: usize,
    right: usize,

    fn contains(self: Range, val: usize) bool {
        return val >= self.left and val <= self.right;
    }

    fn remove(self: *Range, other: Range) ?Range {
        if (self.is_zero() or other.is_zero()) {
            // cannot overlap with zero
            return null;
        }
        if (self.left > other.right or self.right < other.left) {
            // ranges miss each other
            return null;
        }
        if (self.left >= other.left and self.right <= other.right) {
            // we're fully contained within other
            self.* = zero;
            return null;
        }
        if (self.left < other.left and self.right > other.right) {
            // we get split into 2 parts
            const second_part: Range = .{
                .left = other.right + 1,
                .right = self.right,
            };
            self.right = other.left - 1;
            return second_part;
        }
        if (self.left < other.left) {
            // only left side left
            self.right = other.left - 1;
            return null;
        }
        // only right side left
        self.left = other.right + 1;
        return null;
    }

    fn is_zero(self: Range) bool {
        return self.left == zero.left and self.right == zero.right;
    }

    fn len(self: Range) usize {
        return self.right + 1 - self.left;
    }
};

test "sample" {
    const sample =
        \\3-5
        \\10-14
        \\16-20
        \\12-18
        \\
        \\1
        \\5
        \\8
        \\11
        \\17
        \\32
        \\
    ;
    var reader = std.io.Reader.fixed(sample);
    const result = try processBuf(&reader);
    try std.testing.expectEqual(3, result.part1);
    try std.testing.expectEqual(14, result.part2);
}
