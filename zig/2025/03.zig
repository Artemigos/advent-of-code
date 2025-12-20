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
    var part1: u64 = 0;
    var part2: u64 = 0;
    while (try reader.takeDelimiter('\n')) |line| {
        var solution1 = Solution(2){};
        var solution2 = Solution(12){};

        var i: usize = 0;
        while (i < line.len) : (i += 1) {
            const digit = line[i] - '0';
            const n_digits_left = line.len - i - 1;
            solution1.observeDigit(digit, n_digits_left);
            solution2.observeDigit(digit, n_digits_left);
        }

        part1 += solution1.max;
        part2 += solution2.max;
    }

    return .{
        .part1 = part1,
        .part2 = part2,
    };
}

fn Solution(comptime w: u8) type {
    return struct {
        const Self = @This();

        digits: [w]u8 = .{0} ** w,
        max: u64 = 0,

        fn observeDigit(self: *Self, digit: u8, n_digits_left: usize) void {
            if (digit > self.digits[w - 1]) {
                self.digits[w - 1] = digit;
                self.collectNewMax();
            }

            var i: u8 = 0;
            while (i < w - 1) : (i += 1) {
                const need_x_more = w - i - 1;
                if (need_x_more > n_digits_left) {
                    continue;
                }
                if (digit > self.digits[i]) {
                    self.digits[i] = digit;
                    var j: u8 = i + 1;
                    while (j < w) : (j += 1) {
                        self.digits[j] = 0;
                    }
                    break;
                }
            }
        }

        fn collectNewMax(self: *Self) void {
            var acc: u64 = 0;
            var i: u8 = 0;
            while (i < w) : (i += 1) {
                acc *= 10;
                acc += self.digits[i];
            }
            self.max = acc;
        }
    };
}

test "sample" {
    const sample =
        \\987654321111111
        \\811111111111119
        \\234234234234278
        \\818181911112111
    ;
    var reader = std.io.Reader.fixed(sample);
    const result = try processBuf(&reader);
    try std.testing.expectEqual(357, result.part1);
    try std.testing.expectEqual(3121910778619, result.part2);
}
