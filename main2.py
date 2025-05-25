import random
import matplotlib
# use a non-interactive backend so we can save to file without needing a display
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
    if not combos: return False
    lowest, idx = float('inf'), 0
    for i, combo in enumerate(combos):
        if min(combo) < lowest:
            lowest, idx = min(combo), i
    for x in combos[idx]:
        board.remove(x)
    return True

def remove_highest(board, n):
    combos = find_combinations(board, n)
    if not combos: return False
    highest, idx = -float('inf'), 0
    for i, combo in enumerate(combos):
        if max(combo) > highest:
            highest, idx = max(combo), i
    for x in combos[idx]:
        board.remove(x)
    return True

def remove_random(board, n):
    combos = find_combinations(board, n)
    if not combos: return False
    combo = random.choice(combos)
    for x in combo:
        board.remove(x)
    return True

def remove_max_total(board, n):
    combos = find_combinations(board, n)
    if not combos: return False
    best = max(combos, key=sum)
    for x in best:
        board.remove(x)
    return True

def remove_fewest_numbers(board, n):
    combos = find_combinations(board, n)
    if not combos: return False
    best = min(combos, key=len)
    for x in best:
        board.remove(x)
    return True

def get_rand():
    return random.randint(1,6) + random.randint(1,6)

def run(strategy):
    board = list(range(1, 11))
    while strategy(board, get_rand()):
        pass
    # return 0 if board empty else concatenated remaining digits
    return 0 if not board else int(''.join(str(d) for d in board))

def simulate_all(strategy, trials):
    return [run(strategy) for _ in range(trials)]


if __name__ == '__main__':
    trials = 1000000
    strategies = {
        'remove_lowest':      remove_lowest,
        'remove_highest':     remove_highest,
        'remove_random':      remove_random,
        'remove_max_total':   remove_max_total,
        'remove_fewest_nums': remove_fewest_numbers
    }

    # simulate and compute means
    all_results = {}
    for name, strat in strategies.items():
        scores = simulate_all(strat, trials)
        all_results[name] = scores
        mean_score = sum(scores) / trials
        print(f'Avg. score {name:17s}: {mean_score:.3f}')

    # Plot distributions
    fig, axes = plt.subplots(len(all_results), 1, figsize=(8, 12))
    for ax, (name, scores) in zip(axes, all_results.items()):
        max_score = max(scores)
        ax.hist(scores, bins=100, range=(0, max_score), edgecolor='black')
        ax.set_title(f'Distribution of end-game scores: {name}')
        ax.set_xlabel('Score')
        ax.set_ylabel('Frequency')
        ax.set_xlim(0, max_score)
        ax.set_yscale('log')

    plt.tight_layout()
    plt.savefig('score_distributions_linear.png')
    print("\nHistogram saved as 'score_distributions_linear.png'")
