from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Any
from py_clob_client.clob_types import (
    Market,
    RewardsMarket,
    Token,
    Rewards,
    RewardsConfig,
    RewardRate,
    TimeSeriesPoint,
    OrderSummary,
    OrderBookSummary,
)


class ResponseStatus(Enum):
    SUCCESS = 0
    ERROR = 1


@dataclass
class Response:
    status_code: ResponseStatus


@dataclass
class ErrorResponse(Response):
    error: str = ""


@dataclass
class GetMarketResponse(Response):
    market: Optional[Market] = None

    @classmethod
    def load_from_dict(cls, data: dict):
        print(data)
        return cls(ResponseStatus.SUCCESS, Market.load_from_dict(data))


@dataclass
class GetMarketsResponse(Response):
    data: List[Market] = field(default_factory=list)
    next_cursor: str = ""
    limit: int = 0
    count: int = 0

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(
            ResponseStatus.SUCCESS,
            [Market.load_from_dict(market) for market in data.get("data")],
            data.get("next_cursor"),
            data.get("limit"),
            data.get("count"),
        )


@dataclass
class GetPricesHistoryResponse(Response):
    history: List[TimeSeriesPoint] = field(default_factory=list)

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(
            ResponseStatus.SUCCESS,
            [TimeSeriesPoint.load_from_dict(point) for point in data.get("history")],
        )


@dataclass
class GetOrderBookResponse(Response):
    order_book: OrderBookSummary

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(ResponseStatus.SUCCESS, OrderBookSummary.load_from_dict(data))


@dataclass
class GetOrderBooksResponse(Response):
    order_books: List[OrderBookSummary] = field(default_factory=list)

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(
            ResponseStatus.SUCCESS,
            [OrderSummary.load_from_dict(order_book) for order_book in data],
        )
