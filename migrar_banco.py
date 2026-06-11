#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║   TechOS — Migração: Correção de Tamanho de Colunas              ║
║                                                                  ║
║   Corrige o erro:                                                ║
║   DataError: (1406, "Data too long for column 'cpf' at row 1")  ║
║                                                                  ║
║   Execute com:  python migrar_banco.py                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys

try:
    import pymysql
except ImportError:
    print("❌ pymysql não instalado. Execute: pip install pymysql")
    sys.exit(1)

CONFIG = {
    'host':     '2.25.131.174',
    'port':     3409,
    'user':     'mysql',
    'password': 'd95d2d9bcf70ab284a90',
    'database': 'os_sistem',
    'charset':  'utf8mb4',
    'connect_timeout': 15,
}

# ── Migrações: (tabela, coluna, novo_tipo) ────────────────────────────────────
# Motivo de cada mudança:
#   cpf  VARCHAR(15) → VARCHAR(30)  → CPF tem 14 chars, CNPJ tem 18; margem extra
#   phone VARCHAR(20) → VARCHAR(30) → telefones com DDI ficam maiores
#   state VARCHAR(2)  → VARCHAR(50) → evitar truncar nome de estado por extenso
#   cep   VARCHAR(10) → VARCHAR(15) → CEP formatado + margem
#   email VARCHAR(100)→ VARCHAR(150)→ emails longos
#   rg    VARCHAR(20) → VARCHAR(30) → RG com órgão emissor
MIGRATIONS = [
    # ── client ──────────────────────────────────────────
    ("client", "cnpj",    "VARCHAR(30)"),
    ("client", "cpf",     "VARCHAR(30)"),
    ("client", "phone",   "VARCHAR(30)"),
    ("client", "email",   "VARCHAR(150)"),
    ("client", "state",   "VARCHAR(50)"),
    ("client", "cep",     "VARCHAR(15)"),

    # ── store ────────────────────────────────────────────
    ("store",  "cnpj",          "VARCHAR(30)"),
    ("store",  "phone",         "VARCHAR(30)"),
    ("store",  "state",         "VARCHAR(50)"),
    ("store",  "cep",           "VARCHAR(15)"),
    ("store",  "manager_phone", "VARCHAR(30)"),
    ("store",  "manager_email", "VARCHAR(150)"),

    # ── technician ───────────────────────────────────────
    ("technician", "phone", "VARCHAR(30)"),
    ("technician", "email", "VARCHAR(150)"),
    ("technician", "state", "VARCHAR(50)"),
    ("technician", "rg",    "VARCHAR(30)"),
    ("technician", "cpf",   "VARCHAR(30)"),

    # ── company ──────────────────────────────────────────
    ("company", "phone", "VARCHAR(30)"),
    ("company", "email", "VARCHAR(150)"),
    ("company", "state", "VARCHAR(50)"),
    ("company", "cep",   "VARCHAR(15)"),
]

def connect():
    print(f"\n🔌 Conectando em {CONFIG['host']}:{CONFIG['port']}...")
    try:
        conn = pymysql.connect(**CONFIG)
        print("✅ Conexão OK\n")
        return conn
    except Exception as e:
        print(f"❌ Falha: {e}")
        sys.exit(1)

def get_current_type(cursor, table, column):
    """Retorna o tipo atual da coluna no banco."""
    cursor.execute(f"""
        SELECT COLUMN_TYPE
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = %s
          AND TABLE_NAME   = %s
          AND COLUMN_NAME  = %s
    """, (CONFIG['database'], table, column))
    row = cursor.fetchone()
    return row[0].upper() if row else None

def run_migrations(conn):
    cursor = conn.cursor()
    ok, skipped, failed = [], [], []

    print("🔧 Aplicando migrações...\n")
    print(f"  {'Tabela':<15} {'Coluna':<20} {'Antes':<20} {'Depois':<20} Status")
    print(f"  {'─'*15} {'─'*20} {'─'*20} {'─'*20} {'─'*10}")

    for table, column, new_type in MIGRATIONS:
        current = get_current_type(cursor, table, column)
        if current is None:
            print(f"  {table:<15} {column:<20} {'N/A':<20} {new_type:<20} ⚠️ col. não existe")
            skipped.append((table, column))
            continue

        # Se o tamanho já é suficiente, pular
        if current == new_type.upper():
            print(f"  {table:<15} {column:<20} {current:<20} {new_type:<20} ⏭ sem mudança")
            skipped.append((table, column))
            continue

        try:
            sql = f"ALTER TABLE `{table}` MODIFY COLUMN `{column}` {new_type};"
            cursor.execute(sql)
            conn.commit()
            print(f"  {table:<15} {column:<20} {current:<20} {new_type:<20} ✅ migrado")
            ok.append((table, column))
        except Exception as e:
            conn.rollback()
            print(f"  {table:<15} {column:<20} {current:<20} {new_type:<20} ❌ {e}")
            failed.append((table, column, str(e)))

    return ok, skipped, failed

def verify(conn):
    """Verifica se as colunas críticas têm o tamanho correto."""
    cursor = conn.cursor()
    print("\n🔍 Verificação pós-migração:\n")
    all_ok = True
    for table, column, expected in MIGRATIONS:
        current = get_current_type(cursor, table, column)
        if current and current == expected.upper():
            print(f"  ✅ {table}.{column} = {current}")
        elif current:
            print(f"  ⚠️  {table}.{column} = {current}  (esperado: {expected})")
            all_ok = False
        else:
            print(f"  ❌ {table}.{column} não encontrado")
            all_ok = False
    return all_ok

if __name__ == '__main__':
    print("""
  ╔══════════════════════════════════════════╗
  ║   TechOS — Migração de Banco de Dados    ║
  ╚══════════════════════════════════════════╝
""")
    conn = connect()
    try:
        ok, skipped, failed = run_migrations(conn)
        all_ok = verify(conn)

        print("\n" + "═"*60)
        print(f"  ✅ Colunas migradas : {len(ok)}")
        print(f"  ⏭  Sem alteração   : {len(skipped)}")
        print(f"  ❌ Com erro         : {len(failed)}")
        if failed:
            print("\n  Erros detalhados:")
            for t, c, e in failed:
                print(f"    • {t}.{c}: {e}")
        print("═"*60)

        if len(failed) == 0:
            print("\n  🎉 Migração concluída com sucesso!")
            print("  Agora execute: python app.py\n")
        else:
            print("\n  ⚠️  Migração concluída com erros. Verifique acima.\n")

    finally:
        conn.close()
