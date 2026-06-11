#!/usr/bin/env python3
"""
TechOS — Migração v2: Login + Solicitação de Peças
Adiciona tabelas: user, parts_request, parts_request_item
Corrige colunas existentes para tamanhos maiores
"""
import sys
try: import pymysql
except ImportError: print("pip install pymysql"); sys.exit(1)

CONFIG = dict(host='2.25.131.174',port=3409,user='mysql',
              password='d95d2d9bcf70ab284a90',database='os_sistem',charset='utf8mb4',connect_timeout=15)

NEW_COLS = [
    # tabela, coluna, tipo, after
    ('company','smtp_host',    'VARCHAR(100)',  'insc_estadual'),
    ('company','smtp_port',    'INT DEFAULT 587','smtp_host'),
    ('company','smtp_user',    'VARCHAR(150)',  'smtp_port'),
    ('company','smtp_password','VARCHAR(200)',  'smtp_user'),
    ('company','smtp_from',    'VARCHAR(150)',  'smtp_password'),
    ('company','parts_email',  'VARCHAR(300)',  'smtp_from'),
]

FIX_COLS = [
    ('client','cnpj','VARCHAR(30)'),('client','cpf','VARCHAR(30)'),('client','phone','VARCHAR(30)'),
    ('client','email','VARCHAR(150)'),('client','state','VARCHAR(50)'),('client','cep','VARCHAR(15)'),
    ('store','cnpj','VARCHAR(30)'),('store','phone','VARCHAR(30)'),('store','state','VARCHAR(50)'),
    ('store','cep','VARCHAR(15)'),('store','manager_phone','VARCHAR(30)'),('store','manager_email','VARCHAR(150)'),
    ('technician','phone','VARCHAR(30)'),('technician','email','VARCHAR(150)'),('technician','state','VARCHAR(50)'),
    ('technician','rg','VARCHAR(30)'),('technician','cpf','VARCHAR(30)'),
    ('company','phone','VARCHAR(30)'),('company','state','VARCHAR(50)'),('company','cep','VARCHAR(15)'),
]

NEW_TABLES = {}

