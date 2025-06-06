const std = @import("std");
const writer = std.io.getStdOut().writer();
const token = "1O9IRMRx4-S5pgtuzhW4kHjXEP6R4s4hmwbGeyKOPxn2WEbqR7Y2T_138Q7LvJC0XxT0D4s38ZfU09HCsc2Gxw";

pub fn main() !void {
    //std.debug.print("Hello, World!\n", .{});

    // todo - working api req using zig; target incident table api as example

    // dynamic allocation
    const alloc = std.heap.page_allocator;
    var arena = std.heap.ArenaAllocator.init(alloc);
    const allocator = arena.allocator();

    defer arena.deinit();

    const prefix = "Basic ".*;
    const tkn_slice = token[0..];
    const encoded_token = try b64_encode(allocator, tkn_slice);
    try writer.print("Attempting to encode token {s}\n", .{tkn_slice});
    var client = std.http.Client{
        .allocator = allocator,
    };

    var auth_header_val = try allocator.alloc(u8, (prefix.len + encoded_token.len));
    auth_header_val = @memmove(u8, auth_header_val[0..6], prefix);
    auth_header_val = @memmove(u8, auth_header_val[6..], encoded_token);

    const headers = &[_]std.http.Header{ .{ .name = "Content-Type", .value = "application/json" }, .{ .name = "Accept", .value = "application/json" }, .{ .name = "Authorization", .value = auth_header_val } };

    // todo - parameterize table and sys_id
    const url = "https://dev188245.service-now.com/api/now/table/incident/a9a16740c61122760004fe9095b7ddca";
    const response = try get(url, headers, &client, alloc);

    // unknown fields (returned from the server; not in our type) cause error. Ignore for simple cases
    const result = try std.json.parseFromSlice(Result, allocator, response.items, .{ .ignore_unknown_fields = true });
    try writer.print("title: {s}\n", .{result.value.short_description});
}

//sys_id, short_description, description, number
const Result = struct { sys_id: [32]u8, short_description: []u8, description: []u8, number: [10]u8 };

fn get(
    url: []const u8,
    headers: []const std.http.Header,
    client: *std.http.Client,
    allocator: std.mem.Allocator,
) !std.ArrayList(u8) {
    try writer.print("\nURL: {s} GET\n", .{url});

    var response_body = std.ArrayList(u8).init(allocator);

    try writer.print("Sending request...\n", .{});
    const response = try client.fetch(.{
        .method = .GET,
        .location = .{ .url = url },
        .extra_headers = headers,
        .response_storage = .{ .dynamic = &response_body },
        // if using POST...
        // .payload = "<some stringified payload>"
    });

    try writer.print("Response status: {d}\nResponse Body: {s}\n", .{ response.status, response_body.items });
    return response_body;
}

fn b64_encode(allocator: std.mem.Allocator, data: []const u8) ![]const u8 {
    const codecs = std.base64.url_safe;
    const bsfe = std.base64.Base64Encoder.init(codecs.alphabet_chars, codecs.pad_char);
    var encoded = try allocator.alloc(u8, bsfe.calcSize(data.len));
    _ = bsfe.encode(encoded, data);
    const result = encoded[0..];
    return result;
}
