from entity import pools, tokens, prices

pools = pools.load_pools("./data/uni.json", "./data/balancer-weighted.json")
tokens = tokens.load_tokens("./data/tokens.json")
prices = prices.load_prices("./data/prices.json")

# Clean up data

token_by_address = {token.address: token for token in tokens}
price_by_address = {price.address: price for price in prices}

if token_by_address.keys() != price_by_address.keys():
    raise Exception("token_address must exist in both price and token data")

# filter out pools that contains a token that we don't have data
pools = list(filter(lambda pool: all([(token.address in token_by_address) for token in pool.tokens]), pools))

# n = number of tokens
n = len(token_by_address)
# m = number of pools
m = len(pools)
