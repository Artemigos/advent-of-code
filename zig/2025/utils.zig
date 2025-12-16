const std = @import("std");

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
