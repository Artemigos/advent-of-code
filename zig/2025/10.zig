const std = @import("std");
const utils = @import("utils.zig");
const Matrix = @import("matrix.zig").Matrix;
const solver = @import("gaussian_elimination.zig");

pub fn main() !void {
    const file = try utils.io.readFileFromArg();
    defer file.close();
    var buf: [4096]u8 = undefined;
    var reader = file.reader(&buf);
    const result = try processBuf(&reader.interface);
    try utils.io.printStdOutUnsafe("{f}", .{result});
}

const Bits = usize;
const BitsWidth = std.meta.Int(.unsigned, std.math.log2_int(u16, @bitSizeOf(Bits)));

fn Step(Payload: type) type {
    return struct {
        const Self = @This();
        depth: usize,
        payload: Payload,

        fn new(depth: usize, payload: Payload) Self {
            return .{
                .depth = depth,
                .payload = payload,
            };
        }

        fn cmp(_: void, a: Self, b: Self) std.math.Order {
            if (a.depth < b.depth) {
                return .lt;
            } else if (a.depth == b.depth) {
                return .eq;
            }
            return .gt;
        }
    };
}

const Step1 = Step(Bits);

fn processBuf(reader: *std.io.Reader) !utils.Result {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();

    var part1: u64 = 0;
    var part2: u64 = 0;

    while (try reader.takeDelimiter('\n')) |line| {
        const lights_end = std.mem.indexOfScalar(u8, line, ']').?;
        const lights = line[1..lights_end];
        var light_bits: Bits = 0;
        var bit: BitsWidth = 0;
        while (bit < lights.len) : (bit += 1) {
            if (lights[bit] == '#') {
                light_bits |= @as(Bits, 1) << bit;
            }
        }

        var buttons = try std.ArrayList(Bits).initCapacity(alloc, 10);
        defer buttons.deinit(alloc);
        var nums = try std.ArrayList(u16).initCapacity(alloc, 15);
        defer nums.deinit(alloc);

        var at: usize = lights_end + 1;
        while (std.mem.indexOfScalarPos(u8, line, at, '(')) |open_pos| {
            const close_pos = std.mem.indexOfScalarPos(u8, line, open_pos + 1, ')').?;
            at = close_pos + 1;

            const inside = line[open_pos + 1 .. close_pos];
            var light_toggles: Bits = 0;
            var inside_at: usize = 0;
            while (std.mem.indexOfScalarPos(u8, inside, inside_at, ',')) |comma_pos| {
                const num: BitsWidth = try std.fmt.parseInt(BitsWidth, inside[inside_at..comma_pos], 10);
                light_toggles |= @as(Bits, 1) << num;
                inside_at = comma_pos + 1;
            }
            const num: BitsWidth = try std.fmt.parseInt(BitsWidth, inside[inside_at..inside.len], 10);
            light_toggles |= @as(Bits, 1) << num;

            try buttons.append(alloc, light_toggles);
        }

        const nums_start = std.mem.indexOfScalarPos(u8, line, at, '{').?;
        at = nums_start + 1;
        while (std.mem.indexOfScalarPos(u8, line, at, ',')) |comma_pos| {
            const num: u16 = try std.fmt.parseInt(u16, line[at..comma_pos], 10);
            try nums.append(alloc, num);
            at = comma_pos + 1;
        }
        const num: u16 = try std.fmt.parseInt(u16, line[at .. line.len - 1], 10);
        try nums.append(alloc, num);

        // part 1
        var q = std.PriorityDequeue(Step1, void, Step1.cmp).init(alloc, {});
        defer q.deinit();
        try q.add(Step1.new(0, light_bits));
        part1 += search: while (q.len > 0) {
            const curr = q.removeMin();
            const depth = curr.depth;
            const bits: Bits = curr.payload;

            for (buttons.items) |btn| {
                const new: Bits = bits ^ btn;
                if (new == 0) {
                    break :search depth + 1;
                }
                try q.add(Step1.new(depth + 1, new));
            }
        } else unreachable;

        // part 2
        var matrix = try Matrix(f64).init(alloc, nums.items.len, buttons.items.len + 1);
        defer matrix.deinit();

        // convert buttons and levers to an (augmented) equation system matrix
        var i: usize = 0;
        while (i < buttons.items.len) : (i += 1) {
            const btn = buttons.items[i];
            var idx: BitsWidth = 0;
            while (idx < nums.items.len) : (idx += 1) {
                const mask = @as(Bits, 1) << idx;
                if (btn & mask > 0) {
                    matrix.at(idx, i).* = 1;
                }
            }
        }

        i = 0;
        while (i < nums.items.len) : (i += 1) {
            matrix.at(i, buttons.items.len).* = @floatFromInt(nums.items[i]);
        }

        // solve equation system (as far as possible)
        solver.run(&matrix);

        // divide buttons into knowns, calculated and unkowns
        const ButtonState = union(enum) {
            known: f64, // known value
            calculated: Matrix(f64), // coefficiets to calculate
            unknown: usize, // max value it could have
        };
        var unknowns = try std.ArrayList(usize).initCapacity(alloc, 5);
        defer unknowns.deinit(alloc);
        var calculated: usize = 0;
        var button_states = try std.ArrayList(ButtonState).initCapacity(alloc, 10);
        defer {
            for (button_states.items) |btn| {
                if (btn == .calculated) {
                    btn.calculated.deinit();
                }
            }
            button_states.deinit(alloc);
        }
        var iter = solver.iterateSolution(&matrix);
        while (iter.next()) |param| switch (param) {
            .known => {
                try button_states.append(alloc, .{
                    .known = param.known,
                });
            },
            .calculated => {
                var vec = try Matrix(f64).init(alloc, 1, matrix.cols);
                var k: usize = param.calculated.col + 1;
                while (k < matrix.cols - 1) : (k += 1) {
                    vec.vec_at(k).* = matrix.get(param.calculated.row, k) * -1;
                }
                vec.vec_at(matrix.cols - 1).* = matrix.get(param.calculated.row, matrix.cols - 1);
                try button_states.append(alloc, .{
                    .calculated = vec,
                });
                calculated += 1;
            },
            .unknown => {
                const btn = buttons.items[param.unknown.col];
                var min_num: u16 = std.math.maxInt(u16);
                var btn_i: BitsWidth = 0;
                while (btn_i < nums.items.len) : (btn_i += 1) {
                    const mask = @as(usize, 1) << btn_i;
                    if (btn & mask > 0) {
                        min_num = @min(min_num, nums.items[btn_i]);
                    }
                }
                try button_states.append(alloc, .{
                    .unknown = min_num,
                });
                try unknowns.append(alloc, param.unknown.col);
            },
        };

        if (unknowns.items.len == 0) {
            std.debug.assert(calculated == 0);
            for (button_states.items) |state| {
                std.debug.assert(state == .known);
                const val = try utils.floats.toInt(u64, state.known);
                part2 += val;
            }
        } else {
            // collect calculated buttons into one formula and known ones into a val
            var known_val: u64 = 0;
            for (button_states.items) |state| {
                if (state == .known) {
                    known_val += try utils.floats.toInt(u64, state.known);
                }
            }
            var vars_mx = try Matrix(f64).init(alloc, 1, matrix.cols);
            defer vars_mx.deinit();
            vars_mx.at(0, vars_mx.cols - 1).* = 1;

            // brute-force remaining unknowns
            var min_presses: u64 = std.math.maxInt(u64);
            var unknown_vals = try std.ArrayList(u16).initCapacity(alloc, unknowns.items.len);
            defer unknown_vals.deinit(alloc);
            i = 0;
            while (i < unknowns.items.len) : (i += 1) {
                try unknown_vals.appendBounded(0);
            }
            var did_zero = false; // weird trick, but I'm tired
            outer: while (true) {
                // increase by one
                if (did_zero) {
                    var curr_i: usize = 0;
                    while (curr_i < unknowns.items.len) : (curr_i += 1) {
                        unknown_vals.items[curr_i] += 1;
                        var lower_i: usize = curr_i;
                        while (lower_i > 0) {
                            lower_i -= 1;
                            unknown_vals.items[lower_i] = 0;
                        }
                        const unknown_idx = unknowns.items[curr_i];
                        const max = button_states.items[unknown_idx].unknown;
                        if (unknown_vals.items[curr_i] <= max) {
                            break;
                        }
                    } else {
                        break;
                    }
                } else {
                    did_zero = true;
                }

                // find current sum
                var presses = known_val;
                var curr_i: usize = 0;
                while (curr_i < unknown_vals.items.len) : (curr_i += 1) {
                    const val = unknown_vals.items[curr_i];
                    presses += val;
                    const unknown_idx = unknowns.items[curr_i];
                    vars_mx.at(0, unknown_idx).* = @floatFromInt(val);
                }
                var button_i: usize = 0;
                for (button_states.items) |state| {
                    if (state == .calculated) {
                        const calc = state.calculated.vec_mul_sum(vars_mx);
                        if (calc < 0 and !utils.floats.eq(calc, 0)) {
                            continue :outer;
                        }
                        if (!utils.floats.isCloseToInt(u64, calc)) {
                            continue :outer;
                        }
                        presses += try utils.floats.toInt(u16, calc);
                    }
                    button_i += 1;
                }
                min_presses = @min(min_presses, presses);
            }

            part2 += min_presses;
        }
    }

    return .{
        .part1 = part1,
        .part2 = part2,
    };
}

test "sample" {
    const sample =
        \\[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        \\[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        \\[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
        \\
    ;
    var reader = std.io.Reader.fixed(sample);
    const result = try processBuf(&reader);
    try std.testing.expectEqual(7, result.part1);
    try std.testing.expectEqual(33, result.part2);
}
