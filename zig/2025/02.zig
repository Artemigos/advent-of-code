const std = @import("std");
const utils = @import("utils.zig");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const file = try utils.io.readFileFromArg();
    defer file.close();
    var file_buffer: [4096]u8 = undefined;
    var file_reader = file.reader(&file_buffer);
    const result = try processBuf(allocator, &file_reader.interface);
    try utils.io.printStdOutUnsafe("{f}", .{result});
}

fn processBuf(allocator: std.mem.Allocator, reader: *std.io.Reader) !utils.Result {
    var part1: u64 = 0;
    var part2: u64 = 0;
    while (try reader.takeDelimiter(',')) |range| {
        const rng = std.mem.trimEnd(u8, range, "\n");
        const comma_idx = findIndex(rng, '-').?;
        const left = rng[0..comma_idx];
        const right = rng[comma_idx + 1 ..];

        const left_w = left.len;
        const right_w = right.len;

        const left_val = try std.fmt.parseInt(u64, left, 10);
        const right_val = try std.fmt.parseInt(u64, right, 10);

        var set1 = std.AutoHashMap(u64, void).init(allocator);
        defer set1.deinit();
        var set2 = std.AutoHashMap(u64, void).init(allocator);
        defer set2.deinit();

        var i = @max(left_w, 2);
        while (i <= right_w) : (i += 1) {
            if (i % 2 == 0) {
                var gen1 = ChainedGenerator.new(&.{
                    .{ .digits = try std.math.divExact(u64, i, 2), .repetitions = 2 },
                });
                while (gen1.next()) |val| {
                    if (try set1.fetchPut(val, {})) |_| {
                        continue;
                    }
                    if (val >= left_val and val <= right_val) {
                        part1 += val;
                    }
                }
            }

            var gen2 = try createGen(i);
            while (gen2.next()) |val| {
                if (try set2.fetchPut(val, {})) |_| {
                    continue;
                }
                if (val >= left_val and val <= right_val) {
                    part2 += val;
                }
            }
        }
    }

    return .{
        .part1 = part1,
        .part2 = part2,
    };
}

test "sample" {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const sample = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124";
    var reader = std.io.Reader.fixed(sample);
    const result = try processBuf(allocator, &reader);
    try std.testing.expect(result.part1 == 1227775554);
    try std.testing.expect(result.part2 == 4174379265);
}

fn findIndex(data: []const u8, to_find: u8) ?usize {
    var i: usize = 0;
    while (i < data.len) : (i += 1) {
        if (data[i] == to_find) {
            return i;
        }
    }
    return null;
}

fn countDigits(comptime T: type, num: T, base: T) !usize {
    var digits: usize = 0;
    var curr = num;
    while (curr > 0) : (curr = try std.math.divTrunc(T, curr, base)) {
        digits += 1;
    }
    return digits;
}

fn createGen(totalDigits: u64) !ChainedGenerator {
    return switch (totalDigits) {
        2 => ChainedGenerator.new(&.{
            .{ .digits = 1, .repetitions = 2 },
        }),
        3 => ChainedGenerator.new(&.{
            .{ .digits = 1, .repetitions = 3 },
        }),
        4 => ChainedGenerator.new(&.{
            .{ .digits = 1, .repetitions = 4 },
            .{ .digits = 2, .repetitions = 2 },
        }),
        5 => ChainedGenerator.new(&.{
            .{ .digits = 1, .repetitions = 5 },
        }),
        6 => ChainedGenerator.new(&.{
            .{ .digits = 1, .repetitions = 6 },
            .{ .digits = 2, .repetitions = 3 },
            .{ .digits = 3, .repetitions = 2 },
        }),
        7 => ChainedGenerator.new(&.{
            .{ .digits = 1, .repetitions = 7 },
        }),
        8 => ChainedGenerator.new(&.{
            .{ .digits = 1, .repetitions = 8 },
            .{ .digits = 2, .repetitions = 4 },
            .{ .digits = 4, .repetitions = 2 },
        }),
        9 => ChainedGenerator.new(&.{
            .{ .digits = 1, .repetitions = 9 },
            .{ .digits = 3, .repetitions = 3 },
        }),
        10 => ChainedGenerator.new(&.{
            .{ .digits = 1, .repetitions = 10 },
            .{ .digits = 2, .repetitions = 5 },
            .{ .digits = 5, .repetitions = 2 },
        }),
        else => error.UnsupportedNumberOfTotalDigits,
    };
}

const ChainedGenerator = struct {
    const GeneratorSpec = struct { digits: u64, repetitions: u64 };
    generators: []const GeneratorSpec,
    _at_generator: usize = 0,
    _current: u64 = 0,
    _mul: u64 = 0,
    _max: u64 = 0,

    fn new(generators: []const GeneratorSpec) ChainedGenerator {
        var result: ChainedGenerator = .{
            .generators = generators,
        };
        result._init();
        return result;
    }

    fn _init(self: *ChainedGenerator) void {
        // calculate mul
        const current_gen = self.generators[self._at_generator];
        const digits = current_gen.digits;
        const repetitions = current_gen.repetitions;
        const shift = std.math.pow(u64, 10, digits);
        self._mul = 0;
        var i: u64 = 0;
        while (i < repetitions) : (i += 1) {
            self._mul *= shift;
            self._mul += 1;
        }

        // calculate start and end
        self._current = std.math.pow(u64, 10, digits - 1);
        self._max = std.math.pow(u64, 10, digits);
    }

    fn next(self: *ChainedGenerator) ?u64 {
        while (self._at_generator < self.generators.len) {
            if (self._current < self._max) {
                const result = self._current * self._mul;
                self._current += 1;
                return result;
            }
            self._at_generator += 1;
            if (self._at_generator < self.generators.len) {
                self._init();
            }
        }
        return null;
    }
};
