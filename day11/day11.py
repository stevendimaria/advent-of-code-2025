from collections import deque

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
            q.extend(graph.get(edge, []))
    return ans

def star2():
    ans, q = 0, deque([[v, {'svr'}] for v in graph['svr']])
    while q:
        edge, seen = q.popleft()
        if edge == 'out':
            ans += {'dac', 'fft'} & seen
            print(f"Current Answer: {ans}")
        else:
            for e in graph[edge]:
                if e in seen:
                    continue
                q.append([e, seen|{e}])
    return ans


if __name__ == "__main__":
    print(f"Answer 1: {star1()}")
    print(f"'dac' -> 'out': {star1('dac')}")
    # print(f"'fft' -> 'out': {star1('fft')}")
    print(f"'dac' -> 'fft': {star1('dac', 'fft')}")
    # print(f"'fft' -> 'dac': {star1('fft', 'dac')}")
    # print(f"'svr' -> 'dac': {star1('svr', 'dac')}")
    print(f"'svr' -> 'fft': {star1('svr', 'fft')}")
    # print(f"Answer 2: {star2()}")
