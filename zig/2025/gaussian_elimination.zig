const std = @import("std");
const utils = @import("utils.zig");
const Matrix = @import("matrix.zig").Matrix;

pub fn run(matrix: *Matrix(f64)) void {
    var row: usize = 0;
    var col: usize = 0;
    // iterate rows
    while (row < matrix.rows) : (row += 1) {
        // look for row with any coefficient at column `col`, advancing `col` by 1 until such row is found
        var i: usize = row;
        while (@abs(matrix.get(i, col)) < 1e-10) {
            i += 1;
            if (i == matrix.rows) {
                i = row;
                col += 1;
                if (col == matrix.cols - 1) {
                    return;
                }
            }
        }

        // move that row to position `row`
        if (i != row) {
            matrix.swapRows(row, i);
        }

        // scale `row` to get 1 at the `col` coefficient
        const f = matrix.get(row, col);
        if (@abs(f - 1) > 1e-10) {
            i = 0;
            while (i < matrix.cols) : (i += 1) {
                matrix.at(row, i).* /= f;
            }
        }

        // scale and subtract row k from rows below
        i = 0;
        while (i < matrix.rows) : (i += 1) {
            if (i == row) {
                continue;
            }

            const f2 = matrix.get(i, col);
            var j: usize = col;
            while (j < matrix.cols) : (j += 1) {
                matrix.at(i, j).* -= matrix.get(row, j) * f2;
            }
        }

        col += 1;
        if (col == matrix.cols - 1) {
            return;
        }
    }
}

pub fn iterateSolution(matrix: *Matrix(f64)) SolutionIterator {
    return .{
        .matrix = matrix,
    };
}

pub const SolutionValue = union(enum) {
    known: f64,
    calculated: struct {
        matrix: *Matrix(f64),
        row: usize,
        col: usize,
    },
    unknown: struct {
        row: usize,
        col: usize,
    },
};

pub const SolutionIterator = struct {
    matrix: *Matrix(f64),
    col: usize = 0,
    row: usize = 0,

    pub fn next(self: *SolutionIterator) ?SolutionValue {
        if (self.row < self.matrix.rows and self.col < self.matrix.cols - 1) {
            if (utils.floats.eq(self.matrix.get(self.row, self.col), 1)) {
                var j: usize = self.col + 1;
                const known = l: while (j < self.matrix.cols - 1) : (j += 1) {
                    if (!utils.floats.eq(self.matrix.get(self.row, j), 0)) {
                        break :l false;
                    }
                } else true;
                if (known) {
                    self.row += 1;
                    self.col += 1;
                    return .{
                        .known = self.matrix.get(self.row - 1, self.matrix.cols - 1),
                    };
                } else {
                    self.row += 1;
                    self.col += 1;
                    return .{
                        .calculated = .{
                            .matrix = self.matrix,
                            .row = self.row - 1,
                            .col = self.col - 1,
                        },
                    };
                }
            } else {
                std.debug.assert(utils.floats.eq(self.matrix.get(self.row, self.col), 0));
                self.col += 1;
                return .{
                    .unknown = .{
                        .row = self.row,
                        .col = self.col - 1,
                    },
                };
            }
        }
        if (self.col < self.matrix.cols - 1) {
            self.col += 1;
            return .{
                .unknown = .{
                    .row = self.row,
                    .col = self.col - 1,
                },
            };
        }
        return null;
    }
};
