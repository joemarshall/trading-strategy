"""Exchange information and analysis."""

import enum
from dataclasses import dataclass
from typing import Optional, List, Iterable, Dict

from dataclasses_json import dataclass_json

from capitalgram.chain import ChainId
from capitalgram.types import NonChecksummedAddress, UNIXTimestamp, PrimaryKey


class ExchangeType(enum.Enum):
    """What kind of an decentralised exchange, AMM or other the pair is trading on.

    Note that each type can have multiple implementations.
    For example QuickSwap, Sushi and Pancake are all Uniswap v2 types.
    """

    #: Uniswap v2 style exchange
    uniswap_v2 = "uni_v2"

    #: Uniswap v3 style exchange
    uniswap_v3 = "uni_v3"


@dataclass_json
@dataclass
class Exchange:
    """A decentralised exchange.

    Each chain can have multiple active or abadon decentralised exchanges
    of different types, like :term:`AMM` based or order book based.

    The :term:`dataset server` server automatically discovers exchanges
    and tries to add meaningful label and risk data for them.

    Regarding 30d and life time stats like `buy_volume_30d`:
    These stats calculated only if exchanged deemed active and we
    can convert the volume to a supported quote token.
    Any unsupported token volume does not show up in these stats.
    Useful mostly for risk assessment, as this data is **not** accurate,
    but gives some reference information about the popularity of the token.
    """

    #: The chain id on which chain this pair is trading. 1 for Ethereum.
    chain_id: ChainId

    #: The exchange where this token trades
    exchange_id: PrimaryKey

    #: The factory smart contract address of Uniswap based exchanges
    address: NonChecksummedAddress

    #: What kind of exchange is this
    exchange_type: ExchangeType

    #: How many pairs we have discovered for this exchange so far
    pair_count: int

    #: When someone traded on this exchange last time
    last_trade_at: Optional[UNIXTimestamp] = None

    #: Exchange name - if known or guessed
    name: Optional[str] = None

    #: Denormalised exchange statistics
    buy_count_all_time: Optional[int] = None

    #: Denormalised exchange statistics
    sell_count_all_time: Optional[int] = None

    #: Denormalised exchange statistics
    buy_volume_all_time: Optional[float] = None

    #: Denormalised exchange statistics
    sell_volume_all_time: Optional[float] = None

    #: Denormalised exchange statistics
    buy_count_30d: Optional[int] = None

    #: Denormalised exchange statistics
    sell_count_30d: Optional[int] = None

    #: Denormalised exchange statistics
    buy_volume_30d: Optional[float] = None

    #: Denormalised exchange statistics
    sell_volume_30d: Optional[float] = None

    def __repr__(self):
        chain_name = self.chain_id.name.capitalize()
        name = self.name or "<unknown>"
        return f"<Exchange {name} at {self.address} on {chain_name}>"

    def __json__(self, request):
        """Pyramid JSON renderer compatibility.

        https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/renderers.html#using-a-custom-json-method
        """
        return self.__dict__

    @property
    def vol_30d(self):
        return (self.buy_volume_30d or 0) + (self.sell_volume_30d or 0)


@dataclass_json
@dataclass
class ExchangeUniverse:
    """Exchange manager.

    Contains look up for exchanges by their internal primary key ids.
    """

    #: Exchange id -> Exchange data mapping
    exchanges: Dict[PrimaryKey, Exchange]

    def get_top_exchanges_by_30d_volume(self) -> List[Exchange]:
        """Get top exchanges sorted by their 30d volume.

        Note that we consider volume only for supported quote tokens.
        See :py:class:`capitalgram.exchange.Exchange` for more details.
        """

        def vol(x: Exchange):
            return (x.buy_volume_30d or 0) + (x.sell_volume_30d or 0)

        exchanges = sorted(list(self.exchanges.values()), key=vol, reverse=True)
        return exchanges

    def get_by_name_and_chain(self, chain_id: ChainId, name: str) -> Optional[Exchange]:
        """Get the exchange implementation on a specific chain.

        :param chain_id: Blockchain this exchange is on

        :param name: Like `sushiswap` or `uniswap v2`. Case insensitive.
        """
        assert isinstance(chain_id, ChainId)
        for xchg in self.exchanges.values():
            if xchg.name.lower() == name:
                return xchg
        return None







