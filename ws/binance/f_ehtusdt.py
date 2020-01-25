from .binance_ws import BinanceWS
from ws.ws_const import ExchangeType

class BinanceF_ETHUSDT(BinanceWS):
    ws_url = 'wss://fstream.binance.com/ws/ethusdt@trade'
    ex_key = ExchangeType.binance['f_ethusdt']