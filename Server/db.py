import sqlite3

# 通过 main.py 初始化时传入 conn 和 cursor
conn = None
cursor = None

def init_db(connection):
    """初始化数据库连接和游标"""
    global conn, cursor
    conn = connection
    cursor = conn.cursor()
    # links 表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY,
        url TEXT NOT NULL UNIQUE,
        note TEXT
    )
    """)
    # tags 表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY,
        tag TEXT NOT NULL UNIQUE
    )
    """)
    # link&tag多对多关系表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS link_tags (
        link_id INTEGER NOT NULL,
        tag_id INTEGER NOT NULL,
        PRIMARY KEY (link_id, tag_id),
        FOREIGN KEY (link_id) REFERENCES links(id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
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











def add_tag_to_url(url: str, tag: str):
    """给指定 url 添加 tag"""
    # 确保 url 存在
    cursor.execute("SELECT id FROM links WHERE url = ?", (url,))
    row = cursor.fetchone()
    if not row:
        return False  # url 不存在
    link_id = row[0]

    # 确保 tag 存在，不存在则创建
    cursor.execute("INSERT OR IGNORE INTO tags (tag) VALUES (?)", (tag,))
    conn.commit()
    cursor.execute("SELECT id FROM tags WHERE tag = ?", (tag,))
    tag_id = cursor.fetchone()[0]

    # 插入关系
    cursor.execute("INSERT OR IGNORE INTO link_tags (link_id, tag_id) VALUES (?, ?)", (link_id, tag_id))
    conn.commit()
    return True


def remove_tag_from_url(url: str, tag: str):
    """删除 url 的指定 tag"""
    cursor.execute("SELECT id FROM links WHERE url = ?", (url,))
    link = cursor.fetchone()
    if not link:
        return False
    link_id = link[0]

    cursor.execute("SELECT id FROM tags WHERE tag = ?", (tag,))
    t = cursor.fetchone()
    if not t:
        return False
    tag_id = t[0]

    cursor.execute("DELETE FROM link_tags WHERE link_id = ? AND tag_id = ?", (link_id, tag_id))
    conn.commit()
    return True


def get_tags_by_url(url: str):
    """查询 url 对应的所有 tag"""
    cursor.execute("""
        SELECT tags.tag 
        FROM tags
        JOIN link_tags ON tags.id = link_tags.tag_id
        JOIN links ON links.id = link_tags.link_id
        WHERE links.url = ?
    """, (url,))
    return [row[0] for row in cursor.fetchall()]#形如['工作', '学习']


def get_urls_by_tag(tag: str):
    """查询 tag 对应的所有 url"""
    cursor.execute("""
        SELECT links.url
        FROM links
        JOIN link_tags ON links.id = link_tags.link_id
        JOIN tags ON tags.id = link_tags.tag_id
        WHERE tags.tag = ?
    """, (tag,))
    return [row[0] for row in cursor.fetchall()]










def add_note_to_url(url: str, note: str) -> bool:
    """给指定 url 添加 note（仅当该 url 存在且当前 note 为空时成功）"""
    cursor.execute("SELECT note FROM links WHERE url = ?", (url,))
    row = cursor.fetchone()
    if not row:
        return False  # url 不存在
    if row[0] is not None:  # 已经有 note
        return False
    cursor.execute("UPDATE links SET note = ? WHERE url = ?", (note, url))
    conn.commit()
    return True


def update_note_of_url(url: str, note: str) -> bool:
    """修改指定 url 的 note（如果 url 存在则覆盖）"""
    cursor.execute("SELECT id FROM links WHERE url = ?", (url,))
    if cursor.fetchone() is None:
        return False
    cursor.execute("UPDATE links SET note = ? WHERE url = ?", (note, url))
    conn.commit()
    return True


def delete_note_of_url(url: str) -> bool:
    """删除指定 url 的 note（置空）"""
    cursor.execute("SELECT id FROM links WHERE url = ?", (url,))
    if cursor.fetchone() is None:
        return False
    cursor.execute("UPDATE links SET note = NULL WHERE url = ?", (url,))
    conn.commit()
    return True


def has_note(url: str) -> bool:
    """检查指定 url 是否有 note"""
    cursor.execute("SELECT note FROM links WHERE url = ?", (url,))
    row = cursor.fetchone()
    return row is not None and row[0] is not None


def get_note_by_url(url: str):
    """获取指定 url 的 note（如果不存在则返回 None）"""
    cursor.execute("SELECT note FROM links WHERE url = ?", (url,))
    row = cursor.fetchone()
    if not row:
        return None  # url 不存在
    return row[0]  # 可能是 str 或 None




