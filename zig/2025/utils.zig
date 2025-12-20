const std = @import("std");

pub const buf = struct {
    pub fn findLines(buffer: []u8, lines_buf: [][]u8) ![][]u8 {
        var lines = std.ArrayList([]u8).initBuffer(lines_buf);
        var offset: usize = 0;
        while (offset < buffer.len) {
            const next_newline = std.mem.indexOfScalarPos(u8, buffer, offset, '\n');
            if (next_newline) |val| {
                try lines.appendBounded(buffer[offset..val]);
                offset = val + 1;
            } else {
                try lines.appendBounded(buffer[offset..buffer.len]);
                break;
            }
        }

        return lines.items;
    }
};

pub const floats = struct {
    // NOTE: ugly, but it's fine for the purpose of this repo
    pub var equality_threshold: f64 = 1e-10;

    pub fn isCloseToInt(T: type, val: f64) bool {
        const converted: T = @intFromFloat(std.math.round(val));
        return eq(val, converted);
    }

    pub fn eq(val: f64, expected: anytype) bool {
        const T = @TypeOf(expected);
        return switch (@typeInfo(T)) {
            .int, .comptime_int => @abs(val - @as(f64, @floatFromInt(expected))) < equality_threshold,
            .float, .comptime_float => @abs(val - expected) < equality_threshold,
            else => @compileError("unsupported comparison to f64 for " ++ @typeName(T)),
        };
    }

    pub fn toInt(T: type, val: f64) !T {
        const converted: T = @intFromFloat(std.math.round(val));
        if (!eq(val, converted)) {
            return error.FloatTooFarFromInt;
        }
        return converted;
    }
};

pub const int = struct {
    pub fn countDigits(comptime T: type, num: T, base: T) !usize {
        var digits: usize = 0;
        var curr = num;
        while (curr > 0) : (curr = try std.math.divTrunc(T, curr, base)) {
            digits += 1;
        }
        return digits;
    }
};

pub const io = struct {
    pub fn readFileFromArg() !std.fs.File {
        var args = std.process.args();
        _ = args.next();
        const path = args.next();
        if (path == null) {
            return error.InvalidNumberOfArguments;
        }
        return std.fs.cwd().openFile(path.?, .{});
    }

    pub fn printStdOutUnsafe(comptime fmt: []const u8, args: anytype) !void {
        var buffer: [64]u8 = undefined;
        var writer = std.fs.File.stdout().writer(&buffer);
        try writer.interface.print(fmt, args);
        try writer.interface.flush();
    }

    pub fn readAllToBuffer(buffer: []u8, reader: *std.io.Reader) ![]u8 {
        const len = try reader.readSliceShort(buffer);
        if (len == buffer.len) {
            return error.BufferTooSmall;
        }
        return buffer[0..len];
    }
};

pub const Result = struct {
    part1: u64,
    part2: u64,

    pub fn format(self: Result, writer: *std.io.Writer) !void {
        try writer.print("{}\n{}\n", .{ self.part1, self.part2 });
    }
};
