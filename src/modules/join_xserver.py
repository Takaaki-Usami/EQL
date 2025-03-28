import mysql.connector
from sshtunnel import SSHTunnelForwarder


class xserver_class:
    def __init__(self):
        self.ssh_host = '{サーバー番号}.xserver.jp'
        self.ssh_port = {SSH接続ポート}
        self.ssh_user = '{サーバーID}'
        self.ssh_password = '{パスフレーズ}'
        self.ssh_pkey = R'{秘密鍵ファイルのフルパス}'

        self.db_name = '{MySQLデータベース名}'
        self.db_user = '{MySQLユーザー名}'
        self.db_password = '{MySQLパスワード}'
        self.db_host = '{ホスト名}'
        self.db_port = {DB接続ポート}
        self.db_charset = '{文字コード}'

    def __connect__(self):
        self.server = SSHTunnelForwarder(
            (self.ssh_host, self.ssh_port),
            ssh_username=self.ssh_user,
            ssh_password=self.ssh_password,
            ssh_pkey=self.ssh_pkey,
            remote_bind_address=(self.db_host, self.db_port),
        )
        self.server.start()
        # connectのリファレンスはコチラ
        # https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        self.con = mysql.connector.connect(
            host=self.db_host,
            port=self.server.local_bind_port,
            user=self.db_user,
            passwd=self.db_password,
            db=self.db_name,
            charset=self.db_charset,
            use_pure=True,
        )
        # 扱いやすいdict型を指定しておく
        self.cur = self.con.cursor(dictionary=True)
        # コネクションの設定
        self.con.autocommit = False

    def __disconnect__(self):
        self.con.close()
        self.server.stop()

    def fetch(self, sql):
        self.con.ping(reconnect=True)
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    def execute(self, sql):
        self.con.ping(reconnect=True)
        self.cur.execute(sql)
        self.con.commit()

    def open(self):
        self.__connect__()

    def close(self):
        self.__disconnect__()