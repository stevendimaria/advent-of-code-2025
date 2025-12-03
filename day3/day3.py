with open('input3.txt', 'r') as f:
    data = f.read().splitlines()


def star1():
    ans = 0
    for line in data:
        tens, ones = (0, 0), (0, 0)
        for i, joltage in enumerate(line):
            joltage = int(joltage)
            if joltage == 9:
                tens = (joltage, i)
                break
            if joltage > tens[0]:
                tens = (joltage, i)
        if tens[1] == len(line) - 1:
            ones = (tens[0], tens[1])
            tens = (0, 0)
            for i in range(len(line) - 1):
                tens = max(tens, (int(line[i]), i))
        else:
            for i in range(tens[1] + 1, len(line)):
                ones = max(ones, (int(line[i]), i))
        ans += (tens[0] * 10) + ones[0]
    return ans


def star2(n=12):
    ans = 0
    for line in data:
        rem = len(line) - n
        stack = []

        for ch in line:
            while rem and stack and stack[-1] < ch:
                stack.pop()
                rem -= 1
            stack.append(ch)

        ans += int(''.join(stack[:n]))
    return ans


if __name__ == "__main__":
    ans1 = star1()  # alternatively, star2(n=2)
    ans2 = star2()
    print(f"Answer 1: {ans1}")
    print(f"Answer 2: {ans2}")
