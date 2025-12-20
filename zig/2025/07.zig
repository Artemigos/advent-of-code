const std = @import("std");
const utils = @import("utils.zig");

const buf_cap: usize = 30000;
const lines_cap: usize = 200;

pub fn main() !void {
    const file = try utils.io.readFileFromArg();
    defer file.close();
    var buf: [4096]u8 = undefined;
    var reader = file.reader(&buf);
    const result = try processBuf(&reader.interface);
    try utils.io.printStdOutUnsafe("{f}", .{result});
}

fn processBuf(reader: *std.io.Reader) !utils.Result {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var data_buf: [buf_cap]u8 = undefined;
    var lines_buf: [lines_cap][]const u8 = undefined;
    const buf = try utils.io.readAllToBuffer(&data_buf, reader);
    const lines = try utils.buf.findLines(buf, &lines_buf);

    const s_x = std.mem.indexOfScalar(u8, lines[0], 'S').?;
    const s = Point{
        .x = s_x,
        .y = 0,
    };

    const fist_splitter = findSplitterBelow(lines, s).?;
    var finder = MemoFindPaths.init(allocator);
    defer finder.deinit();
    const paths = try finder.call(lines, fist_splitter);

    return .{
        .part1 = finder.cache.count(),
        .part2 = paths,
    };
}

test "sample" {
    const sample =
        \\.......S.......
        \\...............
        \\.......^.......
        \\...............
        \\......^.^......
        \\...............
        \\.....^.^.^.....
        \\...............
        \\....^.^...^....
        \\...............
        \\...^.^...^.^...
        \\...............
        \\..^...^.....^..
        \\...............
        \\.^.^.^.^.^...^.
        \\...............
        \\
    ;
    var reader = std.io.Reader.fixed(sample);
    const result = try processBuf(&reader);
    try std.testing.expectEqual(21, result.part1);
    try std.testing.expectEqual(40, result.part2);
}

const MemoFindPaths = struct {
    cache: std.AutoHashMap(Point, usize),

    fn init(allocator: std.mem.Allocator) MemoFindPaths {
        return .{
            .cache = std.AutoHashMap(Point, usize).init(allocator),
        };
    }

    fn deinit(self: *MemoFindPaths) void {
        self.cache.deinit();
    }

    fn call(
        self: *MemoFindPaths,
        lines: [][]const u8,
        splitter: Point,
    ) std.mem.Allocator.Error!usize {
        if (self.cache.get(splitter)) |ret| {
            return ret;
        }
        const ret = try self._impl(lines, splitter);
        try self.cache.put(splitter, ret);
        return ret;
    }

    fn _impl(
        self: *MemoFindPaths,
        lines: [][]const u8,
        splitter: Point,
    ) !usize {
        var result: usize = 0;
        if (splitter.x > 0) {
            if (findSplitterBelow(lines, .{
                .x = splitter.x - 1,
                .y = splitter.y,
            })) |next| {
                result += try self.call(
                    lines,
                    next,
                );
            } else {
                result += 1;
            }
        }
        if (splitter.x < lines[0].len - 1) {
            if (findSplitterBelow(lines, .{
                .x = splitter.x + 1,
                .y = splitter.y,
            })) |next| {
                result += try self.call(
                    lines,
                    next,
                );
            } else {
                result += 1;
            }
        }
        return result;
    }
};

const Point = struct {
    x: usize,
    y: usize,
};

fn findSplitterBelow(lines: [][]const u8, start: Point) ?Point {
    var y: usize = start.y;
    while (y < lines.len) : (y += 1) {
        if (lines[y][start.x] == '^') {
            return .{
                .x = start.x,
                .y = y,
            };
        }
    }
    return null;
}
