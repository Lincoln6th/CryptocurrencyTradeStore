from .binance_ws import BinanceWS
from ws.ws_const import ExchangeType

class BinanceF_BTCUSDT(BinanceWS):
    ws_url = 'wss://fstream.binance.com/ws/btcusdt@trade'
    ex_key = ExchangeType.binance['f_btcusdt']