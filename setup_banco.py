#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║   TechOS — Script de Criação de Tabelas no MySQL             ║
║   Execute este script UMA VEZ para preparar o banco.         ║
╚══════════════════════════════════════════════════════════════╝

Uso:
    python setup_banco.py

Dependências:
    pip install pymysql cryptography flask flask-sqlalchemy flask-cors
"""

import sys

# ── Verifica dependências ─────────────────────────────────────────────────────
def check_deps():
    missing = []
    for pkg in ['pymysql', 'flask', 'flask_sqlalchemy', 'flask_cors']:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg.replace('_','-'))
    if missing:
        print(f"❌ Pacotes faltando: {', '.join(missing)}")
        print(f"   Instale com: pip install {' '.join(missing)}")
        sys.exit(1)

check_deps()

import pymysql
from datetime import datetime

# ── CONFIGURAÇÕES ─────────────────────────────────────────────────────────────
CONFIG = {
    'host':     'easypanel.pontocomdesconto.com.br',
    'port':     3409,
    'user':     'mysql',
    'password': 'd95d2d9bcf70ab284a90',
    'database': 'os_sistem',
    'charset':  'utf8mb4',
    'connect_timeout': 15,
}

BANNER = """
  ╔══════════════════════════════════════╗
  ║   TechOS — Setup do Banco de Dados   ║
  ╚══════════════════════════════════════╝
