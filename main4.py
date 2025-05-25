import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
    trials = 100000
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

    # 3) scatter each strategy at those ordinal positions
    fig, ax = plt.subplots(figsize=(10, 6))
    for name, scores in all_results.items():
        freq = Counter(scores)
        # for each actually-seen score, get its position and its count
        xs = [pos_map[s] for s in sorted(freq)]
        ys = [freq[s]           for s in sorted(freq)]
        ax.scatter(xs, ys, s=10, alpha=0.6, label=name)

    # 4) relabel the x–axis ticks back to the real score values
    #    but only every Nth tick, so it doesn’t overlap
    N = len(unique_scores)
    step = max(1, N // 20)                 # show ~20 labels
    tick_positions = list(range(0, N, step))
    tick_labels    = [str(unique_scores[i]) for i in tick_positions]

    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha='right')

    ax.set_xlabel('End-game score (only possible values)')
    ax.set_ylabel('Frequency')
    ax.set_title('Raw Score Frequencies Across Strategies (scatter, no gaps)')
    ax.set_yscale('log')       # optional
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('raw_score_scatter_nogaps.png')
    print("Scatter-plot saved as 'raw_score_scatter_nogaps.png'")
