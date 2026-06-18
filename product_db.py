import sqlite3
import datetime
from pathlib import Path

DB_PATH = "products.db"

def _dict_factory(cursor, row):
    """Return rows as dicts instead of tuples (much safer)."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = _dict_factory
    c = conn.cursor()

    # Base table (from original zip)
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            title TEXT,
            niche TEXT,
            status TEXT DEFAULT 'draft',
            created DATE,
            sales INT DEFAULT 0
        )
    ''')

    # Add new columns for Gumroad + profitability (idempotent)
    cols_to_add = [
        ("price_cents", "INTEGER DEFAULT 0"),
        ("revenue_cents", "INTEGER DEFAULT 0"),
        ("gumroad_id", "TEXT"),
        ("gumroad_url", "TEXT"),
        ("file_path", "TEXT"),
        ("last_synced", "DATE"),
    ]
    for col, typ in cols_to_add:
        try:
            c.execute(f"ALTER TABLE products ADD COLUMN {col} {typ}")
        except sqlite3.OperationalError:
            pass  # column already exists

    conn.commit()
    conn.close()

def log_product(title, niche, price_cents=990, file_path=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.date.today()
    c.execute("""
        INSERT INTO products 
        (title, niche, status, created, price_cents, sales, revenue_cents, file_path)
        VALUES (?, ?, 'generated', ?, ?, 0, 0, ?)
    """, (title, niche, today, price_cents, file_path))
    conn.commit()
    row_id = c.lastrowid
    conn.close()
    return row_id

def update_gumroad_info(product_id, gumroad_id, gumroad_url):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE products 
        SET gumroad_id = ?, gumroad_url = ?, status = 'live'
        WHERE id = ?
    """, (gumroad_id, gumroad_url, product_id))
    conn.commit()
    conn.close()

def update_sales(product_id, sales, revenue_cents):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE products 
        SET sales = ?, revenue_cents = ?, last_synced = ?
        WHERE id = ?
    """, (sales, revenue_cents, datetime.date.today(), product_id))
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = _dict_factory
    c = conn.cursor()
    c.execute("SELECT * FROM products ORDER BY created DESC, id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_live_products():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = _dict_factory
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE status IN ('live', 'generated') ORDER BY created DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_total_revenue():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = _dict_factory
    c = conn.cursor()
    try:
        c.execute("SELECT COALESCE(SUM(revenue_cents), 0) as total FROM products")
        row = c.fetchone()
        revenue = row["total"] if row else 0
    except sqlite3.OperationalError:
        revenue = 0
    conn.close()
    return revenue

# ==================== NEW TABLES FOR AUDIT IMPROVEMENTS ====================

def _ensure_run_history(c):
    c.execute('''
        CREATE TABLE IF NOT EXISTS run_history (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            topic TEXT,
            decision TEXT,           -- GO / NO-GO
            quality_score INTEGER,
            profit_score INTEGER,
            est_cost_cents INTEGER DEFAULT 0,
            product_id INTEGER,
            published BOOLEAN DEFAULT 0,
            gumroad_url TEXT,
            notes TEXT
        )
    ''')

def _ensure_niche_memory(c):
    c.execute('''
        CREATE TABLE IF NOT EXISTS niche_memory (
            niche TEXT PRIMARY KEY,
            attempts INTEGER DEFAULT 0,
            successes INTEGER DEFAULT 0,
            total_revenue_cents INTEGER DEFAULT 0,
            last_tried DATE,
            avg_quality REAL DEFAULT 0,
            avg_profit REAL DEFAULT 0
        )
    ''')

def log_run_history(topic, decision, quality=0, profit=0, est_cost_cents=0, product_id=None, published=False, gumroad_url=None, notes=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = _dict_factory
    c = conn.cursor()
    _ensure_run_history(c)
    c.execute('''
        INSERT INTO run_history (topic, decision, quality_score, profit_score, est_cost_cents, product_id, published, gumroad_url, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (topic, decision, quality, profit, est_cost_cents, product_id, 1 if published else 0, gumroad_url, notes))
    row_id = c.lastrowid
    conn.commit()
    conn.close()
    return row_id

def get_recent_runs(limit=20):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = _dict_factory
    c = conn.cursor()
    _ensure_run_history(c)
    c.execute("SELECT * FROM run_history ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def update_niche_memory(niche, success=False, revenue_cents=0, quality=0, profit=0):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = _dict_factory
    c = conn.cursor()
    _ensure_niche_memory(c)
    today = datetime.date.today().isoformat()
    c.execute('''
        INSERT INTO niche_memory (niche, attempts, successes, total_revenue_cents, last_tried, avg_quality, avg_profit)
        VALUES (?, 1, ?, ?, ?, ?, ?)
        ON CONFLICT(niche) DO UPDATE SET
            attempts = attempts + 1,
            successes = successes + ?,
            total_revenue_cents = total_revenue_cents + ?,
            last_tried = ?,
            avg_quality = (avg_quality * (attempts - 1) + ?) / attempts,
            avg_profit = (avg_profit * (attempts - 1) + ?) / attempts
    ''', (niche, 1 if success else 0, revenue_cents, today, quality, profit,
          1 if success else 0, revenue_cents, today, quality, profit))
    conn.commit()
    conn.close()

def get_niche_memory():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = _dict_factory
    c = conn.cursor()
    _ensure_niche_memory(c)
    c.execute("SELECT * FROM niche_memory ORDER BY total_revenue_cents DESC, attempts DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_best_niches(limit=5):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = _dict_factory
    c = conn.cursor()
    _ensure_niche_memory(c)
    c.execute("""
        SELECT niche FROM niche_memory 
        WHERE successes > 0 
        ORDER BY (total_revenue_cents * 1.0 / NULLIF(attempts,0)) DESC, avg_profit DESC 
        LIMIT ?
    """, (limit,))
    rows = [r["niche"] for r in c.fetchall()]
    conn.close()
    return rows

# Make sure new tables are created on every import
_conn = sqlite3.connect(DB_PATH)
_conn.row_factory = _dict_factory
_c = _conn.cursor()
_ensure_run_history(_c)
_ensure_niche_memory(_c)
_conn.commit()
_conn.close()
