with open('input5.txt', 'r') as f:
    lines = f.read().splitlines()
    fresh = sorted([(int(x), int(y)) for x,y in [l.split('-') for l in lines if '-' in l]])
    avail = sorted([int(l) for l in lines if l and '-' not in l])


def get_ranges():
    ranges = []
    for rng in fresh:
        start, end = rng
        if not ranges:
            ranges.append((start, end))
            continue
        prev_start, prev_end = ranges.pop()
        curr_start, curr_end = (int(start), int(end))
        if prev_start <= curr_start <= curr_end <= prev_end:
            ranges.append((prev_start, prev_end))
        elif prev_start <= curr_start <= prev_end:
            ranges.append((prev_start, curr_end))
        else:
            ranges.extend([(prev_start, prev_end), (curr_start, curr_end)])
    return ranges

def star1():
    ranges, ans = get_ranges(), 0
    rng_st, rng_end = ranges.pop(0)
    av = avail.pop(0)
    while avail:
        if av < rng_st:
            av = avail.pop(0)
        elif rng_st <= av <= rng_end:
            ans += 1
            av = avail.pop(0)
        else:
            if not ranges:
                break
            rng_st, rng_end = ranges.pop(0)

    return ans

def star2():
    ranges = get_ranges()
    ans = len(ranges)
    while ranges:
        s, e = ranges.pop(0)
        ans += e-s
    return ans

if __name__ == "__main__":
    ans1 = star1()
    ans2 = star2()
    print(f"Answer 1: {ans1}")
    print(f"Answer 2: {ans2}")