# sample script 1.
# real-time print by WS-processor.

import time

from ws import (
    ExchangeType,

    BitfinexWS,
    BitflyerWS,
    BitflyerFxWS,
    BitstampWS,

    WebSocketProcessor,
)

from ws.binance import (
    BinanceBTCUSDT,
    BinanceBCHUSDT,
    BinanceETHUSDT,
    BinanceF_BCHUSDT,
    BinanceF_BTCUSDT,
    BinanceF_ETHUSDT
)

from ws.bitmex import (

    BitmexBCHH20,
    BitmexBTCUSD,
    BitmexETHUSD
)
import asyncio
from trade_sql import TradesSQL

def main():
    ws_processor = WebSocketProcessor().add_ws(
        BitfinexWS,
        BitflyerWS,
        BitflyerFxWS,
        BitstampWS,
        BinanceBTCUSDT,
        BinanceBCHUSDT,
        BinanceETHUSDT,
        BinanceF_BCHUSDT,
        BinanceF_BTCUSDT,
        BinanceF_ETHUSDT,
        BitmexBCHH20,
        BitmexBTCUSD,
        BitmexETHUSD
    ).run()
    
    trades_sql = TradesSQL(ws_processor)
    loop = asyncio.get_event_loop()
    tasks = asyncio.wait([
        trades_sql.store_executions_regularly(),
        trades_sql.delete_datas_regularly(),
    ])
    loop.run_until_complete(tasks)

if __name__ == '__main__':
    main()