"""

# ── SQL DAS TABELAS ───────────────────────────────────────────────────────────
TABLES = {}

TABLES['company'] = """
CREATE TABLE IF NOT EXISTS company (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    name             VARCHAR(200) NOT NULL,
    cnpj             VARCHAR(20),
    phone            VARCHAR(20),
    email            VARCHAR(100),
    address          VARCHAR(300),
    city             VARCHAR(100),
    state            VARCHAR(2),
    cep              VARCHAR(10),
    logo_url         VARCHAR(500),
    website          VARCHAR(200),
    insc_municipal   VARCHAR(50),
    insc_estadual    VARCHAR(50),
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

TABLES['client'] = """
CREATE TABLE IF NOT EXISTS client (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(200) NOT NULL,
    cnpj       VARCHAR(20),
    cpf        VARCHAR(15),
    phone      VARCHAR(20),
    email      VARCHAR(100),
    address    VARCHAR(300),
    city       VARCHAR(100),
    state      VARCHAR(2),
    cep        VARCHAR(10),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

TABLES['store'] = """
CREATE TABLE IF NOT EXISTS store (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    client_id      INT NOT NULL,
    name           VARCHAR(200) NOT NULL,
    cnpj           VARCHAR(20),
    phone          VARCHAR(20),
    address        VARCHAR(300),
    city           VARCHAR(100),
    state          VARCHAR(2),
    cep            VARCHAR(10),
    manager_name   VARCHAR(200),
    manager_phone  VARCHAR(20),
    manager_email  VARCHAR(100),
    created_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_store_client FOREIGN KEY (client_id)
        REFERENCES client(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

TABLES['equipment'] = """
CREATE TABLE IF NOT EXISTS equipment (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    store_id         INT NOT NULL,
    name             VARCHAR(200) NOT NULL,
    serial_number    VARCHAR(100),
    equipment_type   VARCHAR(100),
    brand            VARCHAR(100),
    model            VARCHAR(100),
    current_seal     VARCHAR(100),
    previous_seal    VARCHAR(100),
    current_label    VARCHAR(100),
    previous_label   VARCHAR(100),
    max_load         VARCHAR(50),
    portaria         VARCHAR(50),
    mict             VARCHAR(50),
    active           TINYINT(1) DEFAULT 1,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_equipment_store FOREIGN KEY (store_id)
        REFERENCES store(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

TABLES['technician'] = """
CREATE TABLE IF NOT EXISTS technician (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(200) NOT NULL,
    phone      VARCHAR(20),
    email      VARCHAR(100),
    address    VARCHAR(300),
    city       VARCHAR(100),
    state      VARCHAR(2),
    rg         VARCHAR(20),
    cpf        VARCHAR(15),
    active     TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

TABLES['service_order'] = """
CREATE TABLE IF NOT EXISTS service_order (
    id                   INT AUTO_INCREMENT PRIMARY KEY,
    os_number            VARCHAR(20) UNIQUE,
    store_id             INT NOT NULL,
    equipment_id         INT NOT NULL,
    technician_id        INT NOT NULL,

    -- Dados do chamado
    call_date            VARCHAR(20),
    call_time            VARCHAR(10),
    call_type            VARCHAR(100),

    -- Dados do atendimento
    service_date         VARCHAR(20),
    start_time           VARCHAR(10),
    end_time             VARCHAR(10),
    travel_time          VARCHAR(20),

    -- Ocorrência
    symptom              TEXT,
    services_description TEXT,
    actions              TEXT,
    codes                TEXT,

    -- Status
    status               VARCHAR(50) DEFAULT 'Aberta',
    final_status         VARCHAR(100),

    -- Financeiro
    parts_value          DECIMAL(10,2) DEFAULT 0.00,
    services_value       DECIMAL(10,2) DEFAULT 0.00,
    expenses_value       DECIMAL(10,2) DEFAULT 0.00,
    discount             DECIMAL(10,2) DEFAULT 0.00,
    total_value          DECIMAL(10,2) DEFAULT 0.00,

    -- Assinatura
    signer_name          VARCHAR(200),
    signer_role          VARCHAR(100),
    client_signature     LONGTEXT,
    tech_signature       LONGTEXT,
    signed_at            DATETIME,

    -- Observações
    notes                TEXT,

    created_at           DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at           DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_os_store      FOREIGN KEY (store_id)      REFERENCES store(id),
    CONSTRAINT fk_os_equipment  FOREIGN KEY (equipment_id)  REFERENCES equipment(id),
    CONSTRAINT fk_os_technician FOREIGN KEY (technician_id) REFERENCES technician(id),

    INDEX idx_os_service_date (service_date),
    INDEX idx_os_status       (status),
    INDEX idx_os_store        (store_id),
    INDEX idx_os_technician   (technician_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# Ordem respeitando foreign keys
TABLE_ORDER = ['company', 'client', 'store', 'equipment', 'technician', 'service_order']

# ── DADOS INICIAIS (opcional) ─────────────────────────────────────────────────
SEED_COMPANY = """
INSERT INTO company (name, cnpj, phone, email, address, city, state, cep, website, insc_municipal, insc_estadual)
SELECT
    'Rematec Serviços Ltda',
    '04.645.382/0001-61',
    '(31) 3360-1900',
    'sac@rematecvarejo.com.br',
    'Rua Santa Catarina, 587 - Lojas 01 e 02 - Lourdes',
    'Belo Horizonte',
    'MG',
    '30170-081',
    'www.rematecvarejo.com.br',
    '022.0016/001-4',
    'IST.022.708.400.00.54'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM company LIMIT 1);
"""

# ── FUNÇÕES ───────────────────────────────────────────────────────────────────
def connect():
    print(f"\n🔌 Conectando em {CONFIG['host']}:{CONFIG['port']} ...")
    try:
        conn = pymysql.connect(**CONFIG)
        print("✅ Conexão estabelecida!")
        return conn
    except Exception as e:
        print(f"❌ Falha na conexão: {e}")
        sys.exit(1)

def check_existing_tables(cursor):
    cursor.execute("SHOW TABLES;")
    existing = {row[0] for row in cursor.fetchall()}
    return existing

def create_tables(conn):
    cursor = conn.cursor()
    existing = check_existing_tables(cursor)

    print(f"\n📋 Tabelas existentes no banco: {existing if existing else 'nenhuma'}")
    print("\n🏗️  Criando tabelas...\n")

    created = []
    skipped = []

    for name in TABLE_ORDER:
        sql = TABLES[name]
        try:
            cursor.execute(sql)
            conn.commit()
            if name in existing:
                skipped.append(name)
                print(f"   ⏭  {name:20s} — já existia (sem alterações)")
            else:
                created.append(name)
                print(f"   ✅ {name:20s} — criada com sucesso")
        except Exception as e:
            print(f"   ❌ {name:20s} — ERRO: {e}")
            conn.rollback()

    return created, skipped

def seed_data(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM company;")
        (count,) = cursor.fetchone()
        if count == 0:
            cursor.execute(SEED_COMPANY)
            conn.commit()
            print("\n🌱 Dados iniciais inseridos (empresa demo)")
        else:
            print("\n🌱 Dados iniciais já existem, pulando seed")
    except Exception as e:
        print(f"\n⚠️  Seed ignorado: {e}")

def verify_tables(conn):
    cursor = conn.cursor()
    print("\n🔍 Verificação final:\n")
    for name in TABLE_ORDER:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM `{name}`;")
            (count,) = cursor.fetchone()
            print(f"   ✅ {name:20s} — {count} registro(s)")
        except Exception as e:
            print(f"   ❌ {name:20s} — {e}")

def show_structure(conn):
    cursor = conn.cursor()
    print("\n📐 Estrutura das tabelas:\n")
    for name in TABLE_ORDER:
        try:
            cursor.execute(f"DESCRIBE `{name}`;")
            rows = cursor.fetchall()
            print(f"  ┌─ {name} ({'─'*40}")
            for row in rows:
                col, typ, null, key, default, extra = row
                key_mark = f" [{key}]" if key else ""
                print(f"  │  {col:25s} {typ:30s}{key_mark}")
            print()
        except Exception as e:
            print(f"  ❌ {name}: {e}")

# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print(BANNER)

    conn = connect()

    try:
        created, skipped = create_tables(conn)
        seed_data(conn)
        verify_tables(conn)

        # Pergunta se quer ver estrutura detalhada
        try:
            resp = input("\n📐 Mostrar estrutura detalhada das tabelas? (s/N): ").strip().lower()
            if resp == 's':
                show_structure(conn)
        except (EOFError, KeyboardInterrupt):
            pass

        print("\n" + "═"*52)
        print(f"  🎉 Setup concluído!")
        print(f"  📦 Tabelas criadas : {len(created)}")
        print(f"  ⏭  Já existiam    : {len(skipped)}")
        print("═"*52)
        print("\n  Agora execute: python app.py")
        print("  Acesse:        http://localhost:5000\n")

    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback; traceback.print_exc()
    finally:
        conn.close()
