from math import sqrt


with open('/Users/stevendimaria/Desktop/Work/AoC/AoC25/advent-of-code-2025/day12/input12.txt', 'r') as f:
    lines = [p.split() for p in f.read().splitlines()][30:]
    spaces = [(int(a), int(b)) for l in lines for a, b in [l[0][:-1].split('x')]]
    presents = [[int(p) for p in pr[1:]] for pr in lines]


def parse_shape(rows):
    pts = {(y, x) for y, r in enumerate(rows) for x, c in enumerate(r) if c == '#'}
    return normalize(pts)

def normalize(pts):
    miny = min(y for y, x in pts)
    minx = min(x for y, x in pts)
    return {(y - miny, x - minx) for y, x in pts}

def rotate90(pts):
    maxy = max(y for y, x in pts)
    return {(x, maxy - y) for y, x in pts}

def flip_h(pts):
    maxx = max(x for y, x in pts)
    return {(y, maxx - x) for y, x in pts}

def orientations(pts, allow_flip=True):
    seen = set()
    out = []
    variants = [pts] + ([flip_h(pts)] if allow_flip else [])
    for base in variants:
        cur = base
        for _ in range(4):
            cur = normalize(cur)
            key = tuple(sorted(cur))
            if key not in seen:
                seen.add(key)
                out.append(cur)
            cur = rotate90(cur)
    return out

def pts_to_rowmasks(pts):
    h = max(y for y, x in pts) + 1
    w = max(x for y, x in pts) + 1
    rows = [0] * h
    for y, x in pts:
        rows[y] |= (1 << x)
    return tuple(rows), h, w

def find_packing(N, M, shape_orients):
    board = [0] * N
    placements = {}
    for sid, orients in shape_orients.items():
        ps = []
        for oi, (rows, h, w) in enumerate(orients):
            if h > N or w > M:
                continue
            for y in range(N - h + 1):
                for x in range(M - w + 1):
                    shifted = tuple(r << x for r in rows)
                    ps.append((shifted, y, x, oi))
        if not ps:
            return None
        placements[sid] = ps

    order = sorted(placements.keys(), key=lambda s: len(placements[s]))
    chosen = {}

    def can_place(shifted, y):
        for dy, rowbits in enumerate(shifted):
            if board[y + dy] & rowbits:
                return False
        return True

    def do_place(shifted, y):
        for dy, rowbits in enumerate(shifted):
            board[y + dy] |= rowbits

    def undo_place(shifted, y):
        for dy, rowbits in enumerate(shifted):
            board[y + dy] ^= rowbits

    def backtrack(i=0):
        if i == len(order):
            return True
        sid = order[i]
        for shifted, y, x, oi in placements[sid]:
            if can_place(shifted, y):
                do_place(shifted, y)
                chosen[sid] = (y, x, oi)
                if backtrack(i + 1):
                    return True
                undo_place(shifted, y)
                del chosen[sid]
        return False

    return chosen if backtrack() else None

def render(N, M, chosen, shape_orients):
    grid = [["." for _ in range(M)] for _ in range(N)]
    for sid, (y0, x0, oi) in chosen.items():
        rows, h, w = shape_orients[sid][oi]
        for dy in range(h):
            bits = rows[dy]
            for dx in range(w):
                if (bits >> dx) & 1:
                    grid[y0 + dy][x0 + dx] = str(sid)
    return "\n\t".join("\t".join(r) for r in grid)

def smallest_rect_with_layout(shapes_by_id, allow_flip=True, prefer_square=True):
    shape_orients = {}
    total_cells = 0
    for sid, rows in shapes_by_id.items():
        pts = parse_shape(rows)
        total_cells += len(pts)
        shape_orients[sid] = [pts_to_rowmasks(o) for o in orientations(pts, allow_flip=allow_flip)]

    for area in range(total_cells, total_cells + 5000):
        candidates = []
        for N in range(1, int(sqrt(area)) + 1):
            if area % N == 0:
                M = area // N
                candidates.append((N, M))
                candidates.append((M, N))
        if prefer_square:
            candidates = sorted(set(candidates), key=lambda nm: (max(nm), abs(nm[0] - nm[1])))
        else:
            candidates = sorted(set(candidates))

        for N, M in candidates:
            sol = find_packing(N, M, shape_orients)
            if sol:
                return N, M, render(N, M, sol, shape_orients)

    return None

