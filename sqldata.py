import sqlite3
# Запросы к базе

class sqldata:
  def __init__(self, database):
    """Подключаемся к БД и сохраняем курсор соединения"""
    self.connection = sqlite3.connect(database, isolation_level=None)
    self.cursor = self.connection.cursor()

  def add_user(self, *args):
    #user_id,first_name, last_name,username,language_code,fdate,ldate = args
    with self.connection:
      return self.cursor.execute("INSERT OR IGNORE INTO user('user_id', 'first_name', 'last_name', 'username', 'language_code', 'first_date', 'last_date') VALUES(?,?,?,?,?,?,?)", ([x for x in args]))

  def add_last_date(self, date, user_id):
    # обновляем дату последнего посещения
    with self.connection:
      return self.cursor.execute("UPDATE user SET last_date = ? WHERE user_id = ?", (date, user_id))

  def insert_cutter(self, user_id, service):
    # вносим в базу выбранный сервис
    if service == "None":
      with self.connection:
        return self.cursor.execute("INSERT OR IGNORE INTO select_service('user_id','cutter_service') VALUES(?,?)", (user_id, service))
    else:
      with self.connection:
        return self.cursor.execute("UPDATE select_service SET cutter_service = ? WHERE user_id = ?", (service, user_id))

  def select_cutter(self, user_id):
    with self.connection:
      return self.cursor.execute("SELECT * FROM select_service WHERE user_id = ?", (user_id,)).fetchall()[0]

  def add_stat_url(self, user_id, service, url, date):
    with self.connection:
      return self.cursor.execute("INSERT INTO bitly_stat(user_id,service,url,date) VALUES(?,?,?,?)", (user_id,service,url,date))

  def select_stat_url(self, user_id, service):
    with self.connection:
      return self.cursor.execute("SELECT url,date FROM bitly_stat WHERE user_id = ? AND service = ?", (user_id,service)).fetchall()


  def close(self):
      """Закрываем соединение с БД"""
      self.connection.close()

  def init_bd(self):
    self.cursor.execute("""create table if not exists user(
      user_id         integer not null unique,
      first_name      text,
      last_name       text,
      username        text,
      language_code   text,
      first_date      text,
      last_date       text)"""
      )

    self.cursor.execute("""create table if not exists select_service(
      user_id         integer not null unique,
      cutter_service  text)"""
      )

    self.cursor.execute("""create table if not exists bitly_stat(
      id              integer primary key autoincrement,
      user_id         integer,
      service         text,
      url             text,
      date            text)"""
      )
