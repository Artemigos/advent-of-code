const std = @import("std");

pub fn Matrix(comptime T: type) type {
    return struct {
        const Self = @This();

        rows: usize,
        cols: usize,
        buf: []T = undefined,
        allocator: ?std.mem.Allocator = null,

        pub fn init(alloc: std.mem.Allocator, rows: usize, cols: usize) !Self {
            const buf = try alloc.alloc(T, rows * cols);
            @memset(buf, 0);
            return Self{
                .rows = rows,
                .cols = cols,
                .buf = buf,
                .allocator = alloc,
            };
        }

        pub fn deinit(self: Self) void {
            self.allocator.?.free(self.buf);
        }

        pub fn initBuffered(buf: []T, rows: usize, cols: usize) Self {
            std.debug.assert(rows * cols == buf.len);
            return Self{
                .rows = rows,
                .cols = cols,
                .buf = buf,
            };
        }

        pub fn get(self: Self, y: usize, x: usize) T {
            std.debug.assert(y < self.rows);
            std.debug.assert(x < self.cols);
            const i = y * self.cols + x;
            return self.buf[i];
        }

        pub fn at(self: *Self, y: usize, x: usize) *T {
            std.debug.assert(y < self.rows);
            std.debug.assert(x < self.cols);
            const i = y * self.cols + x;
            return &self.buf[i];
        }

        pub fn add(self: *Self, other: Self) void {
            std.debug.assert(self.rows == other.rows);
            std.debug.assert(self.cols == other.cols);
            var y: usize = 0;
            while (y < self.rows) : (y += 1) {
                var x: usize = 0;
                while (x < self.cols) : (x += 1) {
                    self.at(y, x).* += other.get(y, x);
                }
            }
        }

        pub fn is_vec(self: Self) bool {
            return self.rows == 1 or self.cols == 1;
        }

        pub fn vec_at(self: *Self, x: usize) *T {
            std.debug.assert(self.is_vec());
            if (self.rows == 1) {
                return self.at(0, x);
            }
            return self.at(x, 0);
        }

        pub fn vec_get(self: Self, x: usize) T {
            std.debug.assert(self.is_vec());
            if (self.rows == 1) {
                return self.get(0, x);
            }
            return self.get(x, 0);
        }

        pub fn vec_len(self: Self) usize {
            std.debug.assert(self.is_vec());
            if (self.rows == 1) {
                return self.cols;
            }
            return self.rows;
        }

        pub fn vec_mul_sum(self: Self, other: Self) T {
            std.debug.assert(self.is_vec());
            std.debug.assert(other.is_vec());
            const len1 = self.vec_len();
            const len2 = other.vec_len();
            std.debug.assert(len1 == len2);
            var acc: T = 0;
            var i: usize = 0;
            while (i < len1) : (i += 1) {
                acc += self.vec_get(i) * other.vec_get(i);
            }
            return acc;
        }

        pub fn swapRows(self: *Self, i: usize, j: usize) void {
            std.debug.assert(i != j);
            var col: usize = 0;
            while (col < self.cols) : (col += 1) {
                const tmp = self.get(i, col);
                self.at(i, col).* = self.get(j, col);
                self.at(j, col).* = tmp;
            }
        }

        pub fn format(self: Self, writer: *std.io.Writer) !void {
            var y: usize = 0;
            while (y < self.rows) : (y += 1) {
                const start = if (self.rows == 1) "[" else if (y == 0) "┌ " else if (y == self.rows - 1) "└ " else "│ ";
                try writer.writeAll(start);
                var x: usize = 0;
                while (x < self.cols) : (x += 1) {
                    var max_w: u64 = 0;
                    var curr_w: u64 = 0;
                    var buf: [32]u8 = undefined;
                    var row: usize = 0;
                    while (row < self.rows) : (row += 1) {
                        var counter = std.io.Writer.Discarding.init(&buf);
                        try counter.writer.print("{d:.1}", .{self.get(row, x)});
                        const count = counter.fullCount();
                        if (count > max_w) {
                            max_w = count;
                        }
                        if (row == y) {
                            curr_w = count;
                        }
                    }
                    const w_diff = max_w - curr_w;
                    var i: usize = 0;
                    while (i < w_diff) : (i += 1) {
                        try writer.print(" ", .{});
                    }

                    if (x == self.cols - 1) {
                        try writer.print("{d:.1}", .{self.get(y, x)});
                    } else {
                        try writer.print("{d:.1}, ", .{self.get(y, x)});
                    }
                }
                const end = if (self.rows == 1) "]" else if (y == 0) " ┐\n" else if (y == self.rows - 1) " ┘" else " │\n";
                try writer.writeAll(end);
            }
        }
    };
}
