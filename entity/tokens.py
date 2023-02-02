from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Token:
    address: str
    symbol: str
    name: str
    decimals: int
    cgk_id: str
    type: str
    poolAddress: str


def load_tokens(file_path):
    with open(file_path) as r:
        return Token.schema().loads(r.read(), many=True)

# print(load_tokens("./data/tokens.json"))
