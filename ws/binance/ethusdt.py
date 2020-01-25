from .binance_ws import BinanceWS
from ws.ws_const import ExchangeType

class BinanceETHUSDT(BinanceWS):
    ws_url = 'wss://stream.binance.com/ws/ethusdt@trade'
    ex_key = ExchangeType.binance['ethusdt']