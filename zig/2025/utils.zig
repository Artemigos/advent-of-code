const std = @import("std");

pub const buf = struct {
    pub fn findLines(buffer: []u8, lines_buf: [][]const u8) ![][]const u8 {
        var lines = std.ArrayList([]const u8).initBuffer(lines_buf);
        var iterator = std.mem.splitScalar(u8, buffer, '\n');
        try iter.materializeBounded([]const u8, &iterator, &lines);
        return lines.items[0 .. lines.items.len - 1];
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
    var procArgs: std.process.Args = undefined;
    var io_: std.Io = undefined;

    pub fn setup(init: std.process.Init) void {
        procArgs = init.minimal.args;
        io_ = init.io;
    }

    pub fn readFileFromArg() !std.Io.File {
        var it = procArgs.iterate();
        _ = it.next();
        const path = it.next();
        if (path == null) {
            return error.InvalidNumberOfArguments;
        }
        return try std.Io.Dir.cwd().openFile(io_, path.?, .{});
    }

    pub fn printStdOutUnsafe(comptime fmt: []const u8, args: anytype) !void {
        var buffer: [64]u8 = undefined;
        var writer = std.Io.File.stdout().writer(io_, &buffer);
        try writer.interface.print(fmt, args);
        try writer.interface.flush();
    }

    pub fn readAllToBuffer(buffer: []u8, reader: *std.Io.Reader) ![]u8 {
        const len = try reader.readSliceShort(buffer);
        if (len == buffer.len) {
            return error.BufferTooSmall;
        }
        return buffer[0..len];
    }
};

pub const iter = struct {
    pub fn materializeBounded(T: type, iterator: anytype, target: *std.ArrayList(T)) !void {
        comptime {
            var iter_type = @TypeOf(iterator);
            const iter_info = @typeInfo(iter_type);
            if (iter_info == .pointer) {
                iter_type = iter_info.pointer.child;
            }
            if (!@hasDecl(iter_type, "next")) {
                @compileError("iterator is required to have a next() function");
            }
        }

        while (iterator.next()) |item| {
            try target.appendBounded(item);
        }
    }
};

pub const Result = struct {
    part1: u64,
    part2: u64,

    pub fn format(self: Result, writer: *std.Io.Writer) !void {
        try writer.print("{}\n{}\n", .{ self.part1, self.part2 });
    }
};
