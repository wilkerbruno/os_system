#!/usr/bin/env python3
"""
TechOS — Fix Admin
Recria o usuário admin com senha correta.
Execute no servidor: python fix_admin.py
"""
import sys

try:
    import pymysql
    from werkzeug.security import generate_password_hash, check_password_hash
except ImportError:
    print("pip install pymysql werkzeug cryptography")
    sys.exit(1)

CONFIG = {
    'host':            '2.25.131.174',
    'port':            3409,
    'user':            'mysql',
    'password':        'ea7cz6o5czxsv77g8gsg',
    'database':        'os_sistem',
    'charset':         'utf8mb4',
    'connect_timeout': 10,
}

NOVA_SENHA = 'admin123'

def main():
    print("\n  TechOS — Fix Admin\n")

    # Conectar
    try:
        conn = pymysql.connect(**CONFIG)
        cur  = conn.cursor()
        print(f"✅ Conectado em {CONFIG['host']}:{CONFIG['port']}\n")
    except Exception as e:
        print(f"❌ Falha na conexão: {e}")
        sys.exit(1)

    # Verificar se tabela user existe
    cur.execute(
        "SELECT COUNT(*) FROM information_schema.TABLES "
        "WHERE TABLE_SCHEMA=%s AND TABLE_NAME='user'",
        (CONFIG['database'],)
    )
    if cur.fetchone()[0] == 0:
        print("❌ Tabela 'user' não existe! Execute setup_banco.py primeiro.")
        conn.close()
        sys.exit(1)

    # Ver registros atuais
    cur.execute("SELECT id, username, email, role, active, password_hash FROM `user`")
    rows = cur.fetchall()
    print(f"Usuários encontrados: {len(rows)}")
    for r in rows:
        has_hash = "✅ tem hash" if r[5] else "❌ SEM HASH"
        print(f"  id={r[0]:3} | user={r[1]:<20} | role={r[3]:<15} | active={r[4]} | {has_hash}")

    # Gerar hash correto
    new_hash = generate_password_hash(NOVA_SENHA)
    print(f"\nHash novo gerado: {new_hash[:40]}...")
    print(f"Verificação: {check_password_hash(new_hash, NOVA_SENHA)}")

    # Verificar se admin existe
    cur.execute("SELECT id FROM `user` WHERE username='admin'")
    row = cur.fetchone()

    if row:
        # Atualizar hash e garantir active=1, first_login=0
        cur.execute(
            "UPDATE `user` SET password_hash=%s, active=1, first_login=0 WHERE username='admin'",
            (new_hash,)
        )
        conn.commit()
        print(f"\n✅ Admin atualizado! (id={row[0]})")
    else:
        # Criar do zero
        cur.execute(
            """INSERT INTO `user`
               (name, username, email, password_hash, role, first_login, active)
               VALUES (%s, %s, %s, %s, 'admin', 0, 1)""",
            ('Administrador', 'admin', 'admin@techos.local', new_hash)
        )
        conn.commit()
        print(f"\n✅ Admin criado do zero! (id={cur.lastrowid})")

    # Verificar se company existe, senão criar
    cur.execute("SELECT COUNT(*) FROM `company`")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO `company` (name, phone, city, state) VALUES ('Minha Empresa','','','')"
        )
        conn.commit()
        print("✅ Empresa padrão criada.")

    # Confirmar
    cur.execute(
        "SELECT id, username, role, active, first_login, LEFT(password_hash,20) FROM `user` WHERE username='admin'"
    )
    r = cur.fetchone()
    print(f"\n  Estado final do admin:")
    print(f"  id={r[0]} | username={r[1]} | role={r[2]} | active={r[3]} | first_login={r[4]} | hash={r[5]}...")

    conn.close()
    print(f"\n{'='*45}")
    print(f"  Login:  admin")
    print(f"  Senha:  {NOVA_SENHA}")
    print(f"  URL:    http://localhost:5000")
    print(f"{'='*45}\n")

if __name__ == '__main__':
    main()