shapes = {
    0: ["..#", ".##", "##."],
    1: [".##", "##.", "###"],
    2: ["#.#", "###", "#.#"],
    3: ["###", "#.#", "#.#"],
    4: ["###", ".##", "..#"],
    5: ["#..", "###", "###"]
}

"""     
0:     1:     2:     3:     4:     5:  
..#    .##    #.#    ###    ###    #.. 
.##    ##.    ###    #.#    .##    ### 
##.    ###    #.#    #.#    ..#    ### 

Optimal Shapes
==============
[0,1,2,3,4,5] (5x9)
222..
.2333
222.3
55333
55444
55544
11004
11100
1.1.0
"""
def star1():
    ans = 0
    ct = 1
    for space, present in zip(spaces, presents):
        print(f"Case {ct}\t\t\tSpace: {space}\tPresent:{present}")
        ct += 1
        if max((max(space)//9) * (min(space)//5), (max(space)//5) * (min(space)//9)) >= max(present):
            ans +=1
            continue
        space = [max(space), min(space)]
        found = False
        while max(space)>9 and min(space)>5:
            if (space[0]-9)*(space[1]-5) > (space[0]-5)*(space[1]-9):
                curr = (space[0]//9)
                space[1] -= 5
            else:
                curr = (space[0]//5)
                space[1] -= 9
            for i in range(len(present)):
                present[i] = max(0, present[i]-curr)
            if sum(present)*3 < max(space):
                if min(space)>=3:
                    ans +=1
                    found = True
                    break

        if not found:
            if sum(present) * 3 < max(space) and min(space) >= 3:
                ans += 1
            elif (sum(present)*9)-(space[0]*space[1]) <= 200:
                ans += 1
            else:
                print('\t', space, present, (sum(present)*9)-(space[0]*space[1]))

    return ans


if __name__ == "__main__":
    print(f"Answer 1: {star1()}")

    # for i in range(6):
    #     for j in range(6):
    #         if i > j:
    #             continue
    #         _shapes = {'#': shapes[i], 'X': shapes[j]}
    #
    #         N, M, layout = smallest_rect_with_layout(_shapes, allow_flip=True, prefer_square=True)
    #         print(f"\nShapes: [{i}, {j}]\n\tSmallest rectangle found: {N} x {M} (area {N * M})")
    #         print(f"\t{layout}")
    #
    #         for k in range(6):
    #             if j > k:
    #                 continue
    #             _shapes = {'#': shapes[i], 'X': shapes[j], 'O': shapes[k]}
    #
    #             N, M, layout = smallest_rect_with_layout(_shapes, allow_flip=True, prefer_square=True)
    #             print(f"\nShapes: [{i}, {j}, {k}]\n\tSmallest rectangle found: {N} x {M} (area {N * M})")
    #             print(f"\t{layout}")
    #
    #             for m in range(6):
    #                 if k > m:
    #                     continue
    #                 _shapes = {'#': shapes[i], 'X': shapes[j], 'O': shapes[k], '@': shapes[m]}
    #
    #                 N, M, layout = smallest_rect_with_layout(_shapes, allow_flip=True, prefer_square=True)
    #                 print(f"\nShapes: [{i}, {j}, {k}, {m}]\n\tSmallest rectangle found: {N} x {M} (area {N * M})")
    #                 print(f"\t{layout}")
    #
    #                 for n in range(6):
    #                     if m > n:
    #                         continue
    #                     _shapes = {'#': shapes[i], 'X': shapes[j], 'O': shapes[k], '@': shapes[m], '$': shapes[n]}
    #
    #                     N, M, layout = smallest_rect_with_layout(_shapes, allow_flip=True, prefer_square=True)
    #                     print(f"\nShapes: [{i}, {j}, {k}, {m}, {n}]\n\tSmallest rectangle found: {N} x {M} (area {N * M})")
    #                     print(f"\t{layout}")
