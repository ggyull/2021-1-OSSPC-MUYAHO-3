import pymysql

class Database:

    def __init__(self):                                                         #데이터베이스 생성자
        self.score_db = pymysql.connect(
        user = 'user',
        passwd = 'muyaho12',
        host = 'muyahotris.cbsjhgovfxo7.ap-northeast-2.rds.amazonaws.com',
        db = 'muyahotris',
        charset = 'utf8'
        )

    def load_data(self, game_mode):                                             #데이터 베이스에서 데이터 불러오기
        pass
        curs = self.score_db.cursor(pymysql.cursors.DictCursor)
        if game_mode == 'Easy':
            sql = "select * from easymode_score order by score desc "
        elif game_mode == 'Hard':
            sql = "select * from hardmode_score order by score desc"
        elif game_mode == 'Level':
            sql = "select * from levelmode_score order by level desc"
        curs.execute(sql)
        data = curs.fetchall()
        curs.close()
        return data

    def add_data(self,game_mode,  ID, score):                                   #데이터 베이스에서 데이터 추가하기
        curs = self.score_db.cursor()
        if game_mode == 'Easy':
            sql = "INSERT INTO easymode_score (ID, score) VALUES (%s, %s)"
            curs.execute(sql, (ID, score))
        elif game_mode == 'Hard':
            sql = "INSERT INTO hardmode_score (ID, score) VALUES (%s, %s)"
            curs.execute(sql, (ID, score))
        elif game_mode == 'Level':
            sql = "INSERT INTO levelmode_score (ID, level) VALUES (%s, %s)"
            curs.execute(sql, (ID, score))
        self.score_db.commit()
        curs.close()
