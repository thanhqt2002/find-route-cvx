import cvxpy as cp
import numpy as np

usdt_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"
usdc_address = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
token_in = usdt_address
token_out = usdc_address
# 1000 usdc or usdt
amount_in = 1_000_000_000

pool_file_paths = ["./data/uni.json", "./data/balancer-weighted.json"]
token_file_paths = ["./data/tokens.json"]
price_file_paths = ["./data/prices.json"]


def read_data():
    from entity import pools, tokens, prices

    pools = pools.load_pools(*pool_file_paths)
    tokens = tokens.load_tokens(*token_file_paths)
    prices = prices.load_prices(*price_file_paths)

    return pools, tokens, prices


def build_pool_to_token_matrix(n, pools, token_address_to_indices):
    a = []
    for pool in pools:
        n_i = len(pool.tokens)
        a_i = np.zeros((n, n_i))
        for idx, token in enumerate(pool.tokens):
            a_i[token_address_to_indices[token.address]][idx] = 1
        a.append(a_i)
    return a


def main():
    pools, tokens, prices = read_data()

    token_by_address = {token.address: token for token in tokens}
    price_by_address = {price.address: price for price in prices}
    token_address_to_indices = {token_address: idx for (idx, token_address) in enumerate(token_by_address.keys())}
    if token_by_address.keys() != price_by_address.keys():
        raise Exception("token_address must exist in both price and token data")
    # filter out pools that contains a token that we don't have data
    pools = list(filter(lambda pool: all([token.address in token_by_address for token in pool.tokens]), pools))
    # n = number of tokens
    n = len(token_by_address)
    # m = number of pools
    # m = len(pools)

    # a = matrix(m,n,number of tokens of pools i with i=0...m)
    a = build_pool_to_token_matrix(n, pools, token_address_to_indices)

    # give delta to pool
    deltas = [cp.Variable(len(pool.tokens), nonneg=True) for pool in pools]

    # receive lambda
    lambdas = [cp.Variable(len(pool.tokens), nonneg=True) for pool in pools]

    # sum((n, n_i) @ (n_i)) for i=0...m
    psi = cp.sum([a_i @ (l - d) for a_i, d, l in zip(a, deltas, lambdas)])

    token_in_idx = token_address_to_indices[token_in]
    token_out_idx = token_address_to_indices[token_out]
    print(token_in_idx)
    print(token_out_idx)
    # Objective is to maximize "total market value" of coins out

    reserves = [pool.reserves for pool in pools]
    swap_fees = [1 - pool.swap_fee for pool in pools]
    new_reserves = [r + gamma_i * d - l for r, gamma_i, d, l in zip(reserves, swap_fees, deltas, lambdas)]
    cons = [
        psi[token_in_idx] >= -amount_in,
        psi[:token_in_idx] >= 0,
        psi[token_in_idx + 1:] >= 0,
        # psi[token_out_idx] <= 1000,
        # psi >= 0,
    ]
    for idx, pool in enumerate(pools):
        if pool.type == "uni":
            cons.append(cp.geo_mean(new_reserves[idx]) >= cp.geo_mean(reserves[idx]))
        elif pool.type == "balancer-weighted":
            weights = np.array([token.weight for token in pool.tokens])
            normalized_weights = weights / weights.sum()

            def invariant(reserve):
                return cp.geo_mean(reserve, p=normalized_weights)

            cons.append(invariant(new_reserves[idx]) >= invariant(reserves[idx]))
        else:
            raise Exception("unknown pool type")

    obj = cp.Maximize(psi[token_out_idx])

    # Set up and solve problem
    prob = cp.Problem(obj, cons)
    prob.solve(solver='CVXOPT', verbose=True)
    print(f"CONVEX OPTIMISATION SOLVER RESULT: ${prob.value}\n")


if __name__ == '__main__':
    main()
