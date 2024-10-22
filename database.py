import sqlite3

DB_PATH = 'db/rules.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule TEXT NOT NULL,
            ast TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_rule(rule, ast):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rules (rule, ast) VALUES (?, ?)', (rule, ast))
    conn.commit()
    conn.close()

def get_rules(rule_ids):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM rules WHERE id IN ({','.join('?' * len(rule_ids))})", rule_ids)
    rules = cursor.fetchall()
    conn.close()
    return [{'id': r[0], 'rule': r[1], 'ast': r[2]} for r in rules]
