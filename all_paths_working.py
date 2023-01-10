graph = {
    (1, 0, 2): [(1, 0, 3)],
    (1, 0, 3): [(1, 0, 4), (3, 0, 3)],
    (1, 0, 4): [(2, 0, 1), (3, 0, 5)],
    (2, 0, 1): [(1, 0, 2), (3, 0, 3), (5, 0, 1)],
    (3, 0, 3): [(2, 0, 1), (1, 0, 3), (3, 0, 5), (5, 0, 5)],
    (3, 0, 5): [(3, 0, 3), (5, 0, 5)],
    (5, 0, 1): [(2, 0, 1), (3, 0, 3), (6, 0, 2)],
    (5, 0, 5): [(3, 0, 3), (6, 0, 4)],
    (6, 0, 2): [(5, 0, 1), (6, 0, 4)],
    (6, 0, 4): [(5, 0, 5), (6, 0, 2)],
}

def find_paths(start, end):
    visited = {}
    for k in graph.keys():
        visited[k] = False

    return find(start, end, visited, [], [])


def find(current, end, visited, current_path, paths):
    visited[current] = True
    current_path.append(current)

    if (current == end):
        paths.append(current_path.copy())
    else:
        for i in graph[current]:
            if (visited[i] == False):
                paths = find(i, end, visited, current_path, paths)

    current_path.pop()
    visited[current] = False

    return paths

paths = find_paths((1, 0, 3), (5, 0, 5))
for elt in paths:
    print(elt)