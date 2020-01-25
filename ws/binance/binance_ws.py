import json
import time

from ws.ws_const import ExchangeType
from ws.ws_base import WebSocketBase


class BinanceWS(WebSocketBase):
    
    ws_url = 'wss://fstream.binance.com/ws/btcusdt@trade'
    ex_key = None

    def subscribe(self):
        # ws.send() to Binance, is not required
        pass

    def decode_message(self, message):
        try:
            rcv_time = time.time()

            m = json.loads(message)
            e, ut, price = m['e'], m['E'], float(m['p'])
            size = -float(m['q']) if m['m'] else float(m['q'])
            return [{
                'ex_key': self.ex_key,
                'price': price,
                'size': size,
                'time': ut/1000,
                'rcv_time': rcv_time,
                'latency' : rcv_time - int(ut)/1000
            }], True
        except Exception as e:
            # raise or log if you need.
            return [], False
