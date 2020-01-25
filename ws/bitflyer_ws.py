import json
import time
import pytz

from .ws_const import ExchangeType
from .ws_base import WebSocketBase
from datetime import datetime


class BitflyerWS(WebSocketBase):

    ws_url = 'wss://ws.lightstream.bitflyer.com/json-rpc'

    def subscribe(self):
        message = json.dumps({
            'method': 'subscribe',
            'params': {
                'channel': 'lightning_executions_BTC_JPY'
            }
        })
        self.ws.send(message)

    def decode_message(self, message):
        try:
            rcv_time = time.time()

            m = json.loads(message)
            trades = m['params']['message']

            return list(map(lambda x: {
                'ex_key': ExchangeType.bitflyer,
                'price': x['price'],
                'size': x['size'] if x['side'] == 'BUY' else -x['size'],
                'time': self.timestamp_convert(x['exec_date']),
                'rcv_time': rcv_time,
                'latency' : rcv_time - self.timestamp_convert(x['exec_date'])
            }, trades)), True
        except Exception as e:
            # raise or log if you need.
            return [], False

    def timestamp_convert(self, exec_date):
        dt, _, ms = exec_date.partition(".")
        dt = dt + '.' + ms[:6].rstrip("Z")
        dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=pytz.utc)
        return dt.timestamp()
