#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║   TechOS — Setup DEFINITIVO do Banco de Dados                    ║
║                                                                  ║
║   Cria todas as tabelas necessárias do zero.                     ║
║   Seguro para rodar múltiplas vezes (IF NOT EXISTS).             ║
║                                                                  ║
║   Uso:  python setup_banco.py                                    ║
║                                                                  ║
║   Dependências:  pip install pymysql cryptography                ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys

# ── Verifica dependências ──────────────────────────────────────────────────────
def check_deps():
    missing = []
    for pkg in ['pymysql', 'cryptography']:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"❌ Pacotes faltando: {', '.join(missing)}")
        print(f"   Instale com: pip install {' '.join(missing)}")
        sys.exit(1)

check_deps()
import pymysql

# ── CONFIGURAÇÃO DO BANCO ──────────────────────────────────────────────────────
CONFIG = {
    'host':            '2.25.131.174',
    'port':            3409,
    'user':            'mysql',
    'password':        'ea7cz6o5czxsv77g8gsg',
    'database':        'os_sistem',
    'charset':         'utf8mb4',
    'connect_timeout': 15,
}

# ── DDL DAS TABELAS (ordem respeita FK) ───────────────────────────────────────

# 1 ─ EMPRESA (prestadora de serviços)
SQL_COMPANY = """
CREATE TABLE IF NOT EXISTS `company` (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    name             VARCHAR(200)  NOT NULL,
    cnpj             VARCHAR(30),
    phone            VARCHAR(30),
    email            VARCHAR(150),
    address          VARCHAR(300),
    city             VARCHAR(100),
    state            VARCHAR(50),
    cep              VARCHAR(15),
    logo_url         VARCHAR(500),
    website          VARCHAR(200),
    insc_municipal   VARCHAR(50),
    insc_estadual    VARCHAR(50),
    smtp_host        VARCHAR(100),
    smtp_port        INT           DEFAULT 587,
    smtp_user        VARCHAR(150),
    smtp_password    VARCHAR(200),
    smtp_from        VARCHAR(150),
    parts_email      VARCHAR(300),
    created_at       DATETIME      DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# 2 ─ CLIENTES (empresas contratantes)
SQL_CLIENT = """
CREATE TABLE IF NOT EXISTS `client` (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(200) NOT NULL,
    cnpj       VARCHAR(30),
    cpf        VARCHAR(30),
    phone      VARCHAR(30),
    email      VARCHAR(150),
    address    VARCHAR(300),
    city       VARCHAR(100),
    state      VARCHAR(50),
    cep        VARCHAR(15),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# 3 ─ LOJAS (unidades dos clientes)
SQL_STORE = """
CREATE TABLE IF NOT EXISTS `store` (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    client_id      INT          NOT NULL,
    name           VARCHAR(200) NOT NULL,
    cnpj           VARCHAR(30),
    phone          VARCHAR(30),
    address        VARCHAR(300),
    city           VARCHAR(100),
    state          VARCHAR(50),
    cep            VARCHAR(15),
    manager_name   VARCHAR(200),
    manager_phone  VARCHAR(30),
    manager_email  VARCHAR(150),
    created_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_store_client FOREIGN KEY (client_id)
        REFERENCES `client`(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# 4 ─ TÉCNICOS
SQL_TECHNICIAN = """
CREATE TABLE IF NOT EXISTS `technician` (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(200) NOT NULL,
    phone      VARCHAR(30),
    email      VARCHAR(150),
    address    VARCHAR(300),
    city       VARCHAR(100),
    state      VARCHAR(50),
    rg         VARCHAR(30),
    cpf        VARCHAR(30),
    active     TINYINT(1)   DEFAULT 1,
    created_at DATETIME     DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# 5 ─ EQUIPAMENTOS (por loja)
SQL_EQUIPMENT = """
CREATE TABLE IF NOT EXISTS `equipment` (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    store_id         INT          NOT NULL,
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
    active           TINYINT(1)   DEFAULT 1,
    created_at       DATETIME     DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_equipment_store FOREIGN KEY (store_id)
        REFERENCES `store`(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# 6 ─ ORDENS DE SERVIÇO
SQL_SERVICE_ORDER = """
CREATE TABLE IF NOT EXISTS `service_order` (
    id                   INT AUTO_INCREMENT PRIMARY KEY,
    os_number            VARCHAR(20)     UNIQUE,
    store_id             INT             NOT NULL,
    equipment_id         INT             NOT NULL,
    technician_id        INT             NOT NULL,
    call_date            VARCHAR(20),
    call_time            VARCHAR(10),
    call_type            VARCHAR(100),
    service_date         VARCHAR(20),
    start_time           VARCHAR(10),
    end_time             VARCHAR(10),
    travel_time          VARCHAR(20),
    symptom              TEXT,
    services_description TEXT,
    actions              TEXT,
    codes                TEXT,
    status               VARCHAR(50)     DEFAULT 'Aberta',
    final_status         VARCHAR(100),
    parts_value          DECIMAL(10,2)   DEFAULT 0.00,
    services_value       DECIMAL(10,2)   DEFAULT 0.00,
    expenses_value       DECIMAL(10,2)   DEFAULT 0.00,
    discount             DECIMAL(10,2)   DEFAULT 0.00,
    total_value          DECIMAL(10,2)   DEFAULT 0.00,
    signer_name          VARCHAR(200),
    signer_role          VARCHAR(100),
    client_signature     LONGTEXT,
    tech_signature       LONGTEXT,
    signed_at            DATETIME,
    notes                TEXT,
    created_at           DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at           DATETIME        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_os_store      FOREIGN KEY (store_id)      REFERENCES `store`(id),
    CONSTRAINT fk_os_equipment  FOREIGN KEY (equipment_id)  REFERENCES `equipment`(id),
    CONSTRAINT fk_os_technician FOREIGN KEY (technician_id) REFERENCES `technician`(id),
    INDEX idx_os_service_date (service_date),
    INDEX idx_os_status       (status),
    INDEX idx_os_store        (store_id),
    INDEX idx_os_technician   (technician_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# 7 ─ USUÁRIOS DO SISTEMA (login)
SQL_USER = """
CREATE TABLE IF NOT EXISTS `user` (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(200) NOT NULL,
    username      VARCHAR(100) NOT NULL UNIQUE,
    email         VARCHAR(150) UNIQUE,
    password_hash VARCHAR(256),
    role          VARCHAR(20)  DEFAULT 'technician',
    technician_id INT          NULL,
    store_id      INT          NULL,
    first_login   TINYINT(1)   DEFAULT 1,
    active        TINYINT(1)   DEFAULT 1,
    created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_tech  FOREIGN KEY (technician_id)
        REFERENCES `technician`(id) ON DELETE SET NULL,
    CONSTRAINT fk_user_store FOREIGN KEY (store_id)
        REFERENCES `store`(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# 8 ─ SOLICITAÇÕES DE PEÇAS
SQL_PARTS_REQUEST = """
CREATE TABLE IF NOT EXISTS `parts_request` (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    request_number VARCHAR(20)  UNIQUE,
    technician_id  INT          NOT NULL,
    store_id       INT          NULL,
    equipment_id   INT          NULL,
    os_id          INT          NULL,
    status         VARCHAR(30)  DEFAULT 'Pendente',
    urgency        VARCHAR(20)  DEFAULT 'Normal',
    notes          TEXT,
    email_sent     TINYINT(1)   DEFAULT 0,
    email_sent_at  DATETIME,
    created_at     DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_pr_tech  FOREIGN KEY (technician_id)
        REFERENCES `technician`(id),
    CONSTRAINT fk_pr_store FOREIGN KEY (store_id)
        REFERENCES `store`(id) ON DELETE SET NULL,
    CONSTRAINT fk_pr_equip FOREIGN KEY (equipment_id)
        REFERENCES `equipment`(id) ON DELETE SET NULL,
    CONSTRAINT fk_pr_os    FOREIGN KEY (os_id)
        REFERENCES `service_order`(id) ON DELETE SET NULL,
    INDEX idx_pr_tech   (technician_id),
    INDEX idx_pr_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# 9 ─ ITENS DAS SOLICITAÇÕES DE PEÇAS
SQL_PARTS_REQUEST_ITEM = """
CREATE TABLE IF NOT EXISTS `parts_request_item` (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    request_id  INT          NOT NULL,
    code        VARCHAR(50),
    description VARCHAR(300) NOT NULL,
    quantity    FLOAT        DEFAULT 1,
    unit        VARCHAR(20)  DEFAULT 'un',
    notes       VARCHAR(300),
    CONSTRAINT fk_pri_req FOREIGN KEY (request_id)
        REFERENCES `parts_request`(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# ── TABELAS na ordem correta (respeita FK) ────────────────────────────────────
TABLES = [
    ('company',            SQL_COMPANY),
    ('client',             SQL_CLIENT),
    ('store',              SQL_STORE),
    ('technician',         SQL_TECHNICIAN),
    ('equipment',          SQL_EQUIPMENT),
    ('service_order',      SQL_SERVICE_ORDER),
    ('user',               SQL_USER),
    ('parts_request',      SQL_PARTS_REQUEST),
    ('parts_request_item', SQL_PARTS_REQUEST_ITEM),
]

# ── MIGRAÇÕES: garante colunas extras em tabelas já existentes ────────────────
# Executadas com IF NOT EXISTS lógico (verifica antes de alterar)
EXTRA_COLS = [
    # (tabela, coluna, DDL da coluna, coluna AFTER)
    ('company', 'smtp_host',     'VARCHAR(100)',  'insc_estadual'),
    ('company', 'smtp_port',     'INT DEFAULT 587','smtp_host'),
    ('company', 'smtp_user',     'VARCHAR(150)',  'smtp_port'),
    ('company', 'smtp_password', 'VARCHAR(200)',  'smtp_user'),
    ('company', 'smtp_from',     'VARCHAR(150)',  'smtp_password'),
    ('company', 'parts_email',   'VARCHAR(300)',  'smtp_from'),
]

# ── ADMIN PADRÃO (seed) ───────────────────────────────────────────────────────
# Senha: admin123  — hash gerado pelo werkzeug (mesmo padrão do app.py)
ADMIN_SEED_CHECK = "SELECT COUNT(*) FROM `user` WHERE role = 'admin'"
ADMIN_SEED_INSERT = """
INSERT INTO `user`
    (name, username, email, password_hash, role, first_login, active)
VALUES
    ('Administrador', 'admin', 'admin@techos.local',
     'pbkdf2:sha256:600000$techos2026$c3c1b5b9a2f4e8d0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4',
     'admin', 1, 1)
"""
# Nota: a senha real (admin123) será definida pelo app.py na inicialização.
# O hash acima é apenas placeholder; o app.py cria o admin correto se não existir.

COMPANY_SEED_CHECK  = "SELECT COUNT(*) FROM `company`"
COMPANY_SEED_INSERT = """
INSERT INTO `company` (name, phone, city, state)
VALUES ('Minha Empresa', '', '', '')
"""


# ── HELPERS ───────────────────────────────────────────────────────────────────
def col_exists(cur, table: str, col: str) -> bool:
    cur.execute(
        "SELECT COUNT(*) FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s",
        (CONFIG['database'], table, col)
    )
    return cur.fetchone()[0] > 0


def table_exists(cur, table: str) -> bool:
    cur.execute(
        "SELECT COUNT(*) FROM information_schema.TABLES "
        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s",
        (CONFIG['database'], table)
    )
    return cur.fetchone()[0] > 0


def connect():
    print(f"\n🔌 Conectando em {CONFIG['host']}:{CONFIG['port']} / {CONFIG['database']} ...")
    try:
        conn = pymysql.connect(**CONFIG)
        cur  = conn.cursor()
        cur.execute("SELECT VERSION()")
        ver = cur.fetchone()[0]
        print(f"✅ Conectado! MySQL {ver}\n")
        return conn
    except Exception as e:
        print(f"❌ Falha na conexão: {e}")
        print("\n   Verifique:")
        print("   • IP/host correto e acessível")
        print("   • Porta aberta no firewall")
        print("   • Credenciais válidas")
        sys.exit(1)


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("""
  ╔══════════════════════════════════════════════════╗
  ║   TechOS — Setup Definitivo do Banco de Dados    ║
  ║   mysql://mysql:***@2.25.131.174:3409/os_sistem  ║
  ╚══════════════════════════════════════════════════╝
""")

    conn = connect()
    cur  = conn.cursor()
    ok = skip = err = 0

    # ── 1. Criar tabelas ──────────────────────────────────────────────────────
    print("🏗️  Criando tabelas...\n")
    for name, sql in TABLES:
        already = table_exists(cur, name)
        try:
            cur.execute(sql)
            conn.commit()
            if already:
                print(f"  ⏭  {name:25s} já existia  (estrutura mantida)")
                skip += 1
            else:
                print(f"  ✅ {name:25s} criada com sucesso")
                ok += 1
        except Exception as e:
            conn.rollback()
            print(f"  ❌ {name:25s} ERRO: {e}")
            err += 1

    # ── 2. Adicionar colunas extras (migration) ───────────────────────────────
    print("\n🔧 Verificando colunas extras (SMTP, etc.)...\n")
    for table, col, typedef, after in EXTRA_COLS:
        if not table_exists(cur, table):
            continue
        if col_exists(cur, table, col):
            print(f"  ⏭  {table}.{col:20s} já existe")
            skip += 1
        else:
            try:
                cur.execute(
                    f"ALTER TABLE `{table}` ADD COLUMN `{col}` {typedef} AFTER `{after}`"
                )
                conn.commit()
                print(f"  ✅ {table}.{col:20s} adicionada")
                ok += 1
            except Exception as e:
                conn.rollback()
                print(f"  ❌ {table}.{col:20s} ERRO: {e}")
                err += 1

    # ── 3. Seed: empresa padrão ───────────────────────────────────────────────
    print("\n🌱 Seed de dados iniciais...\n")
    try:
        cur.execute(COMPANY_SEED_CHECK)
        if cur.fetchone()[0] == 0:
            cur.execute(COMPANY_SEED_INSERT)
            conn.commit()
            print("  ✅ Empresa padrão inserida")
        else:
            print("  ⏭  Empresa já cadastrada")
    except Exception as e:
        print(f"  ⚠️  Seed empresa: {e}")

    # ── 4. Contagem final ─────────────────────────────────────────────────────
    print("\n🔍 Verificação final:\n")
    all_good = True
    for name, _ in TABLES:
        if table_exists(cur, name):
            cur.execute(f"SELECT COUNT(*) FROM `{name}`")
            cnt = cur.fetchone()[0]
            print(f"  ✅ {name:25s} {cnt:>6} registro(s)")
        else:
            print(f"  ❌ {name:25s} NÃO ENCONTRADA")
            all_good = False

    conn.close()

    # ── Resumo ────────────────────────────────────────────────────────────────
    print(f"\n{'═'*52}")
    print(f"  ✅ Criados / alterados : {ok}")
    print(f"  ⏭  Sem alteração       : {skip}")
    print(f"  ❌ Erros               : {err}")
    print(f"{'═'*52}")

    if err == 0 and all_good:
        print("""
  🎉 Setup concluído com sucesso!

  Próximos passos:
    1. python app.py           (desenvolvimento)
       ou
       gunicorn app:app        (produção)

  Login padrão criado pelo app na 1ª inicialização:
    usuário : admin
    senha   : admin123
    ⚠️  Troque a senha após o primeiro acesso!
""")
    else:
        print("\n  ⚠️  Setup finalizado com erros. Verifique acima.\n")
        sys.exit(1)


if __name__ == '__main__':
    main()