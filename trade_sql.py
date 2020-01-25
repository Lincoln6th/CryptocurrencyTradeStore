import asyncio
import sqlite3
import time
import threading
import pandas as pd
from datetime import datetime, timedelta

class TradesSQL():
    def __init__(self, ws_processor):
        self.dbname = 'bot.db'
        self.table_name = 'trades'
        self.ls_trades = []
        conn = sqlite3.connect(self.dbname)
        with conn:
            create_table = f"""
                            BEGIN TRANSACTION;
                                CREATE TABLE IF NOT EXISTS {self.table_name}(
                                    timestamp REAL,
                                    exchange_kye REAL,
                                    price REAL,
                                    size REAL,
                                    rcv_time TEXT,
                                    latency REAL
                                );
                                CREATE INDEX IF NOT EXISTS I_TIMESTAMP ON {self.table_name} (timestamp);
                            COMMIT TRANSACTION;
                            """
            conn.executescript(create_table)
        self.keep_receiving_trades(ws_processor)
    
    def keep_receiving_trades(self, ws_processor):
        def run():
            try:
                while True:
                    trades = ws_processor.get()
                    self.ls_trades.extend(trades)
            except KeyboardInterrupt:
                print('Closing sockets...')
                ws_processor.close()
        t = threading.Thread(target=run)
        t.start()
    
    @asyncio.coroutine
    def store_executions_regularly(self):
        while True:
            # 10秒ごとにlistをdataframeに変換
            df_exec = pd.DataFrame([[e["time"], e["ex_key"], e["price"], e["size"], e["rcv_time"], e['latency']] for e in self.ls_trades],
                                    columns=["timestamp", "exchange_kye", "price", "size", "rcv_time", "latency"])
            df_exec.set_index(["timestamp"], inplace=True)
            # データベースに挿入
            self.insert_into_db(df_exec)
            # 初期化
            self.ls_trades = []
            yield from asyncio.sleep(10)

    def insert_into_db(self, df_execs):
        conn = sqlite3.connect(self.dbname)
        with conn:
            # DataFrameから約定履歴テーブル作成(T_TEMP)
            # (to_sqlではPKが設定できないので一時テーブルにimportしてからinsertする)
            df_execs.to_sql(
                "T_TEMP", conn, if_exists="replace", index=True)
            sql = f"""
                    BEGIN TRANSACTION;
                        INSERT INTO {self.table_name} SELECT * FROM T_TEMP;
                        DROP TABLE T_TEMP;
                    COMMIT TRANSACTION;
                    """
            conn.executescript(sql)
            # table件数取得
            cursor = conn.cursor()
            sql = f"SELECT COUNT(timestamp) FROM {self.table_name}"
            for row in cursor.execute(sql):
                print("execution:%d" % row[0])

    @asyncio.coroutine
    def delete_datas_regularly(self):
        while True:
            # 2日目のデータを消す
            with sqlite3.connect(self.dbname) as conn:
                _now = datetime.utcnow()
                two_days_ago = (_now - timedelta(days=2)).timestamp()
                sql = "DELETE FROM {}".format(self.table_name) + " WHERE timestamp < {}".format(two_days_ago)
                # table検索
                cursor = conn.cursor()
                cursor.execute(sql)
            # 1時間ごとに実行
            yield from asyncio.sleep(60 * 60)
