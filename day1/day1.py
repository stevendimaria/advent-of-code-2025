with open('input1.txt', 'r') as f:
    data = [(l[0], int(l[1:])) for l in f.read().splitlines()]


def star1():
    ans = 0
    curr = 50
    for d, n in data:
        if d == 'L':
            curr -= n
        else:
            curr += n
        if not curr % 100:
            ans += 1
    return ans


def star2():
    ans = 0
    curr, prev = 50, (100, "")
    for d, n in data:
        if d == 'L':
            curr -= n
        else:
            curr += n

        tens, ones = divmod(curr, 100)
        if tens:
            ans += abs(tens)
        if prev[0] == 0 and prev[1] != d:
            if prev[1] == 'L':
                ans += 1
            else:
                ans -= 1
        prev = (ones, d)
        curr = ones
    return ans


if __name__ == "__main__":
    ans1 = star1()
    ans2 = star2()
    print(f"Answer 1: {ans1}")
    print(f"Answer 2: {ans2}")
