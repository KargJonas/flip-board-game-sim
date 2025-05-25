import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

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
    return 0 if not board else int(''.join(str(d) for d in board))

def simulate(strategy, trials):
    return [run(strategy) for _ in range(trials)]

if __name__ == '__main__':
    trials = 1_000_000
    strategies = {
        'remove_lowest':      remove_lowest,
        'remove_highest':     remove_highest,
        'remove_random':      remove_random,
        'remove_max_total':   remove_max_total,
        'remove_fewest_nums': remove_fewest_numbers
    }

    # simulate and print means
    all_results = {}
    for name, strat in strategies.items():
        scores = simulate(strat, trials)
        all_results[name] = scores
        print(f'Avg. score {name:17s}: {sum(scores)/trials:.3f}')

    # 1) collect & sort ALL unique scores across strategies
    all_scores = set()
    for scores in all_results.values():
        all_scores |= set(scores)
    unique_scores = sorted(all_scores)

    # 2) create a mapping score -> ordinal position
    pos_map = {score: idx for idx, score in enumerate(unique_scores)}
    N = len(unique_scores)

    # 3) plot side-by-side bar histograms
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 3) make one subplot per strategy
    num_strat = len(all_results)
    fig, axes = plt.subplots(num_strat, 1, sharex=True, figsize=(12, 3*num_strat))

    # compute tick positions & labels once
    step = max(1, N // 20)
    tick_positions = list(range(0, N, step))
    tick_labels    = [str(unique_scores[i]) for i in tick_positions]

    for ax, (name, scores) in zip(axes, all_results.items()):
        freq = Counter(scores)
        sorted_scores = sorted(freq)

        # x positions come from the global pos_map
        xs = [pos_map[s] for s in sorted_scores]
        ys = [freq[s]      for s in sorted_scores]

        ax.bar(xs, ys, width=1.0, alpha=0.7)
        ax.set_yscale('log')                     # keep log scale if desired
        ax.set_ylabel('Freq')
        ax.set_title(name, loc='left')
        ax.grid(True, linestyle='--', alpha=0.3)

    # label the shared x-axis on the bottom plot only
    axes[-1].set_xticks(tick_positions)
    axes[-1].set_xticklabels(tick_labels, rotation=45, ha='right')
    axes[-1].set_xlabel('End-game score (only possible values)')

    plt.tight_layout()
    plt.savefig('score_distributions_subplots_2.png')
    print("Subplot-histograms saved as 'score_distributions_subplots.png'")