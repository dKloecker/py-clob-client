from typing import Any, List, Optional
from dataclasses import dataclass, asdict
from json import dumps
from typing import Literal, Optional
from enum import Enum

from .constants import ZERO_ADDRESS


class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"


class NextCursor(Enum):
    BEGINNING = ""
    END = "LTE="


@dataclass
class ApiCreds:
    api_key: str
    api_secret: str
    api_passphrase: str


@dataclass
class RequestArgs:
    method: str
    request_path: str
    body: Any = None


@dataclass
class BookParams:
    token_id: str
    side: str = ""


@dataclass
class OrderArgs:
    token_id: str
    """
    TokenID of the Conditional token asset being traded
    """

    price: float
    """
    Price used to create the order
    """

    size: float
    """
    Size in terms of the ConditionalToken
    """

    side: str
    """
    Side of the order
    """

    fee_rate_bps: int = 0
    """
    Fee rate, in basis points, charged to the order maker, charged on proceeds
    """

    nonce: int = 0
    """
    Nonce used for onchain cancellations
    """

    expiration: int = 0
    """
    Timestamp after which the order is expired.
    """

    taker: str = ZERO_ADDRESS
    """
    Address of the order taker. The zero address is used to indicate a public order
    """


@dataclass
class MarketOrderArgs:
    token_id: str
    """
    TokenID of the Conditional token asset being traded
    """

    amount: float
    """
    Amount in terms of Collateral
    """

    price: float = 0
    """
    Price used to create the order
    """

    fee_rate_bps: int = 0
    """
    Fee rate, in basis points, charged to the order maker, charged on proceeds
    """

    nonce: int = 0
    """
    Nonce used for onchain cancellations
    """

    taker: str = ZERO_ADDRESS
    """
    Address of the order taker. The zero address is used to indicate a public order
    """


@dataclass
class TradeParams:
    id: str = None
    maker_address: str = None
    market: str = None
    asset_id: str = None
    before: int = None
    after: int = None


@dataclass
class OpenOrderParams:
    id: str = None
    market: str = None
    asset_id: str = None


@dataclass
class DropNotificationParams:
    ids: list[str] = None


@dataclass
class OrderSummary:
    price: str = None
    size: str = None

    @property
    def __dict__(self):
        return asdict(self)

    @property
    def json(self):
        return dumps(self.__dict__)

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(price=data.get("price"), size=data.get("size"))


@dataclass
class OrderBookSummary:
    market: str = None
    asset_id: str = None
    timestamp: str = None
    bids: list[OrderSummary] = None
    asks: list[OrderSummary] = None
    hash: str = None

    @property
    def __dict__(self):
        return asdict(self)

    @property
    def json(self):
        return dumps(self.__dict__, separators=(",", ":"))

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(
            market=data.get("market"),
            asset_id=data.get("asset_id"),
            timestamp=data.get("timestamp"),
            bids=[OrderSummary.load_from_dict(bid) for bid in data.get("bids")],
            asks=[OrderSummary.load_from_dict(ask) for ask in data.get("asks")],
            hash=data.get("hash"),
        )


class AssetType(enumerate):
    COLLATERAL = "COLLATERAL"
    CONDITIONAL = "CONDITIONAL"


@dataclass
class BalanceAllowanceParams:
    asset_type: AssetType = None
    token_id: str = None
    signature_type: int = -1


class OrderType(enumerate):
    GTC = "GTC"
    FOK = "FOK"
    GTD = "GTD"


class Interval(enumerate):
    MAX = "max"
    ONE_MONTH = "1m"
    ONE_WEEK = "1w"
    ONE_DAY = "1d"
    SIX_HOURS = "6h"
    ONE_HOUR = "1h"


@dataclass
class OrderScoringParams:
    orderId: str


@dataclass
class OrdersScoringParams:
    orderIds: list[str]


TickSize = Literal["0.1", "0.01", "0.001", "0.0001"]


@dataclass
class CreateOrderOptions:
    tick_size: TickSize
    neg_risk: bool


@dataclass
class PartialCreateOrderOptions:
    tick_size: Optional[TickSize] = None
    neg_risk: Optional[bool] = None


@dataclass
class RoundConfig:
    price: float
    size: float
    amount: float


@dataclass
class ContractConfig:
    """
    Contract Configuration
    """

    exchange: str
    """
    The exchange contract responsible for matching orders
    """

    collateral: str
    """
    The ERC20 token used as collateral for the exchange's markets
    """

    conditional_tokens: str
    """
    The ERC1155 conditional tokens contract
    """


@dataclass
class Token:
    token_id: str
    outcome: str
    price: float
    winner: bool

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(
            token_id=data.get("token_id"),
            outcome=data.get("outcome"),
            price=data.get("price"),
            winner=data.get("winner"),
        )


