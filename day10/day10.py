from collections import deque

with open('input10.txt', 'r') as f:
    lines = [p.split() for p in f.read().splitlines()]
    lights = [[_ for _ in line[0][1:-1]] for line in lines]
    joltages = [[int(n) for n in line[-1][1:-1].split(',')] for line in lines]
    buttons = [[tuple(map(int, s.strip("()").split(","))) for s in line[1:-1]] for line in lines]

def resolve_lights(_target, _button_list, star=1):
    q = deque([(['.' for _ in _target], {(-1,):0})])
    history = set()
    seen = set()

    while q:
        curr_state, states = q.popleft()
        if curr_state == _target:
            history.add(tuple([(k,v) for k,v in states.items()]))
            if star==1:
                return sum(states.values())
            continue
        if star==2 and max(states.values())>1:
            continue
        state = (tuple(curr_state), tuple(sorted([(k,v) for k,v in states.items()])))
        if state in seen:
            continue
        seen.add(state)

        for button in _button_list:
            temp_b = curr_state[:]
            temp_states = {k:v for k,v in states.items()}
            for b in button:
                temp_b[b] = '.' if temp_b[b]=='#' else '#'
            temp_states[button] = states.get(button, 0) + 1
            q.append((temp_b, temp_states))

    if star==2:
        return [h[1:] for h in history]
    return None

def star1():
    ans = 0
    for i in range(len(lines)):
        target, button_list = lights[i], buttons[i]
        ans += resolve_lights(target, button_list)
        print(i, ans)
    return ans


def star2():
    from itertools import combinations

    def get_patterns(_button_list, len_jolts):
        coeffs = []
        for button in _button_list:
            v = [0] * len_jolts
            for idx in button:
                v[idx] = 1
            coeffs.append(tuple(v))

        out = {tuple([0] * len_jolts): 0}
        n = len(coeffs)
        for k in range(1, n + 1):
            for subset in combinations(range(n), k):
                s = [0] * len_jolts
                for sub in subset:
                    ci = coeffs[sub]
                    for j in range(len_jolts):
                        s[j] += ci[j]
                s = tuple(s)
                if s not in out or k < out[s]:
                    out[s] = k
        return out

    def resolve_joltage(_joltage, pattern_costs, cache):
        key = tuple(_joltage)
        if key in cache:
            return cache[key]
        if all(j == 0 for j in key):
            cache[key] = 0
            return 0

        _ans = float('inf')
        for pattern, cost in pattern_costs.items():
            valid = True
            for p, k in zip(pattern, key):
                if p > k or (p & 1) != (k & 1):
                    valid = False
                    break
            if not valid:
                continue
            curr_joltage = tuple((j - p) // 2 for p, j in zip(pattern, _joltage))
            _ans = min(_ans, cost + 2 * resolve_joltage(curr_joltage, pattern_costs, cache))
        cache[key] = _ans
        return _ans

    ans = 0
    for i in range(len(lines)):
        joltage, button_list = joltages[i], buttons[i]
        pattern_costs, cache = get_patterns(button_list, len(joltage)), {}
        ans += resolve_joltage(joltage, pattern_costs, cache)
        print(i, ans)
    return ans


if __name__ == "__main__":
    print(f"Answer 1: {star1()}")
    print(f"Answer 2: {star2()}")
