const std = @import("std");
const utils = @import("utils.zig");

pub fn main() !void {
    const file = try utils.io.readFileFromArg();
    defer file.close();
    var buf: [4096]u8 = undefined;
    var reader = file.reader(&buf);
    const result = try processBuf(&reader.interface);
    try utils.io.printStdOutUnsafe("{}\n", .{result});
}

fn processBuf(reader: *std.io.Reader) !u64 {
    var shapes: [6][9]bool = undefined;
    var shape_sizes: [6]usize = @splat(0);

    // read shapes
    var shape_i: usize = 0;
    while (shape_i < 6) : (shape_i += 1) {
        // discard line with index
        _ = (try reader.takeDelimiter('\n')).?;

        // collect shape data
        var i: usize = 0;
        while (i < 3) : (i += 1) {
            const shape_line = (try reader.takeDelimiter('\n')).?;
            std.debug.assert(shape_line.len == 3);
            var j: usize = 0;
            while (j < 3) : (j += 1) {
                const is_on = shape_line[j] == '#';
                shapes[shape_i][i * 3 + j] = is_on;
                if (is_on) {
                    shape_sizes[shape_i] += 1;
                }
            }
        }

        // discard empty line
        _ = (try reader.takeDelimiter('\n')).?;
    }

    // go through shape fitting
    var solution: u64 = 0;
    while (try reader.takeDelimiter('\n')) |line| {
        const x_pos = std.mem.indexOfScalar(u8, line, 'x').?;
        const colon_pos = std.mem.indexOfScalarPos(u8, line, x_pos + 1, ':').?;
        const w = try std.fmt.parseInt(usize, line[0..x_pos], 10);
        const h = try std.fmt.parseInt(usize, line[x_pos + 1 .. colon_pos], 10);

        var counts: [6]usize = undefined;
        var rest = line[colon_pos + 2 ..];
        var count_i: usize = 0;
        while (true) : (count_i += 1) {
            const num = std.mem.sliceTo(rest, ' ');
            counts[count_i] = try std.fmt.parseInt(usize, num, 10);
            if (rest.len == num.len) {
                break;
            }
            rest = rest[num.len + 1 ..];
        }

        // check if the area is too small to even fit all those shapes
        const area = w * h;
        var min_required_area: usize = 0;
        var i: usize = 0;
        while (i < 6) : (i += 1) {
            min_required_area += counts[i] * shape_sizes[i];
        }

        if (area < min_required_area) {
            continue;
        }

        // check if the area is large enough to provide a separate 3x3 box for each shape
        const grid_w = @divTrunc(w, 3);
        const grid_h = @divTrunc(h, 3);
        const grid_slots = grid_w * grid_h;
        var total_shape_count: usize = 0;
        for (counts) |ct| {
            total_shape_count += ct;
        }

        if (total_shape_count <= grid_slots) {
            solution += 1;
            continue;
        }

        // it seem this was a joke day - every line is trivially proven or disproven to work
        unreachable;
    }

    return solution;
}
