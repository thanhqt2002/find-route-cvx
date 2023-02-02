from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json
@dataclass
class PoolToken:
    address: str
    weight: int
    swappable: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Pool:
    reserve_usd: float
    amplified_tvl: float
    swap_fee: float
    exchange: str
    type: str
    timestamp: int
    total_supply: str
    static_extra: Optional[str] = field(default_factory=lambda: "")
    reserves: List[float] = field(default_factory=list)
    tokens: List[PoolToken] = field(default_factory=list)


def load_pools(*file_paths):
    pools = []
    for file_path in file_paths:
        with open(file_path) as r:
            pools.extend(Pool.schema().loads(r.read(), many=True))
    return pools

# print(len(load_pools("./data/uni.json", "./data/balancer-weighted.json")))
