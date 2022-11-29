from dataclasses import dataclass
from typing import Literal

from pandas import DataFrame


@dataclass
class ResponseDataFrame:

    df: DataFrame
    response_id: Literal['Google', 'Catalogue']