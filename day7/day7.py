from collections import deque

with open('input7.txt', 'r') as f:
    lines = f.read().splitlines()
    manifold = [[_ for _ in line] for line in lines]
    start, r_end, c_end = None, len(manifold) - 1, {-1, len(manifold[0])}
    for r in range(len(manifold)):
        for c in range(len(manifold[0])):
            if manifold[r][c] == 'S':
                start = (r, c)
                break
        if start:
            break


def star1():
    seen, ans, q = set(), set(), deque([start])
    while q:
        row, col = q.popleft()
        if (row, col) in seen or row == r_end or col in c_end:
            continue
        seen.add((row, col))
        if manifold[row + 1][col] == '.':
            q.append((row + 1, col))
        else:
            ans.add((row, col))
            q.extend([(row + 1, col - 1), (row + 1, col + 1)])

    return len(ans)


def star2():
    manifold = [[0 if ch == '.' else 1 if ch == 'S' else ch for ch in line] for line in lines]
    for r, row in enumerate(manifold):
        if not r: continue
        for c, col in enumerate(row):
            if manifold[r][c] != '^':
                manifold[r][c] += manifold[r - 1][c]
            else:
                manifold[r][c - 1] += manifold[r - 1][c]
                manifold[r][c + 1] += manifold[r - 1][c]
                manifold[r][c] = 0
    return sum(manifold[-1])


if __name__ == "__main__":
    ans1 = star1()
    ans2 = star2()
    print(f"Answer 1: {ans1}")
    print(f"Answer 2: {ans2}")
