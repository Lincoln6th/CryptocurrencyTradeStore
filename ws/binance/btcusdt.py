from .binance_ws import BinanceWS
from ws.ws_const import ExchangeType

class BinanceBTCUSDT(BinanceWS):
    ws_url = 'wss://stream.binance.com/ws/btcusdt@trade'
    ex_key = ExchangeType.binance['btcusdt']