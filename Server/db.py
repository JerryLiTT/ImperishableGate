import sqlite3
import json

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
        note TEXT,
        metainfo TEXT
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
    # names表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS names (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )
    """)
    # link&names多对多关系表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS link_names (
        link_id INTEGER NOT NULL,
        name_id INTEGER NOT NULL,
        PRIMARY KEY (link_id, name_id),
        FOREIGN KEY (link_id) REFERENCES links(id) ON DELETE CASCADE,
        FOREIGN KEY (name_id) REFERENCES names(id) ON DELETE CASCADE
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
    """获取全部链接"""#返回的是(id, url, note)的元组形式！！！
    cursor.execute("SELECT id, url, note FROM links")
    return cursor.fetchall()

def link_exists(url: str) -> bool:
    """检查链接是否存在"""
    cursor.execute("SELECT 1 FROM links WHERE url = ?", (url,))
    return cursor.fetchone() is not None














def get_all_tags() -> list:
    """获取全部 tag（返回纯 tag 列表）"""
    cursor.execute("SELECT tag FROM tags")
    return [row[0] for row in cursor.fetchall()]



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













def add_name_to_url(url: str, name: str) -> bool:
    """给指定 url 添加 name"""
    # 检查 url 是否存在
    cursor.execute("SELECT id FROM links WHERE url = ?", (url,))
    row = cursor.fetchone()
    if not row:
        return False
    link_id = row[0]

    try:
        # 插入全局唯一的 name
        cursor.execute("INSERT INTO names (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # name 已经存在

    # 获取 name id
    cursor.execute("SELECT id FROM names WHERE name = ?", (name,))
    name_id = cursor.fetchone()[0]

    # 建立 link 与 name 的关系
    cursor.execute("INSERT OR IGNORE INTO link_names (link_id, name_id) VALUES (?, ?)", (link_id, name_id))
    conn.commit()
    return True


def remove_name(name: str) -> bool:
    """删除指定 name 以及它与 url 的关系，但不影响 url 与其他 name 的关系"""
    # 获取 name_id
    cursor.execute("SELECT id FROM names WHERE name = ?", (name,))
    row = cursor.fetchone()
    if not row:
        return False  # name 不存在
    name_id = row[0]

    # 删除 link_names 中的所有与该 name 关联的记录
    cursor.execute("DELETE FROM link_names WHERE name_id = ?", (name_id,))

    # 删除 names 表中的该 name
    cursor.execute("DELETE FROM names WHERE id = ?", (name_id,))
    
    conn.commit()
    return True



def get_names_by_url(url: str) -> list:
    """查询 url 对应的所有 name"""
    cursor.execute("""
        SELECT names.name
        FROM names
        JOIN link_names ON names.id = link_names.name_id
        JOIN links ON links.id = link_names.link_id
        WHERE links.url = ?
    """, (url,))
    return [row[0] for row in cursor.fetchall()]


def get_url_by_name(name: str):
    """根据 name 获取对应 url"""
    cursor.execute("""
        SELECT links.url
        FROM links
        JOIN link_names ON links.id = link_names.link_id
        JOIN names ON names.id = link_names.name_id
        WHERE names.name = ?
    """, (name,))
    row = cursor.fetchone()
    return row[0] if row else None


def get_all_names() -> list:
    """获取全部 name（返回纯 name 列表）"""
    cursor.execute("SELECT name FROM names")
    return [row[0] for row in cursor.fetchall()]







def get_info_by_url(url: str):
    """获取指定 URL 的全部信息，返回格式为：
    [url, names列表, note, tags列表, metainfo]
    """
    # URL 本身
    result_url = url

    # 获取 names
    cursor.execute("""
        SELECT names.name
        FROM names
        JOIN link_names ON names.id = link_names.name_id
        JOIN links ON links.id = link_names.link_id
        WHERE links.url = ?
    """, (url,))
    names = [row[0] for row in cursor.fetchall()]  # 可能为空列表

    # 获取 note
    cursor.execute("SELECT note, metainfo FROM links WHERE url = ?", (url,))
    row = cursor.fetchone()
    note = ""
    metainfo = None
    if row:
        note = row[0] if row[0] is not None else ""
        if row[1] is not None:
            try:
                metainfo = json.loads(row[1])
            except json.JSONDecodeError:
                metainfo = None

    # 获取 tags
    cursor.execute("""
        SELECT tags.tag
        FROM tags
        JOIN link_tags ON tags.id = link_tags.tag_id
        JOIN links ON links.id = link_tags.link_id
        WHERE links.url = ?
    """, (url,))
    tags = [row[0] for row in cursor.fetchall()]  # 可能为空列表

    return [result_url, names, note, tags, metainfo]







def get_metainfo_by_url(url: str):
    """根据 URL 获取对应的 metainfo（返回字典，若不存在返回 None）"""
    cursor.execute("SELECT metainfo FROM links WHERE url = ?", (url,))
    row = cursor.fetchone()
    if not row or row[0] is None:
        return None
    try:
        return json.loads(row[0])
    except json.JSONDecodeError:
        return None

def update_metainfo_by_url(url: str, metainfo: dict) -> bool:
    """根据 URL 覆写对应的 metainfo，metainfo 为字典"""
    cursor.execute("SELECT id FROM links WHERE url = ?", (url,))
    if cursor.fetchone() is None:
        return False  # URL 不存在
    metainfo_json = json.dumps(metainfo, ensure_ascii=False)
    cursor.execute("UPDATE links SET metainfo = ? WHERE url = ?", (metainfo_json, url))
    conn.commit()
    return True





def search_all(keyword: str):
    """全局模糊搜索，返回匹配的 URL 及完整信息 + 匹配来源"""
    pattern = f"%{keyword}%"
    matches = {}  # {url: set(匹配字段)}

    # 搜 links 表
    cursor.execute("""
        SELECT url, note, metainfo FROM links
        WHERE url LIKE ? OR note LIKE ? OR metainfo LIKE ?
    """, (pattern, pattern, pattern))
    for url, note, metainfo in cursor.fetchall():
        if url not in matches:
            matches[url] = set()
        if keyword.lower() in url.lower():
            matches[url].add("url")
        if note and keyword.lower() in note.lower():
            matches[url].add("note")
        if metainfo and keyword.lower() in metainfo.lower():
            matches[url].add("metainfo")

    # 搜 tags
    cursor.execute("""
        SELECT links.url, tags.tag
        FROM links
        JOIN link_tags ON links.id = link_tags.link_id
        JOIN tags ON tags.id = link_tags.tag_id
        WHERE tags.tag LIKE ?
    """, (pattern,))
    for url, tag in cursor.fetchall():
        if url not in matches:
            matches[url] = set()
        matches[url].add("tag")

    # 搜 names
    cursor.execute("""
        SELECT links.url, names.name
        FROM links
        JOIN link_names ON links.id = link_names.link_id
        JOIN names ON names.id = link_names.name_id
        WHERE names.name LIKE ?
    """, (pattern,))
    for url, name in cursor.fetchall():
        if url not in matches:
            matches[url] = set()
        matches[url].add("name")

    # 拼装结果
    results = []
    for url, fields in matches.items():
        results.append({
            "info": get_info_by_url(url),  # [url, names, note, tags, metainfo]
            "matched_fields": list(fields) # ["url", "tag", ...]
        })
    return results







