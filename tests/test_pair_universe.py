import datetime

import pytest

from tradingstrategy.chain import ChainId
from tradingstrategy.pair import LegacyPairUniverse, PairType, DEXPair


def test_pair_pyarrow_schema():
    """We get a good Pyrarow schema for pair information serialisation and deserialisation."""

    schema = DEXPair.to_pyarrow_schema()
    assert str(schema[0].type) == "uint32"  # Primary key


def test_write_pyarrow_table():
    """We get a good Pyrarow schema for pair information serialisation and deserialisation."""

    items = [
        DEXPair(
            pair_id=1,
            chain_id=ChainId.ethereum,
            exchange_id=1,
            address="0x0000000000000000000000000000000000000000",
            dex_type=PairType.uniswap_v2,
            base_token_symbol="WETH",
            quote_token_symbol="USDC",
            token0_symbol="USDC",
            token1_symbol="WETH",
            token0_address="0x0000000000000000000000000000000000000000",
            token1_address="0x0000000000000000000000000000000000000000",
            first_swap_at_block_number=1,
            last_swap_at_block_number=1,
            first_swap_at=int(datetime.datetime(2020, 6, 4, 11, 42, 39).timestamp()),
            last_swap_at=int(datetime.datetime(2020, 6, 4, 11, 42, 39).timestamp()),
            flag_inactive=False,
            flag_blacklisted_manually=False,
            flag_unsupported_quote_token=False,
            flag_unknown_exchange=False
        )
    ]
    table = DEXPair.convert_to_pyarrow_table(items)
    assert len(table) == 1


def test_pair_info_url():
    """We get a good info URLs"""

    p = DEXPair(
            pair_id=1,
            chain_id=ChainId.ethereum,
            exchange_id=1,
            address="0x0000000000000000000000000000000000000000",
            dex_type=PairType.uniswap_v2,
            base_token_symbol="WETH",
            quote_token_symbol="USDC",
            token0_symbol="USDC",
            token1_symbol="WETH",
            token0_address="0x0000000000000000000000000000000000000000",
            token1_address="0x0000000000000000000000000000000000000000",
            exchange_slug="uniswap-v2",
            pair_slug="eth-usdc",
            token0_decimals=6,
            token1_decimals=18,
            flag_inactive=False,
            flag_blacklisted_manually=False,
            flag_unsupported_quote_token=False,
            flag_unknown_exchange=False,
        )
    assert p.get_trading_pair_page_url() == "https://tradingstrategy.ai/trading-view/ethereum/uniswap-v2/eth-usdc"
    assert p.base_token_decimals == 18
    assert p.quote_token_decimals == 6
