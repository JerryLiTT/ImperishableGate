import sqlite3

# 通过 main.py 初始化时传入 conn 和 cursor
conn = None
cursor = None

def init_db(connection):
    """初始化数据库连接和游标"""
    global conn, cursor
    conn = connection
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY,
        url TEXT NOT NULL UNIQUE,
        note TEXT
    )
    """)
    conn.commit()

def add_link(url: str):
    """添加链接"""
    try:
        cursor.execute("INSERT INTO links (url) VALUES (?)", (url,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def delete_link(url: str):
    """删除链接"""
    cursor.execute("DELETE FROM links WHERE url = ?", (url,))
    conn.commit()

def get_all_links():
    """获取全部链接"""
    cursor.execute("SELECT id, url, note FROM links")
    return cursor.fetchall()

def link_exists(url: str) -> bool:
    """检查链接是否存在"""
    cursor.execute("SELECT 1 FROM links WHERE url = ?", (url,))
    return cursor.fetchone() is not None

