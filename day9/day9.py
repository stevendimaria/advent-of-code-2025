with open('input9.txt', 'r') as f:
    lines = [p.split(',') for p in f.read().splitlines()]
    points = [tuple(int(x) for x in row) for row in lines]

    xs, ys = set(), set()
    comps = {'x': {}, 'y': {}}
    lo_x, lo_y = 0, 0
    for x, y in points:
        xs.add(x)
        ys.add(y)

    x_map, y_map = {}, {}
    for i, x in enumerate(sorted(xs)):
        x_map[i] = x
        x_map[x] = i
        lo_x = max(i, lo_x)
    for j, y in enumerate(sorted(ys)):
        y_map[j] = y
        y_map[y] = j
        lo_y = max(j, lo_y)

    pts = []
    for x, y in sorted(points):
        _x, _y = x_map[x], y_map[y]
        pts.append((_x, _y))
        if not comps['x'].get(_x):
            comps['x'][_x] = [_y]
        else:
            comps['x'][_x] = sorted(comps['x'][_x] + [_y])
        if not comps['y'].get(_y):
            comps['y'][_y] = [_x]
        else:
            comps['y'][_y] = sorted(comps['y'][_y] + [_x])

def star1():
    ans = 0
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            (x1, y1), (x2, y2) = points[i], points[j]
            ans = max(ans, (abs(x1-x2)+1) * (abs(y1-y2)+1))
    return ans


def star2():
    def check_border(x1, x2, y1, y2):
        return (
                all(inside[x1][y] == '#' for y in range(y1, y2 + 1)) and
                all(inside[x2][y] == '#' for y in range(y1, y2 + 1)) and
                all(inside[x][y1] == '#' for x in range(x1, x2 + 1)) and
                all(inside[x][y2] == '#' for x in range(x1, x2 + 1))
        )

    inside = [['.' for c in range(lo_y+1)] for r in range(lo_x+1)]

    for k,v in comps['x'].items():
        inside[k][v[0]:v[1]+1] = ['#'] * ((v[1]-v[0])+1)
    for k,v in comps['y'].items():
        for _x in range(v[0], v[1]+1):
            inside[_x][k] = '#'

    hull = []
    for i in range(len(inside)):
        for j in range(len(inside[i])):
            if inside[i][j] == '#':
                hull.append((i,j))

    while hull:
        (x1, y1), (x2, y2) = hull.pop(0), hull.pop(0)
        if x1!=x2:
            hull = [(x2,y2)]+hull
            continue
        connected = y2-y1 == 1
        while hull and hull[0][0]==x1 and hull[0][1]-1==y2:
            (x2, y2) = hull.pop(0)
            connected = True
        for y in range(y1, y2+1):
            inside[x1][y] = '#'
        if hull and connected:
            for i in range(0, x2):
                if inside[i][y2] == '#':
                    for j in range(x2+1, lo_x+1):
                        if inside[j][y2] == '#':
                            hull = [(x2, y2)] + hull
                            break
                if hull[0] == (x2, y2):
                    break

    ans = 0
    for x1, y1 in pts:
        for x2, y2 in pts[x1+1:]:
            score = (abs(x_map[x1] - x_map[x2]) + 1) * (abs(y_map[y1] - y_map[y2]) + 1)
            if score < ans:
                continue
            _x1, _x2 = min(x1, x2), max(x1, x2)
            _y1, _y2 = min(y1, y2), max(y1, y2)
            if check_border(_x1, _x2, _y1, _y2):
                ans = max(ans, score)
    return ans


if __name__ == "__main__":
    print(f"Answer 1: {star1()}")
    print(f"Answer 2: {star2()}")