NEW_TABLES['user'] = """
CREATE TABLE IF NOT EXISTS `user` (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(200) NOT NULL,
    username      VARCHAR(100) NOT NULL UNIQUE,
    email         VARCHAR(150) UNIQUE,
    password_hash VARCHAR(256),
    role          VARCHAR(20) DEFAULT 'technician',
    technician_id INT NULL,
    store_id      INT NULL,
    first_login   TINYINT(1) DEFAULT 1,
    active        TINYINT(1) DEFAULT 1,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_tech  FOREIGN KEY (technician_id) REFERENCES technician(id) ON DELETE SET NULL,
    CONSTRAINT fk_user_store FOREIGN KEY (store_id)      REFERENCES store(id)      ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

NEW_TABLES['parts_request'] = """
CREATE TABLE IF NOT EXISTS parts_request (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    request_number VARCHAR(20) UNIQUE,
    technician_id  INT NOT NULL,
    store_id       INT NULL,
    equipment_id   INT NULL,
    os_id          INT NULL,
    status         VARCHAR(30) DEFAULT 'Pendente',
    urgency        VARCHAR(20) DEFAULT 'Normal',
    notes          TEXT,
    email_sent     TINYINT(1) DEFAULT 0,
    email_sent_at  DATETIME,
    created_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_pr_tech  FOREIGN KEY (technician_id) REFERENCES technician(id),
    CONSTRAINT fk_pr_store FOREIGN KEY (store_id)      REFERENCES store(id) ON DELETE SET NULL,
    CONSTRAINT fk_pr_equip FOREIGN KEY (equipment_id)  REFERENCES equipment(id) ON DELETE SET NULL,
    CONSTRAINT fk_pr_os    FOREIGN KEY (os_id)         REFERENCES service_order(id) ON DELETE SET NULL,
    INDEX idx_pr_tech   (technician_id),
    INDEX idx_pr_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

NEW_TABLES['parts_request_item'] = """
CREATE TABLE IF NOT EXISTS parts_request_item (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    request_id  INT NOT NULL,
    code        VARCHAR(50),
    description VARCHAR(300) NOT NULL,
    quantity    FLOAT DEFAULT 1,
    unit        VARCHAR(20) DEFAULT 'un',
    notes       VARCHAR(300),
    CONSTRAINT fk_pri_req FOREIGN KEY (request_id) REFERENCES parts_request(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

TABLE_ORDER = ['user','parts_request','parts_request_item']

# Default admin seed
SEED_ADMIN = """
INSERT INTO `user` (name, username, email, password_hash, role, first_login, active)
SELECT 'Administrador', 'admin', 'admin@techos.local',
       'scrypt:32768:8:1$placeholder$hash',  -- will be replaced by app
       'admin', 1, 1
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM `user` WHERE role='admin' LIMIT 1);
"""

def col_exists(cur, table, col):
    cur.execute("SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_NAME=%s",
                (CONFIG['database'],table,col))
    return cur.fetchone()[0]>0

def col_type(cur, table, col):
    cur.execute("SELECT COLUMN_TYPE FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_NAME=%s",
                (CONFIG['database'],table,col))
    r=cur.fetchone()
    return r[0].upper() if r else None

def table_exists(cur, table):
    cur.execute("SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                (CONFIG['database'],table))
    return cur.fetchone()[0]>0

if __name__=='__main__':
    print("\n  ╔══════════════════════════════════════╗")
    print("  ║   TechOS — Migração v2               ║")
    print("  ╚══════════════════════════════════════╝\n")
    try:
        conn=pymysql.connect(**CONFIG)
        print(f"✅ Conectado em {CONFIG['host']}:{CONFIG['port']}\n")
    except Exception as e:
        print(f"❌ Falha: {e}"); sys.exit(1)

    cur=conn.cursor()
    ok=skip=err=0

    # 1. Fix existing column sizes
    print("🔧 Corrigindo tamanho de colunas existentes...")
    for table,col,ntype in FIX_COLS:
        if not table_exists(cur,table): continue
        cur_type=col_type(cur,table,col)
        if not cur_type: continue
        if cur_type==ntype.upper(): skip+=1; continue
        try:
            cur.execute(f"ALTER TABLE `{table}` MODIFY COLUMN `{col}` {ntype};")
            conn.commit(); ok+=1
            print(f"  ✅ {table}.{col}: {cur_type} → {ntype}")
        except Exception as e:
            conn.rollback(); err+=1
            print(f"  ❌ {table}.{col}: {e}")

    # 2. Add new columns to company (SMTP)
    print("\n📧 Adicionando colunas de email à empresa...")
    for table,col,ntype,after in NEW_COLS:
        if not table_exists(cur,table): continue
        if col_exists(cur,table,col):
            print(f"  ⏭ {table}.{col} — já existe"); skip+=1; continue
        try:
            cur.execute(f"ALTER TABLE `{table}` ADD COLUMN `{col}` {ntype} AFTER `{after}`;")
            conn.commit(); ok+=1
            print(f"  ✅ {table}.{col} — adicionado")
        except Exception as e:
            conn.rollback(); err+=1
            print(f"  ❌ {table}.{col}: {e}")

    # 3. Create new tables
    print("\n🏗️  Criando novas tabelas...")
    for name in TABLE_ORDER:
        if table_exists(cur,name):
            print(f"  ⏭ {name:25s} — já existe"); skip+=1; continue
        try:
            cur.execute(NEW_TABLES[name]); conn.commit(); ok+=1
            print(f"  ✅ {name:25s} — criada")
        except Exception as e:
            conn.rollback(); err+=1
            print(f"  ❌ {name:25s}: {e}")

    # 4. Verify counts
    print("\n🔍 Verificação:")
    for t in ['company','client','store','equipment','technician','service_order','user','parts_request','parts_request_item']:
        if table_exists(cur,t):
            cur.execute(f"SELECT COUNT(*) FROM `{t}`;")
            print(f"  ✅ {t:30s}: {cur.fetchone()[0]} registros")
        else:
            print(f"  ❌ {t} — não encontrada")

    conn.close()
    print(f"\n{'='*50}")
    print(f"  ✅ OK: {ok}  ⏭ Ignorados: {skip}  ❌ Erros: {err}")
    print(f"{'='*50}")
    if err==0:
        print("\n  🎉 Migração concluída! Execute: python app.py\n")
        print("  🔑 Login padrão: usuário=admin | senha=admin123")
        print("  ⚠️  O admin criado pelo app.py terá senha funcional.\n")
    else:
        print("\n  ⚠️  Verifique os erros acima.\n")
