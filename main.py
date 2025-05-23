import random


def find_combinations(numbers, target):
    result = []

    def backtrack(start, path, total):
        if total == target:
            result.append(path[:])
            return
        
        if total > target:
            return
        
        for i in range(start, len(numbers)):
            path.append(numbers[i])
            backtrack(i + 1, path, total + numbers[i])
            path.pop()

    backtrack(0, [], 0)
    return result


def remove_lowest(board, n):
    combos = find_combinations(board, n)
    if not combos:
        return False

    lowest = float("inf")
    i_lowest = 0
    for i, combo in enumerate(combos):
        if min(combo) < lowest:
            lowest = min(combo)
            i_lowest = i
    
    print("Board: ", board)
    print("Combo: ", combos[i_lowest])

    for x in combos[i_lowest]:
        board.remove(x)

    return True

def remove_highest(board, n):
    combos = find_combinations(board, n)
    if not combos:
        return False

    highest = float(0)
    i_highest = 0
    for i, combo in enumerate(combos):
        if max(combo) > highest:
            highest = min(combo)
            i_highest = i
    
    print("Board: ", board)
    print("Combo: ", combos[i_highest])

    for x in combos[i_highest]:
        board.remove(x)

    return True


def remove_random(board, n):
    combos = find_combinations(board, n)
    if not combos:
        return False

    combo = combos[random.randint(0, len(combos) - 1)]
    
    print("Board: ", board)
    print("Combo: ", combo)

    for x in combo:
        board.remove(x)

    return True


def remove_max_total(board, n):
    combos = find_combinations(board, n)
    if not combos:
        return False

    best_combo = max(combos, key=lambda c: sum(c))
    print("Board: ", board)
    print("Combo: ", best_combo)

    for x in best_combo:
        board.remove(x)
    return True


def remove_fewest_numbers(board, n):
    combos = find_combinations(board, n)
    if not combos:
        return False

    best_combo = min(combos, key=lambda c: len(c))
    print("Board: ", board)
    print("Combo: ", best_combo)

    for x in best_combo:
        board.remove(x)
    return True


def get_rand():
    return random.randint(1,6) + random.randint(1,6)


def run(strategy):
    print("New Game")
    board = list(range(1,11))
    
    while True:
        n = get_rand()
        print("\nNumber: ", n)
        if not strategy(board, n):
            break
    
    print("\nOutcome: ", board)
    print("-----------")
    
    return 0 if not board else int("".join(str(d) for d in board))


def simulate(strategy, n):
    avg = 0
    for _ in range(0, n):
        avg += run(strategy)
    return avg / n


n = 30000

lo = simulate(remove_lowest, n)
hi = simulate(remove_highest, n)
rnd = simulate(remove_random, n)
max_total = simulate(remove_max_total, n)
fewest_nums = simulate(remove_fewest_numbers, n)

print("\n\nAvg. score remove lowest:  ", lo)
print("Avg. score remove highest: ", hi)
print("Avg. score remove random:  ", rnd)
print("Avg. score max total:      ", max_total)
print("Avg. score fewest numbers: ", fewest_nums)