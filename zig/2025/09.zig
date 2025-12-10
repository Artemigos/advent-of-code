const std = @import("std");

const points_cap: usize = 500;

pub fn main() !void {
    const file = try readFileFromArg();
    defer file.close();
    var buf: [4096]u8 = undefined;
    var reader = file.reader(&buf);
    const result = try processBuf(&reader.interface);
    try printStdOutUnsafe("{}\n{}\n", .{ result.part1, result.part2 });
}

const Result = struct {
    part1: u64,
    part2: u64,
};

fn processBuf(reader: *std.io.Reader) !Result {
    // parse input points
    var points_buf: [points_cap]Point = undefined;
    var points = std.ArrayList(Point).initBuffer(&points_buf);

    while (try reader.takeDelimiter('\n')) |line| {
        var nums: [2]usize = @splat(0);
        var at_num: usize = 0;
        var i: usize = 0;
        while (i < line.len) : (i += 1) {
            if (line[i] == ',') {
                at_num += 1;
                std.debug.assert(at_num < 2);
                continue;
            }
            nums[at_num] *= 10;
            nums[at_num] += line[i] - '0';
        }
        try points.appendBounded(.{
            .x = nums[0],
            .y = nums[1],
        });
    }

    // part 1
    var part1: u64 = 0;
    var i: usize = 0;
    while (i < points.items.len) : (i += 1) {
        const p1 = &points.items[i];
        var j: usize = i + 1;
        while (j < points.items.len) : (j += 1) {
            const p2 = &points.items[j];
            const dx = (if (p1.x < p2.x) p2.x - p1.x else p1.x - p2.x) + 1;
            const dy = (if (p1.y < p2.y) p2.y - p1.y else p1.y - p2.y) + 1;
            const area = dx * dy;
            if (area > part1) {
                part1 = area;
            }
        }
    }

    // part 2
    var lines_buf: [points_cap]Line = undefined;
    var lines = std.ArrayList(Line).initBuffer(&lines_buf);

    // find all lines
    i = 0;
    while (i < points.items.len - 1) : (i += 1) {
        try lines.appendBounded(Line.new(&points.items[i], &points.items[i + 1]));
    }
    try lines.appendBounded(Line.new(&points.items[i], &points.items[0]));

    // find vertical lines sorted by x coordinate
    var vert_lines_buf: [points_cap]*Line = undefined;
    var vert_lines = std.ArrayList(*Line).initBuffer(&vert_lines_buf);
    i = 0;
    while (i < lines.items.len) : (i += 1) {
        const l = &lines.items[i];
        if (l.vertical) {
            try vert_lines.appendBounded(l);
        }
    }
    std.sort.heap(*Line, vert_lines.items, {}, lesserX);

    // check rectangles:
    // - cast rays at top and bottom to check they're entirely in
    // - for every point within the bounds of the rectangle + it's border ray cast on point and 1 below (if also within bounds)
    i = 0;
    var part2: u64 = 0;
    while (i < points.items.len) : (i += 1) {
        const p1 = &points.items[i];
        var j: usize = i + 1;
        while (j < points.items.len) : (j += 1) {
            const p2 = &points.items[j];
            const lx = if (p1.x < p2.x) p1.x else p2.x;
            const rx = if (p1.x < p2.x) p2.x else p1.x;
            const ly = if (p1.y < p2.y) p1.y else p2.y;
            const ry = if (p1.y < p2.y) p2.y else p1.y;
            const area = (rx - lx + 1) * (ry - ly + 1);
            if (area <= part2) {
                continue;
            }
            for (points.items) |point| {
                if (point.y < ly or point.y > ry) {
                    continue;
                }
                if (!rayCastFromLeft(vert_lines.items, point.y, lx, rx)) {
                    break;
                }
                if (point.y < ry and !rayCastFromLeft(vert_lines.items, point.y + 1, lx, rx)) {
                    break;
                }
            } else {
                part2 = area;
            }
        }
    }

    return .{
        .part1 = part1,
        .part2 = part2,
    };
}

