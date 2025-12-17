const std = @import("std");

const points_cap: usize = 1000;

pub fn main() !void {
    const file = try readFileFromArg();
    defer file.close();
    var buf: [4096]u8 = undefined;
    var reader = file.reader(&buf);
    const result = try processBuf(&reader.interface, 1000);
    try printStdOutUnsafe("{}\n{}\n", .{ result.part1, result.part2 });
}

const Result = struct {
    part1: u64,
    part2: u64,
};

fn processBuf(reader: *std.io.Reader, connections: usize) !Result {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const alloc = arena.allocator();

    // parse input points
    var points_buf: [points_cap]Point = undefined;
    var points = std.ArrayList(Point).initBuffer(&points_buf);

    while (try reader.takeDelimiter('\n')) |line| {
        var nums: [3]usize = @splat(0);
        var at_num: usize = 0;
        var i: usize = 0;
        while (i < line.len) : (i += 1) {
            if (line[i] == ',') {
                at_num += 1;
                std.debug.assert(at_num < 3);
                continue;
            }
            nums[at_num] *= 10;
            nums[at_num] += line[i] - '0';
        }
        try points.appendBounded(.{
            .x = nums[0],
            .y = nums[1],
            .z = nums[2],
            .circuit_num = points.items.len,
        });
    }

    // calculate and sort all distances
    // NOTE: allocating avoids a segfault
    // using a stack buffer gets into some kind of weird comptime vs runtime world
    // that I don't undarstand, which causes all sorting functions to SIGSEGV (???)
    var dists = try std.ArrayList(Dist).initCapacity(alloc, points_cap * points_cap);

    var i: usize = 0;
    while (i < points.items.len) : (i += 1) {
        var j: usize = i + 1;
        while (j < points.items.len) : (j += 1) {
            const distance = points.items[i].distance(points.items[j]);
            try dists.appendBounded(.{
                .distance = distance,
                .p1 = &points.items[i],
                .p2 = &points.items[j],
            });
        }
    }

    std.mem.sort(Dist, dists.items, {}, Dist.lessThan);

    // join circuits of closest points
    var part1: u64 = 0;
    var part2: u64 = 0;
    var repeats: usize = 0;
    while (true) : (repeats += 1) {
        if (repeats == connections) {
            part1 = try collect_part1(points.items);
        }

        const dist = &dists.items[repeats];
        const circuit1 = dist.p1.circuit_num;
        const circuit2 = dist.p2.circuit_num;

        var all_connected = true;
        i = 0;
        while (i < points.items.len) : (i += 1) {
            var point = &points.items[i];
            if (point.circuit_num == circuit2) {
                point.circuit_num = circuit1;
            } else if (point.circuit_num != circuit1) {
                all_connected = false;
            }
        }

        if (all_connected) {
            part2 = dist.p1.x * dist.p2.x;
            break;
        }
    }

    return .{
        .part1 = part1,
        .part2 = part2,
    };
}

fn collect_part1(points: []Point) !u64 {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var q = std.PriorityQueue(usize, void, cmp_usize).init(allocator, {});
    defer q.deinit();
    var circuit: usize = 0;
    while (circuit < points.len) : (circuit += 1) {
        var acc: usize = 0;
        var i: usize = 0;
        while (i < points.len) : (i += 1) {
            if (points[i].circuit_num == circuit) {
                acc += 1;
            }
        }
        if (acc != 0) {
            try q.add(acc);
        }
    }

    var acc: u64 = 1;
    var repeats: usize = 0;
    while (repeats < 3) : (repeats += 1) {
        acc *= q.remove();
    }

    return acc;
}

fn cmp_usize(_: void, a: usize, b: usize) std.math.Order {
    if (a < b) {
        return .gt;
    } else if (a > b) {
        return .lt;
    } else {
        return .eq;
    }
}

test "sample" {
    const sample =
        \\162,817,812
        \\57,618,57
        \\906,360,560
        \\592,479,940
        \\352,342,300
        \\466,668,158
        \\542,29,236
        \\431,825,988
        \\739,650,466
        \\52,470,668
        \\216,146,977
        \\819,987,18
        \\117,168,530
        \\805,96,715
        \\346,949,466
        \\970,615,88
        \\941,993,340
        \\862,61,35
        \\984,92,344
        \\425,690,689
        \\
    ;
    var reader = std.io.Reader.fixed(sample);
    const result = try processBuf(&reader, 10);
    try std.testing.expectEqual(40, result.part1);
    try std.testing.expectEqual(25272, result.part2);
}

const Point = struct {
    x: usize,
    y: usize,
    z: usize,

    circuit_num: usize,

    fn distance(self: Point, other: Point) f64 {
        const dx = if (self.x > other.x) self.x - other.x else other.x - self.x;
        const dy = if (self.y > other.y) self.y - other.y else other.y - self.y;
        const dz = if (self.z > other.z) self.z - other.z else other.z - self.z;
        const sum_of_squares: f64 = @floatFromInt(dx * dx + dy * dy + dz * dz);
        return std.math.sqrt(sum_of_squares);
    }
};

const Dist = struct {
    p1: *Point,
    p2: *Point,
    distance: f64,

    fn lessThan(_: void, lhs: Dist, rhs: Dist) bool {
        return lhs.distance < rhs.distance;
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
