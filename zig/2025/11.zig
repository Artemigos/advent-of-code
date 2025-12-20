const std = @import("std");
const utils = @import("utils.zig");

pub fn main() !void {
    const file = try utils.io.readFileFromArg();
    defer file.close();
    var buf: [4096]u8 = undefined;
    var reader = file.reader(&buf);
    const result = try processBuf(&reader.interface, true, true);
    try utils.io.printStdOutUnsafe("{f}", .{result});
}

const Node = struct {
    name: []const u8,
    targets: std.ArrayList(*Node),

    fn init(alloc: std.mem.Allocator, name: []const u8) !Node {
        const targets = try std.ArrayList(*Node).initCapacity(alloc, 5);
        return .{
            .name = try alloc.dupe(u8, name),
            .targets = targets,
        };
    }

    fn deinit(self: *Node, alloc: std.mem.Allocator) void {
        alloc.free(self.name);
        self.targets.deinit(alloc);
    }
};

fn processBuf(reader: *std.io.Reader, calc_part_1: bool, calc_part_2: bool) !utils.Result {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();

    var part1: u64 = 0;
    var part2: u64 = 0;

    var nodes = std.StringHashMap(Node).init(alloc);
    defer {
        var iter = nodes.iterator();
        while (iter.next()) |node| {
            alloc.free(node.key_ptr.*);
            node.value_ptr.deinit(alloc);
        }
        nodes.deinit();
    }

    var connections = try std.ArrayList(struct { []u8, []u8 }).initCapacity(alloc, 10);
    defer {
        for (connections.items) |item| {
            alloc.free(item.@"1");
        }
        connections.deinit(alloc);
    }

    while (try reader.takeDelimiter('\n')) |line| {
        const colon_i = std.mem.indexOfScalar(u8, line, ':').?;
        const name = try alloc.dupe(u8, line[0..colon_i]);
        const node = try Node.init(alloc, name);
        var rest = line[colon_i + 2 ..];
        while (true) {
            const next = try alloc.dupe(u8, std.mem.sliceTo(rest, ' '));
            try connections.append(alloc, .{ name, next });
            if (next.len == rest.len) {
                break;
            } else rest = rest[next.len + 1 ..];
        }
        try nodes.put(name, node);
    }

    const out_name = try alloc.dupe(u8, "out");
    const out_node = try Node.init(alloc, out_name);
    try nodes.put(out_name, out_node);

    for (connections.items) |conn| {
        var left = nodes.getEntry(conn.@"0").?;
        const right = nodes.getEntry(conn.@"1").?;

        try left.value_ptr.targets.append(alloc, right.value_ptr);
    }

    if (calc_part_1) {
        var you = nodes.get("you").?;
        part1 = pathsToOut(nodes, &you);
    }

    if (calc_part_2) {
        var svr = nodes.get("svr").?;
        var memo = Memoized.init(alloc);
        defer memo.deinit();
        part2 = (try memo.call(nodes, &svr)).paths_both;
    }

    return .{
        .part1 = part1,
        .part2 = part2,
    };
}

fn pathsToOut(map: std.StringHashMap(Node), start: *Node) usize {
    const out = map.getEntry("out").?.value_ptr;

    var acc: usize = 0;
    for (start.targets.items) |target| {
        if (target == out) {
            acc += 1;
        } else {
            acc += pathsToOut(map, target);
        }
    }

    return acc;
}

const TrackingResult = struct {
    paths_no_dac_or_fft: usize = 0,
    paths_dac_only: usize = 0,
    paths_fft_only: usize = 0,
    paths_both: usize = 0,
};

const Memoized = struct {
    const Self = @This();
    const Cache = std.AutoHashMap(*Node, TrackingResult);

    cache: Cache,

    fn init(alloc: std.mem.Allocator) Self {
        return .{
            .cache = Cache.init(alloc),
        };
    }

    fn deinit(self: *Self) void {
        self.cache.deinit();
    }

    fn call(self: *Self, map: std.StringHashMap(Node), start: *Node) error{OutOfMemory}!TrackingResult {
        if (self.cache.get(start)) |result| {
            return result;
        }

        const result = try self.pathsToOutWithTracking(map, start);
        try self.cache.put(start, result);
        return result;
    }

    fn pathsToOutWithTracking(self: *Self, map: std.StringHashMap(Node), start: *Node) !TrackingResult {
        const out = map.getEntry("out").?.value_ptr;
        const dac = map.getEntry("dac").?.value_ptr;
        const fft = map.getEntry("fft").?.value_ptr;

        var acc = TrackingResult{};
        if (start == out) {
            acc.paths_no_dac_or_fft = 1;
        } else {
            for (start.targets.items) |target| {
                const inner = try self.call(map, target);
                acc.paths_both += inner.paths_both;
                if (start == dac) {
                    acc.paths_both += inner.paths_fft_only;
                    acc.paths_dac_only += inner.paths_no_dac_or_fft + inner.paths_dac_only;
                } else if (start == fft) {
                    acc.paths_both += inner.paths_dac_only;
                    acc.paths_fft_only += inner.paths_no_dac_or_fft + inner.paths_fft_only;
                } else {
                    acc.paths_dac_only += inner.paths_dac_only;
                    acc.paths_fft_only += inner.paths_fft_only;
                    acc.paths_no_dac_or_fft += inner.paths_no_dac_or_fft;
                }
            }
        }

        return acc;
    }
};

test "sample 1" {
    const sample =
        \\aaa: you hhh
        \\you: bbb ccc
        \\bbb: ddd eee
        \\ccc: ddd eee fff
        \\ddd: ggg
        \\eee: out
        \\fff: out
        \\ggg: out
        \\hhh: ccc fff iii
        \\iii: out
        \\
    ;
    var reader = std.io.Reader.fixed(sample);
    const result = try processBuf(&reader, true, false);
    try std.testing.expectEqual(5, result.part1);
}

test "sample 2" {
    const sample =
        \\svr: aaa bbb
        \\aaa: fft
        \\fft: ccc
        \\bbb: tty
        \\tty: ccc
        \\ccc: ddd eee
        \\ddd: hub
        \\hub: fff
        \\eee: dac
        \\dac: fff
        \\fff: ggg hhh
        \\ggg: out
        \\hhh: out
        \\
    ;
    var reader = std.io.Reader.fixed(sample);
    const result = try processBuf(&reader, false, true);
    try std.testing.expectEqual(2, result.part2);
}
