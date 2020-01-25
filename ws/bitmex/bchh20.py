from .bitmex_ws import BitmexWS
from ws.ws_const import ExchangeType

class BitmexBCHH20(BitmexWS):
    ex_key = ExchangeType.bitmex['bchusd']
    trade_symbol = 'BCHH20'
