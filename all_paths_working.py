graph = {
    1: [2, 6],
    2: [1, 3, 4, 6],
    3: [6],
    4: [2, 5],
    5: [7],
    6: [2, 3, 7],
    7: [3]
}

paths = []

def find_paths(start, end, graphe):
    paths.clear()

    visited = {}
    for k in graphe.keys():
        visited[k] = False

    find(start, end, graphe, visited, [])


def find(current, end, graphe, visited, current_path):
    visited[current] = True
    current_path.append(current)

    print(current_path)

    if (current == end):
        paths.append(current_path.copy())
    else:
        for i in graphe[current]:
            if (visited[i] == False):
                find(i, end, graphe, visited, current_path)

    current_path.pop()
    visited[current] = False

find_paths(1, 3, graph)
print(paths)
