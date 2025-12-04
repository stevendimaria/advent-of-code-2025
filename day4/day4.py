def make_data() -> list:
    with open('input4.txt', 'r') as f:
        lines = f.read().splitlines()
        data = [[_ for _ in l] for l in lines]
    return data

def star1(data=None, rem=False):
    if not data:
        data = make_data()
    L = len(data)
    W = len(data[0])

    def get_surrounding(_r, _c):

        surrounding = [
            (_r - 1, _c - 1), (_r - 1, _c), (_r - 1, _c + 1),
            (_r, _c - 1),                 (_r, _c + 1),
            (_r + 1, _c - 1), (_r + 1, _c), (_r + 1, _c + 1),
        ]
        return [
            (i, j) for (i, j) in surrounding
            if 0 <= i < L and 0 <= j < W
        ]

    ans = 0
    for r in range(L):
        for c in range(W):
            if data[r][c] != '@':
                continue
            surrounding = get_surrounding(r,c)
            rolls = 0
            for x,y in surrounding:
                if data[x][y] == '@':
                    rolls += 1
            if rolls<4:
                ans += 1
                if rem:
                    data[r][c] = '.'
    return ans
def star2():
    ans = 0
    data = make_data()
    while True:
        to_rem = star1(data, True)
        if not to_rem:
            return ans
        ans += to_rem


if __name__ == "__main__":
    ans1 = star1()
    ans2 = star2()
    print(f"Answer 1: {ans1}")
    print(f"Answer 2: {ans2}")