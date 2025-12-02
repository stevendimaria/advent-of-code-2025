with open('input2.txt', 'r') as f:
    temp = f.read().split(',')
    data = []
    for d in temp:
        _start, _end = d.split('-')
        data.append((int(_start.strip()), int(_end.strip())))


def star1():
    ans = 0
    for start, end in data:
        for n in range(start, end+1):
            s = str(n)
            if s[:len(s)//2] == s[len(s)//2:]:
                ans += int(s)
    return ans

def star2():
    def is_repeating(s):
        return s in (s + s)[1:-1]

    ans = 0
    for start, end in data:
        for n in range(start, end+1):
            if is_repeating(str(n)):
                ans += int(n)
    return ans



if __name__ == "__main__":
    ans1 = star1()
    ans2 = star2()
    print(f"Answer 1: {ans1}")
    print(f"Answer 2: {ans2}")