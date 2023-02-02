from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

PriceSourceKyberswap = "kyberswap"
PriceSourceCoingecko = "coingecko"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Price:
    address: str
    price: float
    liquidity: float
    lp_address: str
    market_price: float
    prefer_price_source: str

    def get_preferred_price(self):
        if self.market_price == 0:
            return self.price
        if self.prefer_price_source == PriceSourceKyberswap:
            return self.price
        elif self.prefer_price_source == PriceSourceCoingecko:
            return self.market_price
        else:
            return self.price


def load_prices(file_path):
    with open(file_path) as r:
        return Price.schema().loads(r.read(), many=True)

# print(load_prices("./data/prices.json"))
