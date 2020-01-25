import json
import time
import pytz

from ws.ws_const import ExchangeType
from ws.ws_base import WebSocketBase
from datetime import datetime


class BitmexWS(WebSocketBase):

    ws_url = 'wss://www.bitmex.com/realtime'
    ex_key = None
    trade_symbol = None

    def subscribe(self):
        message = json.dumps({
            'op': 'subscribe',
            'args': [
                f'trade:{self.trade_symbol}',
            ]
        })
        self.ws.send(message)

    def decode_message(self, message):
        try:
            rcv_time = time.time()

            m = json.loads(message)
            trades = m['data']
            if 'table' not in m:
                return [], False
                
            return list(map(lambda x: {
                'ex_key': self.ex_key,
                'price': x['price'],
                'size': (x['size']/x['price']) if x['side'] == 'Buy' else -(x['size']/x['price']),
                'time': self.timestamp_convert(x['timestamp']),
                'rcv_time': rcv_time,
                'latency' : rcv_time - self.timestamp_convert(x['timestamp'])
            }, trades)), True

        except Exception as e:
            # raise or log if you need.
            return [], False

    def timestamp_convert(self, exec_date):
        dt, _, ms = exec_date.partition(".")
        dt = dt + '.' + ms[:6].rstrip("Z")
        dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=pytz.utc)
        return dt.timestamp()
