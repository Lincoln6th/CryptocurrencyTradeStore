from .binance_ws import BinanceWS
from ws.ws_const import ExchangeType

class BinanceBCHUSDT(BinanceWS):
    ws_url = 'wss://stream.binance.com:9443/ws/bchusdt@trade'
    ex_key = ExchangeType.binance['bchusdt']