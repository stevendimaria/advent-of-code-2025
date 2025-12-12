from collections import deque
from functools import lru_cache

with open('input11.txt', 'r') as f:
    lines = [p.split() for p in f.read().splitlines()]
    vertices, edges = [v[0][:-1] for v in lines], [e[1:] for e in lines]
    graph = {v:e for v,e in zip(vertices, edges)}

def star1(start='you', end='out'):
    ans, q = 0, deque(graph[start])
    while q:
        edge = q.popleft()
        if edge == end:
            ans += 1
        else:
            for e in graph.get(edge, []):
                q.append(e)
    return ans


def star2():
    BIT = {"dac": 1, "fft": 2}
    @lru_cache(None)
    def dp(node, mask):
        if node == "out":
            return 1 if mask == 3 else 0
        total = 0
        for nxt in graph.get(node, ()):
            total += dp(nxt, mask | BIT.get(nxt, 0))
        return total

    return dp("svr", BIT.get("svr", 0))

if __name__ == "__main__":
    print(f"Answer 1: {star1()}")
    print(f"Answer 2: {star2()}")
