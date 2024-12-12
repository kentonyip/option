import numpy as np

def shout_put_price(S0, strike, steps, up_move, down_move, r):
    # Initialize parameters
    N = steps
    c = strike
    S_tree = [[S0]]  # Stock price tree

    # Build stock price tree
    for t in range(1, N + 1):
        prev_prices = S_tree[-1]
        new_prices = [price + up_move for price in prev_prices] + [price - down_move for price in prev_prices]
        S_tree.append(list(sorted(set(new_prices))))  # Sort and remove duplicates
    
    # Risk-neutral probability
    u = S0 + up_move
    d = S0 - down_move
    p = (1 + r - d / S0) / ((u / S0) - (d / S0))
    
    # Initialize the option value tree
    V_tree = [[0] * len(level) for level in S_tree]
    
    # Fill terminal payoff at maturity for put option
    for i, S in enumerate(S_tree[-1]):
        V_tree[-1][i] = max(c - S, 0)
    
    # Backward recursive calculation
    for t in range(N - 1, -1, -1):
        for i, S in enumerate(S_tree[t]):
            # Option value if shouting now
            shout_value = max(c - S, 0)
            
            # Expected value if continuing
            next_prices = S_tree[t + 1]
            up_value = V_tree[t + 1][next_prices.index(S + up_move)] if S + up_move in next_prices else 0
            down_value = V_tree[t + 1][next_prices.index(S - down_move)] if S - down_move in next_prices else 0
            continue_value = p * up_value + (1 - p) * down_value
            
            # Store the max of shout and continue
            V_tree[t][i] = max(shout_value, continue_value)
    
    # Option price at the root
    return V_tree[0][0]

# Parameters
S0 = 100  # Initial stock price
strike = 101  # Strike price
steps = 2  # Number of steps
up_move = 4  # Stock increases by 4
down_move = 6  # Stock decreases by 6
r = 0  # Risk-free rate

# Compute the shout put option price
price = shout_put_price(S0, strike, steps, up_move, down_move, r)
print(f"Shout put option price: {price}")
