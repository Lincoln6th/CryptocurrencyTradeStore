from .binance_ws import BinanceWS
from ws.ws_const import ExchangeType

class BinanceF_BCHUSDT(BinanceWS):
    ws_url = 'wss://fstream.binance.com/ws/bchusdt@trade'
    ex_key = ExchangeType.binance['f_bchusdt']