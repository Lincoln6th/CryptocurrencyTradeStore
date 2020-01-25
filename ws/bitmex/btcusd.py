from .bitmex_ws import BitmexWS
from ws.ws_const import ExchangeType

class BitmexBTCUSD(BitmexWS):
    ex_key = ExchangeType.bitmex['btcusd']
    trade_symbol = 'XBTUSD'