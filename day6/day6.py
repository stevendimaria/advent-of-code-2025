with open('input6.txt', 'r') as f:
    lines = f.read().splitlines()
    ops = [l for l in lines.pop().split()]
    probs = {i: [op] for i, op in enumerate(ops)}
    str_probs = {i: [op] for i, op in enumerate(ops)}
    for line in lines:
        for i, l in enumerate(line.split()):
            probs[i].append(int(l))
            str_probs[i].append(l)


def calc(op, nums):
    if op == '+':
        return sum(nums)
    else:
        return (lambda p=1: [p := p * x for x in nums] and p)()


def star1():
    ans = 0
    for _, nums in probs.items():
        ans += calc(nums.pop(0), nums)
    return ans


def star2():
    ans = 0
    rows = []
    for line in lines:
        rows.append([x for x in line])

    op = ops.pop()
    nums, rem = [], len(rows[0])
    while True:
        if rem:
            curr = [row.pop() for row in rows]
            rem -= 1
        else:
            ans += calc(op, nums)
            break

        if set(curr) == {' '}:
            ans += calc(op, nums)
            nums, op = [], ops.pop()
        else:
            nums.append(int(''.join(curr)))
    return ans


if __name__ == "__main__":
    ans1 = star1()
    ans2 = star2()
    print(f"Answer 1: {ans1}")
    print(f"Answer 2: {ans2}")
