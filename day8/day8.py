import math

from collections import deque
from heapq import heappush, heappop

with open('input8.txt', 'r') as f:
    lines = [p.split(',') for p in f.read().splitlines()]
    points = [[int(x) for x in row] for row in lines]


def calc_pairwise_distances(points):
    n = len(points)
    dist = [[0.0] * n for _ in range(n)]

    for i in range(n):
        x1, y1, z1 = points[i]
        for j in range(i + 1, n):
            x2, y2, z2 = points[j]
            d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
            dist[i][j] = d
            dist[j][i] = d
    return dist


def get_n_nearest_neighbors(n_pairs):
    distances = calc_pairwise_distances(points)

    h, seen = [], set()
    for r, row in enumerate(distances):
        for c, dist in enumerate(row):
            if seen & {(r, c), (c, r)}:
                continue
            seen |= {(r, c), (c, r)}
            if dist:
                heappush(h, (dist, (r, c)))

    nearest_neighbors = []
    for _ in range(n_pairs or len(h)):
        nearest_neighbors.append(heappop(h))
    return nearest_neighbors


def star1(n_pairs=None, n_largest=None):
    nearest_neighbors = get_n_nearest_neighbors(n_pairs)

    connections = {}
    for nn in nearest_neighbors:
        _, (x, y) = nn
        if not connections.get(x):
            connections[x] = set()
        if not connections.get(y):
            connections[y] = set()

        connections[x] |= {x, y}
        connections[y] |= {x, y}

    circuits = {}
    while connections:
        _id, pts = connections.popitem()
        circuits[_id] = set()

        q, seen = deque(list(pts)), set()
        while q:
            p = q.popleft()
            if p in seen:
                continue
            seen.add(p)
            if connections.get(p):
                circuits[_id] |= connections[p]
                q.extend(list(connections.pop(p)))

    top_n = sorted(circuits.items(), key=lambda item: len(item[1]), reverse=True)[:n_largest]
    ans = 1
    for k, v in top_n:
        ans *= len(v)

    return ans


def star2():
    parent = list(range(len(points)))
    size = [1] * len(points)

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    def union(a, b):
        root_a = find(a)
        root_b = find(b)

        if root_a == root_b:
            return False

        if size[root_a] < size[root_b]:
            root_a, root_b = root_b, root_a

        parent[root_b] = root_a
        size[root_a] += size[root_b]
        return True

    nearest_neighbors = get_n_nearest_neighbors(None)
    last_connection = None
    unions_done = 0
    max_unions = len(nearest_neighbors)

    while nearest_neighbors and unions_done < max_unions:
        dist, (u, v) = nearest_neighbors.pop(0)
        if union(u, v):
            last_connection = (dist, (u, v))
            unions_done += 1
            if not unions_done%25000: print(unions_done)

    return points[last_connection[1][0]][0] * points[last_connection[1][1]][0]


if __name__ == "__main__":
    print(f"Answer 1: {star1(n_pairs=1000, n_largest=3)}")
    print(f"Answer 2: {star2()}")
