def pipe_map(*args):
    result = args[-1]
    for mod in args[:-1]:
        result = map(mod, result)
    return list(result)
