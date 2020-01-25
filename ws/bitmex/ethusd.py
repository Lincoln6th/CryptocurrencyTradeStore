from .bitmex_ws import BitmexWS
from ws.ws_const import ExchangeType

class BitmexETHUSD(BitmexWS):
    ex_key = ExchangeType.bitmex['ethusd']
    trade_symbol = 'ETHUSD'
