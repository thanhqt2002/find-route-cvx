from entity import pools, tokens, prices

pools = pools.load_pools("./data/uni.json")
tokens = tokens.load_tokens("./data/tokens.json")
prices = prices.load_prices("./data/prices.json")

print(len(tokens), len(pools), len(prices))

for price in prices:
    print(price.get_preferred_price())
