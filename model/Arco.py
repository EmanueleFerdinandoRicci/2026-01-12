from dataclasses import dataclass

from model.Constructor import Constructor


@dataclass
class Arco:
    constructor1 : Constructor
    constructor2: Constructor