@dataclass
class RewardRate:
    asset_address: str
    rewards_daily_rate: float

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(
            asset_address=data.get("asset_address"),
            rewards_daily_rate=data.get("rewards_daily_rate"),
        )


@dataclass
class Rewards:
    rates: List[RewardRate]
    min_size: float
    max_spread: float

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(
            rates=[RewardRate.load_from_dict(rate) for rate in data.get("rates")],
            min_size=data.get("min_size"),
            max_spread=data.get("max_spread"),
        )


@dataclass
class RewardsConfig:
    asset_address: str
    start_date: str
    end_date: str
    id: int
    rate_per_day: float
    total_rewards: float
    total_days: int

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(
            asset_address=data.get("asset_address"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            id=data.get("id"),
            rate_per_day=data.get("rate_per_day"),
            total_rewards=data.get("total_rewards"),
            total_days=data.get("total_days"),
        )


@dataclass
class SimplifiedMarket:
    condition_id: str
    tokens: List[Token]
    rewards: Rewards
    min_incentive_size: str
    max_incentive_spread: str
    active: bool
    closed: bool

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(
            condition_id=data.get("condition_id"),
            tokens=[Token.load_from_dict(token) for token in data.get("tokens")],
            rewards=Rewards.load_from_dict(data.get("rewards")),
            min_incentive_size=data.get("min_incentive_size"),
            max_incentive_spread=data.get("max_incentive_spread"),
            active=data.get("active"),
            closed=data.get("closed"),
        )


@dataclass
class Market:
    enable_order_book: bool
    active: bool
    closed: bool
    archived: bool
    accepting_orders: bool
    accepting_order_timestamp: str
    minimum_order_size: float
    minimum_tick_size: float
    condition_id: str
    question_id: str
    question: str
    description: str
    market_slug: str
    end_date_iso: str
    game_start_time: Optional[str]
    seconds_delay: int
    fpmm: Optional[str]
    maker_base_fee: float
    taker_base_fee: float
    notifications_enabled: bool
    neg_risk: bool
    neg_risk_market_id: Optional[str]
    neg_risk_request_id: Optional[str]
    icon: str
    image: str
    rewards: Rewards
    is_50_50_outcome: bool
    tokens: List[Token]
    tags: List[str]

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(
            enable_order_book=data.get("enable_order_book"),
            active=data.get("active"),
            closed=data.get("closed"),
            archived=data.get("archived"),
            accepting_orders=data.get("accepting_orders"),
            accepting_order_timestamp=data.get("accepting_order_timestamp"),
            minimum_order_size=data.get("minimum_order_size"),
            minimum_tick_size=data.get("minimum_tick_size"),
            condition_id=data.get("condition_id"),
            question_id=data.get("question_id"),
            question=data.get("question"),
            description=data.get("description"),
            market_slug=data.get("market_slug"),
            end_date_iso=data.get("end_date_iso"),
            game_start_time=data.get("game_start_time"),
            seconds_delay=data.get("seconds_delay"),
            fpmm=data.get("fpmm"),
            maker_base_fee=data.get("maker_base_fee"),
            taker_base_fee=data.get("taker_base_fee"),
            notifications_enabled=data.get("notifications_enabled"),
            neg_risk=data.get("neg_risk"),
            neg_risk_market_id=data.get("neg_risk_market_id"),
            neg_risk_request_id=data.get("neg_risk_request_id"),
            icon=data.get("icon"),
            image=data.get("image"),
            rewards=Rewards.load_from_dict(data.get("rewards")),
            is_50_50_outcome=data.get("is_50_50_outcome"),
            tokens=[Token.load_from_dict(token) for token in data.get("tokens")],
            tags=data.get("tags"),
        )


@dataclass
class RewardsMarket:
    condition_id: str
    question: str
    market_slug: str
    event_slug: str
    image: str
    tokens: List[Token]
    rewards_config: RewardsConfig
    rewards_max_spread: float
    rewards_min_size: float

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(
            condition_id=data.get("condition_id"),
            question=data.get("question"),
            market_slug=data.get("market_slug"),
            event_slug=data.get("event_slug"),
            image=data.get("image"),
            tokens=[Token.load_from_dict(token) for token in data.get("tokens")],
            rewards_config=RewardsConfig.load_from_dict(data.get("rewards_config")),
            rewards_max_spread=data.get("rewards_max_spread"),
            rewards_min_size=data.get("rewards_min_size"),
        )


@dataclass
class TimeSeriesPoint:
    utc_timestamp: int
    price: float

    @classmethod
    def load_from_dict(cls, data: dict):
        return cls(utc_timestamp=data.get("t"), price=data.get("p"))