fn lesserX(_: void, l1: *Line, l2: *Line) bool {
    return l1.p1.x < l2.p1.x;
}

// ray cast from left:
// - if intersects with vertical line's inside, enter/exit polygon
// - if intersects with point make sure we're in and either:
//   - remember if we were in/out before entering and whether the vertical line was above/below, or
//   - if we have those remembered:
//      - if direction of the vert line is the same as remembered, restore remembered in/out state
//      - otherwise set in/out state to the opposite of remembered
fn rayCastFromLeft(vert_lines: []*Line, y: usize, check_start_x: usize, check_end_x: usize) bool {
    var entered_at: ?usize = null;
    const VertDir = enum { Up, Down };
    var dir_at_point: ?VertDir = null;
    const State = enum { In, Out };
    var state_at_point: ?State = null;
    const lx = if (check_start_x < check_end_x) check_start_x else check_end_x;
    const rx = if (check_start_x < check_end_x) check_end_x else check_start_x;

    for (vert_lines) |line| {
        if (rx < line.p1.x and entered_at == null) {
            // we passed the range
            break;
        }
        if (y < line.p1.y and y < line.p2.y or y > line.p1.y and y > line.p2.y) {
            // no intersection
            continue;
        }
        if (y == line.p1.y or y == line.p2.y) {
            // intersection at point
            if (dir_at_point == null) {
                // we start driving along a horizontal line
                dir_at_point = if (line.p1.y > y or line.p2.y > y) .Down else .Up;
                state_at_point = if (entered_at == null) .Out else .In;
                if (entered_at == null) {
                    entered_at = line.p1.x;
                }
            } else {
                // we stop driving along a horizontal line
                const dir_now: VertDir = if (line.p1.y > y or line.p2.y > y) .Down else .Up;
                if (dir_now == dir_at_point.? and state_at_point == .Out or dir_now != dir_at_point.? and state_at_point == .In) {
                    // exiting polygon - check success/failure conditions
                    if (entered_at.? <= lx and rx <= line.p1.x) {
                        return true;
                    } else if (entered_at.? <= lx and lx <= line.p1.x or entered_at.? <= rx and rx <= line.p1.x) {
                        return false;
                    }
                    entered_at = null;
                }
                dir_at_point = null;
                state_at_point = null;
            }
        } else {
            // intersection inside the line
            if (entered_at == null) {
                entered_at = line.p1.x;
            } else {
                // exiting polygon - check success/failure conditions
                if (entered_at.? <= lx and rx <= line.p1.x) {
                    return true;
                } else if (entered_at.? <= lx and lx <= line.p1.x or entered_at.? <= rx and rx <= line.p1.x) {
                    return false;
                }
                entered_at = null;
            }
        }
    }

    return false;
}

test "sample" {
    const sample =
        \\7,1
        \\11,1
        \\11,7
        \\9,7
        \\9,5
        \\2,5
        \\2,3
        \\7,3
        \\
    ;
    var reader = std.io.Reader.fixed(sample);
    const result = try processBuf(&reader);
    try std.testing.expectEqual(50, result.part1);
    try std.testing.expectEqual(24, result.part2);
}

const Point = struct {
    x: usize,
    y: usize,
};

const Line = struct {
    p1: *const Point,
    p2: *const Point,
    vertical: bool,

    fn new(p1: *const Point, p2: *const Point) Line {
        return .{
            .p1 = p1,
            .p2 = p2,
            .vertical = p1.x == p2.x,
        };
    }
};

fn readFileFromArg() !std.fs.File {
    var args = std.process.args();
    _ = args.next();
    const path = args.next();
    if (path == null) {
        return error.InvalidNumberOfArguments;
    }
    return std.fs.cwd().openFile(path.?, .{});
}

fn printStdOutUnsafe(comptime fmt: []const u8, args: anytype) !void {
    var buf: [64]u8 = undefined;
    var writer = std.fs.File.stdout().writer(&buf);
    try writer.interface.print(fmt, args);
    try writer.interface.flush();
}
