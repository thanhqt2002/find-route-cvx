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


def load_tokens(*file_paths):
    tokens = []
    for file_path in file_paths:
        with open(file_path) as r:
            tokens.extend(Token.schema().loads(r.read(), many=True))
    return tokens

# print(len(load_tokens("./data/tokens.json")))
