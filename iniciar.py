#!/usr/bin/env python3
"""TechOS — Inicializador (MySQL)"""
import subprocess, sys, os

DEPS = ['flask', 'flask-sqlalchemy', 'flask-cors', 'pymysql', 'cryptography']

print("📦 Verificando dependências...")
subprocess.check_call([sys.executable,'-m','pip','install',*DEPS,'--quiet'])

print("🔌 Conectando ao banco MySQL...")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Company

with app.app_context():
    try:
        db.create_all()
        if not Company.query.first():
            db.session.add(Company(name='Minha Empresa', phone='(00) 0000-0000'))
            db.session.commit()
        print("✅ Banco de dados OK!")
    except Exception as e:
        print(f"⚠️  Erro no banco: {e}")
        print("   Execute primeiro: python setup_banco.py")
        sys.exit(1)

print("\n✅ TechOS pronto!")
print("🌐 Acesse: http://localhost:5000\n")
app.run(debug=False, port=5000, host='0.0.0.0')
