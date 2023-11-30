import sqlite3

class Catalogo:
    def __init__(self, nome_banco='catalogo.db'):
        self.conn = sqlite3.connect(nome_banco)
        self.c = self.conn.cursor()

    def _criar_tabelas(self):
        # Criação da tabela "type" se ela não existir
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS type (
                typeid INTEGER PRIMARY KEY AUTOINCREMENT,
                typename TEXT NOT NULL
            )
        ''')

        # Criação da tabela "item" se ela não existir
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS item (
                itemid INTEGER PRIMARY KEY AUTOINCREMENT,
                itemname TEXT,
                itemtype INTEGER,
                FOREIGN KEY (itemtype) REFERENCES type(typeid)
            )
        ''')

        # Criação da tabela "user" se ela não existir
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS user (
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE
            )
        ''')

        # Criação da tabela "favs" se ela não existir
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS favs (
                favid INTEGER PRIMARY KEY AUTOINCREMENT,
                favuser INTEGER,
                favitem item,
                FOREIGN KEY (favuser) REFERENCES user(userid),
                FOREIGN KEY (favitem) REFERENCES user(itemid)
            )
        ''')

        self.conn.commit()

    def _criar_tipos(self):
        # Faz os inserts dos tipos disponiveis
        self.insert_type('Filme')
        self.insert_type('Série')
        self.insert_type('Anime')
        self.insert_type('Outro')

    def insert_type(self, typename):
        self.c.execute('''
            INSERT INTO type (typename)
            VALUES (?)
        ''', (typename,))
        self.conn.commit()

    def insert_item(self, itemname, itemtype):
        self.c.execute('''
            INSERT INTO item (itemname, itemtype)
            VALUES (?, ?)
        ''', (itemname, itemtype))
        self.conn.commit()

    def insert_user(self, username):
        self.c.execute('''
            INSERT INTO user (username)
            VALUES (?)
        ''', (username,))
        self.conn.commit()

    def get_user_id(self, username):
        self.c.execute('''
            SELECT userid FROM user
            WHERE username=?
        ''', (username,))
        return self.c.fetchall()

    def insert_favorites(self, user_id, item_id):
        self.c.execute('''
            INSERT INTO favs (favuser, favitem)
            VALUES(?, ?)
        ''', (user_id, item_id))
        self.conn.commit()

    def was_favorited(self, user_id, item_id):
        self.c.execute('''
            SELECT favid from favs
            WHERE favuser = ? AND favitem = ?
        ''', (user_id, item_id))
        return self.c.fetchall()

    def delete_favorites(self, fav_id):
        self.c.execute('''
            DELETE FROM favs
            WHERE favid=?
        ''', (fav_id,))
        self.conn.commit()

    def update_item(self, itemid, itemname, itemtype):
        self.c.execute('''
            UPDATE item
            SET itemname=?, itemtype=?
            WHERE itemid=?
        ''', (itemname, itemtype, itemid))
        self.conn.commit()

    def delete_item(self, itemid):
        self.c.execute('''
            DELETE FROM item
            WHERE itemid=?
        ''', (itemid,))
        self.conn.commit()

    def query_items(self):
        self.c.execute('''
            SELECT item.itemid, item.itemname, type.typename
            FROM item
            INNER JOIN type ON item.itemtype = type.typeid
        ''')
        return self.c.fetchall()
    
    def query_types(self):
        self.c.execute('''
            SELECT type.typeid, type.typename FROM type
        ''')
        return self.c.fetchall()
    
    def query_favorites(self, user_id):
        self.c.execute('''
            SELECT favs.favid, item.itemname, type.typename
            FROM favs
            INNER JOIN item ON favs.favitem = item.itemid
            INNER JOIN type on item.itemtype = type.typeid
            WHERE favs.favuser=?
        ''', (user_id,))
        return self.c.fetchall()


    def search_items(self, searchname: str):
        self.c.execute('''
            SELECT item.itemid, item.itemname, type.typename
            FROM item INNER JOIN type ON item.itemtype = type.typeid
            WHERE item.itemname LIKE ? ORDER BY item.itemname asc
        ''', ('%' + searchname + '%',))
        return self.c.fetchall()
    
    def search_favorites(self, user_id, searchname: str):
        self.c.execute('''
            SELECT favs.favid, item.itemname, type.typename
            FROM favs
            INNER JOIN item ON favs.favitem = item.itemid
            INNER JOIN type on item.itemtype = type.typeid
            WHERE favs.favuser=? and item.itemname LIKE ? ORDER BY item.itemname asc
        ''', (user_id, '%' + searchname + '%',))
        return self.c.fetchall()

    def close_connection(self):
        self.conn.close()