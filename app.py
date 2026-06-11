from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, date
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ─── CONFIG ───────────────────────────────────────────────────────────────────
DB_HOST     = os.environ.get('DB_HOST',     'os-system.banco-de-dados.svc.cluster.local')
DB_PORT     = os.environ.get('DB_PORT',     '3306')
DB_USER     = os.environ.get('DB_USER',     'mysql')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'ea7cz6o5czxsv77g8gsg')
DB_NAME     = os.environ.get('DB_NAME',     'os_sistem')
SECRET_KEY  = os.environ.get('SECRET_KEY',  'techos-secret-2026-xK9mP3')

def _test_mysql():
    try:
        import pymysql
        c = pymysql.connect(
            host=DB_HOST, port=int(DB_PORT), user=DB_USER,
            password=DB_PASSWORD, database=DB_NAME,
            connect_timeout=5
        )
        c.close()
        return True
    except Exception as e:
        print(f"⚠️  MySQL indisponível ({e})")
        return False

USE_MYSQL = _test_mysql()

if USE_MYSQL:
    DB_URI = (f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
              f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4")
    ENGINE_OPTS = {
        'pool_pre_ping': True, 'pool_recycle': 300,
        'pool_timeout': 20, 'pool_size': 5, 'max_overflow': 10,
    }
    print(f"✅ Usando MySQL: {DB_HOST}:{DB_PORT}/{DB_NAME}")
else:
    _sqlite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'techos_local.db')
    DB_URI = f"sqlite:///{_sqlite_path}"
    ENGINE_OPTS = {}
    print(f"⚠️  Usando SQLite local: {_sqlite_path}")

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if ENGINE_OPTS:
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = ENGINE_OPTS
app.secret_key = SECRET_KEY
CORS(app)
db  = SQLAlchemy(app)
ser = URLSafeTimedSerializer(SECRET_KEY)

# ─── MODELS ───────────────────────────────────────────────────────────────────
# IMPORTANTE: todos os models devem ser declarados ANTES de init_app()

class Company(db.Model):
    __tablename__ = 'company'
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(200), nullable=False)
    cnpj           = db.Column(db.String(30))
    phone          = db.Column(db.String(30))
    email          = db.Column(db.String(150))
    address        = db.Column(db.String(300))
    city           = db.Column(db.String(100))
    state          = db.Column(db.String(50))
    cep            = db.Column(db.String(15))
    logo_url       = db.Column(db.String(500))
    website        = db.Column(db.String(200))
    insc_municipal = db.Column(db.String(50))
    insc_estadual  = db.Column(db.String(50))
    smtp_host      = db.Column(db.String(100))
    smtp_port      = db.Column(db.Integer, default=587)
    smtp_user      = db.Column(db.String(150))
    smtp_password  = db.Column(db.String(200))
    smtp_from      = db.Column(db.String(150))
    parts_email    = db.Column(db.String(300))
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['smtp_password'] = '***' if d.get('smtp_password') else ''
        return d

class Client(db.Model):
    __tablename__ = 'client'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(200), nullable=False)
    cnpj       = db.Column(db.String(30))
    cpf        = db.Column(db.String(30))
    phone      = db.Column(db.String(30))
    email      = db.Column(db.String(150))
    address    = db.Column(db.String(300))
    city       = db.Column(db.String(100))
    state      = db.Column(db.String(50))
    cep        = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    stores     = db.relationship('Store', backref='client', lazy=True)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Store(db.Model):
    __tablename__ = 'store'
    id            = db.Column(db.Integer, primary_key=True)
    client_id     = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    name          = db.Column(db.String(200), nullable=False)
    cnpj          = db.Column(db.String(30))
    phone         = db.Column(db.String(30))
    address       = db.Column(db.String(300))
    city          = db.Column(db.String(100))
    state         = db.Column(db.String(50))
    cep           = db.Column(db.String(15))
    manager_name  = db.Column(db.String(200))
    manager_phone = db.Column(db.String(30))
    manager_email = db.Column(db.String(150))
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    equipments    = db.relationship('Equipment', backref='store', lazy=True)
    service_orders= db.relationship('ServiceOrder', backref='store', lazy=True)
    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['client_name'] = self.client.name if self.client else ''
        return d

class Technician(db.Model):
    __tablename__ = 'technician'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(200), nullable=False)
    phone      = db.Column(db.String(30))
    email      = db.Column(db.String(150))
    address    = db.Column(db.String(300))
    city       = db.Column(db.String(100))
    state      = db.Column(db.String(50))
    rg         = db.Column(db.String(30))
    cpf        = db.Column(db.String(30))
    active     = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    service_orders = db.relationship('ServiceOrder', backref='technician', lazy=True)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Equipment(db.Model):
    __tablename__ = 'equipment'
    id             = db.Column(db.Integer, primary_key=True)
    store_id       = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    name           = db.Column(db.String(200), nullable=False)
    serial_number  = db.Column(db.String(100))
    equipment_type = db.Column(db.String(100))
    brand          = db.Column(db.String(100))
    model          = db.Column(db.String(100))
    current_seal   = db.Column(db.String(100))
    previous_seal  = db.Column(db.String(100))
    current_label  = db.Column(db.String(100))
    previous_label = db.Column(db.String(100))
    max_load       = db.Column(db.String(50))
    portaria       = db.Column(db.String(50))
    mict           = db.Column(db.String(50))
    active         = db.Column(db.Boolean, default=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    service_orders = db.relationship('ServiceOrder', backref='equipment', lazy=True)
    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['store_name'] = self.store.name if self.store else ''
        return d

class User(db.Model):
    __tablename__ = 'user'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(200), nullable=False)
    username      = db.Column(db.String(100), unique=True, nullable=False)
    email         = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(256))
    role          = db.Column(db.String(20), default='technician')
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=True)
    store_id      = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=True)
    first_login   = db.Column(db.Boolean, default=True)
    active        = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)
    def check_password(self, pw):
        if not self.password_hash: return False
        return check_password_hash(self.password_hash, pw)
    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d.pop('password_hash', None)
        t = Technician.query.get(self.technician_id) if self.technician_id else None
        d['technician_name'] = t.name if t else ''
        s = Store.query.get(self.store_id) if self.store_id else None
        d['store_name'] = s.name if s else ''
        return d

class ServiceOrder(db.Model):
    __tablename__ = 'service_order'
    id                   = db.Column(db.Integer, primary_key=True)
    os_number            = db.Column(db.String(20), unique=True)
    store_id             = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    equipment_id         = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    technician_id        = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=False)
    call_date            = db.Column(db.String(20))
    call_time            = db.Column(db.String(10))
    call_type            = db.Column(db.String(100))
    service_date         = db.Column(db.String(20))
    start_time           = db.Column(db.String(10))
    end_time             = db.Column(db.String(10))
    travel_time          = db.Column(db.String(20))
    symptom              = db.Column(db.Text)
    services_description = db.Column(db.Text)
    actions              = db.Column(db.Text)
    codes                = db.Column(db.Text)
    status               = db.Column(db.String(50), default='Aberta')
    final_status         = db.Column(db.String(100))
    parts_value          = db.Column(db.Float, default=0)
    services_value       = db.Column(db.Float, default=0)
    expenses_value       = db.Column(db.Float, default=0)
    discount             = db.Column(db.Float, default=0)
    total_value          = db.Column(db.Float, default=0)
    signer_name          = db.Column(db.String(200))
    signer_role          = db.Column(db.String(100))
    client_signature     = db.Column(db.Text)
    tech_signature       = db.Column(db.Text)
    signed_at            = db.Column(db.DateTime)
    notes                = db.Column(db.Text)
    created_at           = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at           = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['store_name']         = self.store.name if self.store else ''
        d['store_address']      = self.store.address if self.store else ''
        d['store_city']         = self.store.city if self.store else ''
        d['store_phone']        = self.store.phone if self.store else ''
        d['store_cnpj']         = self.store.cnpj if self.store else ''
        d['store_manager']      = self.store.manager_name if self.store else ''
        d['client_name']        = self.store.client.name if self.store and self.store.client else ''
        d['equipment_name']     = self.equipment.name if self.equipment else ''
        d['equipment_serial']   = self.equipment.serial_number if self.equipment else ''
        d['equipment_type']     = self.equipment.equipment_type if self.equipment else ''
        d['equipment_brand']    = self.equipment.brand if self.equipment else ''
        d['equipment_model']    = self.equipment.model if self.equipment else ''
        d['equipment_seal']     = self.equipment.current_seal if self.equipment else ''
        d['equipment_label']    = self.equipment.current_label if self.equipment else ''
        d['equipment_max_load'] = self.equipment.max_load if self.equipment else ''
        d['equipment_portaria'] = self.equipment.portaria if self.equipment else ''
        d['equipment_mict']     = self.equipment.mict if self.equipment else ''
        d['technician_name']    = self.technician.name if self.technician else ''
        d['technician_rg']      = self.technician.rg if self.technician else ''
        d['created_at']  = self.created_at.isoformat() if self.created_at else ''
        d['updated_at']  = self.updated_at.isoformat() if self.updated_at else ''
        d['signed_at']   = self.signed_at.isoformat() if self.signed_at else ''
        return d

class PartsRequest(db.Model):
    __tablename__ = 'parts_request'
    id             = db.Column(db.Integer, primary_key=True)
    request_number = db.Column(db.String(20), unique=True)
    technician_id  = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=False)
    store_id       = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=True)
    equipment_id   = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=True)
    os_id          = db.Column(db.Integer, db.ForeignKey('service_order.id'), nullable=True)
    status         = db.Column(db.String(30), default='Pendente')
    urgency        = db.Column(db.String(20), default='Normal')
    notes          = db.Column(db.Text)
    email_sent     = db.Column(db.Boolean, default=False)
    email_sent_at  = db.Column(db.DateTime)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at     = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    items          = db.relationship('PartsRequestItem', backref='request', lazy=True, cascade='all, delete-orphan')
    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['created_at']    = self.created_at.isoformat() if self.created_at else ''
        d['updated_at']    = self.updated_at.isoformat() if self.updated_at else ''
        d['email_sent_at'] = self.email_sent_at.isoformat() if self.email_sent_at else ''
        tech  = Technician.query.get(self.technician_id)
        store = Store.query.get(self.store_id) if self.store_id else None
        equip = Equipment.query.get(self.equipment_id) if self.equipment_id else None
        os_   = ServiceOrder.query.get(self.os_id) if self.os_id else None
        d['technician_name'] = tech.name if tech else ''
        d['store_name']      = store.name if store else ''
        d['equipment_name']  = equip.name if equip else ''
        d['os_number']       = os_.os_number if os_ else ''
        d['items']           = [i.to_dict() for i in self.items]
        return d

class PartsRequestItem(db.Model):
    __tablename__ = 'parts_request_item'
    id          = db.Column(db.Integer, primary_key=True)
    request_id  = db.Column(db.Integer, db.ForeignKey('parts_request.id', ondelete='CASCADE'), nullable=False)
    code        = db.Column(db.String(50))
    description = db.Column(db.String(300), nullable=False)
    quantity    = db.Column(db.Float, default=1)
    unit        = db.Column(db.String(20), default='un')
    notes       = db.Column(db.String(300))
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# ─── DB INIT ──────────────────────────────────────────────────────────────────
# Chamado APÓS todos os models estarem definidos
def init_app():
    with app.app_context():
        try:
            db.create_all()
            print("✅ Tabelas criadas/verificadas com sucesso")
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            return
        try:
            # Seed admin
            if not User.query.filter_by(username='admin').first():
                admin = User(
                    name='Administrador', username='admin',
                    email='admin@techos.local', role='admin',
                    first_login=False, active=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                print("✅ Usuário admin criado (admin / admin123)")
            else:
                print("✅ Usuário admin já existe")
            # Seed company
            if not Company.query.first():
                db.session.add(Company(name='Minha Empresa', phone='', city='', state=''))
                print("✅ Empresa padrão criada")
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro no seed: {e}")

# Executa init AGORA — todos os models já foram declarados acima
init_app()

# ─── AUTH HELPERS ─────────────────────────────────────────────────────────────

def gen_token(uid):
    return ser.dumps(uid, salt='auth')

def check_token(token):
    try:
        uid = ser.loads(token, salt='auth', max_age=86400*30)
        return User.query.filter_by(id=uid, active=True).first()
    except (BadSignature, SignatureExpired):
        return None

def current_user():
    h = request.headers.get('Authorization', '')
    if h.startswith('Bearer '):
        return check_token(h[7:])
    return None

def auth_required(f):
    @wraps(f)
    def d(*a, **kw):
        u = current_user()
        if not u: return jsonify({'error': 'Não autorizado. Faça login.'}), 401
        g.user = u
        return f(*a, **kw)
    return d

def admin_required(f):
    @wraps(f)
    def d(*a, **kw):
        u = current_user()
        if not u: return jsonify({'error': 'Não autorizado.'}), 401
        if u.role != 'admin': return jsonify({'error': 'Acesso restrito a administradores.'}), 403
        g.user = u
        return f(*a, **kw)
    return d

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def sanitize_str(v, mx=None):
    if v is None: return None
    v = str(v).strip()
    if mx and len(v) > mx: v = v[:mx]
    return v or None

def sanitize_client(data):
    c = dict(data)
    cnpj = (c.get('cnpj') or '').strip()
    cpf  = (c.get('cpf') or '').strip()
    if cpf and len(cpf) > 14: c['cpf'] = None
    if cpf and cnpj and cpf == cnpj: c['cpf'] = None
    for f in ('phone', 'cnpj', 'cpf', 'cep'):
        if f in c: c[f] = sanitize_str(c[f], 30)
    c['state'] = sanitize_str(c.get('state'), 50)
    c['email'] = sanitize_str(c.get('email'), 150)
    return c

def gen_os():
    last = ServiceOrder.query.order_by(ServiceOrder.id.desc()).first()
    return f"{(last.id + 1) if last else 1:06d}"

def gen_req():
    last = PartsRequest.query.order_by(PartsRequest.id.desc()).first()
    return f"REQ-{(last.id + 1) if last else 1:05d}"

def os_role_filter(q, user):
    if user.role == 'technician' and user.technician_id:
        q = q.filter(ServiceOrder.technician_id == user.technician_id)
    elif user.role == 'manager' and user.store_id:
        q = q.filter(ServiceOrder.store_id == user.store_id)
    return q

# ─── EMAIL ────────────────────────────────────────────────────────────────────

def send_email(subject, html, to_list):
    co = Company.query.first()
    if not co or not co.smtp_host or not co.smtp_user:
        return False, 'SMTP não configurado em Minha Empresa.'
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From']    = co.smtp_from or co.smtp_user
        msg['To']      = ', '.join(to_list)
        msg.attach(MIMEText(html, 'html', 'utf-8'))
        with smtplib.SMTP(co.smtp_host, co.smtp_port or 587, timeout=15) as s:
            s.ehlo(); s.starttls(); s.login(co.smtp_user, co.smtp_password or '')
            s.sendmail(msg['From'], to_list, msg.as_string())
        return True, 'Email enviado!'
    except Exception as e:
        return False, f'Erro SMTP: {e}'

def parts_email_html(pr, co):
    uc = {'Normal': '#58a6ff', 'Urgente': '#d29922', 'Crítico': '#f85149'}.get(pr.urgency, '#58a6ff')
    rows = ''.join(
        f"<tr><td style='padding:7px 10px;border-bottom:1px solid #eee'>{i.code or '-'}</td>"
        f"<td style='padding:7px 10px;border-bottom:1px solid #eee'>{i.description}</td>"
        f"<td style='padding:7px 10px;border-bottom:1px solid #eee;text-align:center'>{i.quantity} {i.unit}</td>"
        f"<td style='padding:7px 10px;border-bottom:1px solid #eee'>{i.notes or ''}</td></tr>"
        for i in pr.items
    )
    tech  = Technician.query.get(pr.technician_id)
    store = Store.query.get(pr.store_id) if pr.store_id else None
    equip = Equipment.query.get(pr.equipment_id) if pr.equipment_id else None
    os_   = ServiceOrder.query.get(pr.os_id) if pr.os_id else None
    co_name = co.name if co else 'TechOS'
    dt = pr.created_at.strftime('%d/%m/%Y %H:%M') if pr.created_at else ''
    return f"""<div style="font-family:Arial,sans-serif;max-width:680px;margin:0 auto;background:#f4f4f4;padding:20px">
      <div style="background:#161b22;color:white;padding:18px 22px;border-radius:8px 8px 0 0">
        <h2 style="margin:0;font-size:18px">🔧 {co_name} — Solicitação de Peças</h2>
        <p style="margin:4px 0 0;color:#8b949e;font-size:12px">{pr.request_number} &nbsp;|&nbsp; {dt}</p>
      </div>
      <div style="background:#fff;padding:20px 22px">
        <table style="width:100%;margin-bottom:14px;font-size:13px">
          <tr><td><b>Técnico:</b> {tech.name if tech else '-'}</td><td><b>Loja:</b> {store.name if store else '-'}</td></tr>
          <tr><td><b>Equipamento:</b> {equip.name if equip else '-'}</td><td><b>OS:</b> #{os_.os_number if os_ else '-'}</td></tr>
          <tr><td colspan="2"><b>Urgência:</b> <span style="color:{uc};font-weight:700">{pr.urgency}</span></td></tr>
        </table>
        <table style="width:100%;border-collapse:collapse;border:1px solid #e0e0e0;font-size:13px">
          <thead><tr style="background:#f0f0f0">
            <th style="padding:8px 10px;text-align:left">CÓDIGO</th>
            <th style="padding:8px 10px;text-align:left">DESCRIÇÃO</th>
            <th style="padding:8px 10px;text-align:center">QTD</th>
            <th style="padding:8px 10px;text-align:left">OBS</th>
          </tr></thead>
          <tbody>{rows}</tbody>
        </table>
        {'<p style="margin-top:12px;font-size:13px"><b>Observações:</b> ' + pr.notes + '</p>' if pr.notes else ''}
        <p style="margin-top:16px;font-size:11px;color:#999">Gerado pelo TechOS</p>
      </div></div>"""

# ─── ROUTES ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    html_path = os.path.join(app.template_folder, 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return f.read(), 200, {'Content-Type': 'text/html; charset=utf-8'}

# Auth
@app.route('/api/auth/login', methods=['POST'])
def login():
    d = request.json or {}
    uname = (d.get('username') or '').strip().lower()
    pw    = d.get('password') or ''
    u = User.query.filter(
        db.or_(User.username == uname, User.email == uname),
        User.active == True
    ).first()
    if not u or not u.check_password(pw):
        return jsonify({'error': 'Usuário ou senha incorretos.'}), 401
    return jsonify({'token': gen_token(u.id), 'user': u.to_dict(), 'first_login': u.first_login})

@app.route('/api/auth/set-password', methods=['POST'])
def set_password():
    d = request.json or {}
    uname = (d.get('username') or '').strip().lower()
    pw    = d.get('password') or ''
    if len(pw) < 6:
        return jsonify({'error': 'Senha deve ter ao menos 6 caracteres.'}), 400
    u = User.query.filter(db.or_(User.username == uname, User.email == uname)).first()
    if not u: return jsonify({'error': 'Usuário não encontrado.'}), 404
    u.set_password(pw); u.first_login = False
    db.session.commit()
    return jsonify({'token': gen_token(u.id), 'user': u.to_dict()})

@app.route('/api/auth/me')
@auth_required
def me(): return jsonify(g.user.to_dict())

# Users
@app.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    return jsonify([u.to_dict() for u in User.query.filter_by(active=True).order_by(User.name).all()])

@app.route('/api/users', methods=['POST'])
@admin_required
def create_user():
    try:
        d = request.json or {}
        uname = (d.get('username') or '').strip().lower()
        if not uname or not d.get('name'):
            return jsonify({'error': 'Nome e usuário são obrigatórios.'}), 400
        if User.query.filter_by(username=uname).first():
            return jsonify({'error': 'Usuário já existe.'}), 400
        u = User(name=d['name'], username=uname,
                 email=(d.get('email') or '').strip() or None,
                 role=d.get('role', 'technician'),
                 technician_id=d.get('technician_id') or None,
                 store_id=d.get('store_id') or None,
                 first_login=True, active=True)
        if d.get('temp_password'): u.set_password(d['temp_password'])
        db.session.add(u); db.session.commit()
        return jsonify(u.to_dict()), 201
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/users/<int:uid>', methods=['PUT'])
@admin_required
def update_user(uid):
    try:
        u = User.query.get_or_404(uid)
        d = request.json or {}
        for f in ('name', 'email', 'role'):
            if f in d: setattr(u, f, d[f])
        for f in ('technician_id', 'store_id'):
            if f in d: setattr(u, f, d[f] or None)
        if d.get('username'): u.username = d['username'].strip().lower()
        if d.get('temp_password'):
            u.set_password(d['temp_password']); u.first_login = True
        db.session.commit(); return jsonify(u.to_dict())
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/users/<int:uid>', methods=['DELETE'])
@admin_required
def delete_user(uid):
    u = User.query.get_or_404(uid)
    u.active = False; db.session.commit()
    return jsonify({'ok': True})

# Company
@app.route('/api/company', methods=['GET'])
def get_company():
    c = Company.query.first()
    return jsonify(c.to_dict() if c else {})

@app.route('/api/company', methods=['POST'])
@auth_required
def save_company():
    try:
        d = request.json or {}
        smtp_pw = d.pop('smtp_password', None)
        c = Company.query.first()
        if c:
            for k, v in d.items():
                if hasattr(c, k) and k != 'id': setattr(c, k, v)
            if smtp_pw and smtp_pw != '***': c.smtp_password = smtp_pw
        else:
            c = Company(**{k: v for k, v in d.items() if hasattr(Company, k) and k != 'id'})
            if smtp_pw and smtp_pw != '***': c.smtp_password = smtp_pw
            db.session.add(c)
        db.session.commit(); return jsonify(c.to_dict())
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/company/test-email', methods=['POST'])
@admin_required
def test_email():
    to = (request.json or {}).get('to', '')
    if not to: return jsonify({'error': 'Informe o email de destino.'}), 400
    ok, msg = send_email('TechOS — Teste de Email', '<h2>✅ Email configurado com sucesso!</h2>', [to])
    return jsonify({'ok': ok, 'message': msg})

# Clients
@app.route('/api/clients', methods=['GET'])
@auth_required
def get_clients():
    return jsonify([c.to_dict() for c in Client.query.order_by(Client.name).all()])

@app.route('/api/clients', methods=['POST'])
@auth_required
def create_client():
    try:
        c = Client(**{k: v for k, v in sanitize_client(request.json or {}).items() if hasattr(Client, k) and k != 'id'})
        db.session.add(c); db.session.commit(); return jsonify(c.to_dict()), 201
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/clients/<int:cid>', methods=['PUT'])
@auth_required
def update_client(cid):
    try:
        c = Client.query.get_or_404(cid)
        for k, v in sanitize_client(request.json or {}).items():
            if hasattr(c, k) and k != 'id': setattr(c, k, v)
        db.session.commit(); return jsonify(c.to_dict())
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/clients/<int:cid>', methods=['DELETE'])
@admin_required
def delete_client(cid):
    c = Client.query.get_or_404(cid); db.session.delete(c); db.session.commit()
    return jsonify({'ok': True})

# Stores
@app.route('/api/stores', methods=['GET'])
@auth_required
def get_stores():
    q = Store.query
    if g.user.role == 'manager' and g.user.store_id:
        q = q.filter_by(id=g.user.store_id)
    return jsonify([s.to_dict() for s in q.order_by(Store.name).all()])

@app.route('/api/stores', methods=['POST'])
@auth_required
def create_store():
    try:
        d = request.json or {}
        s = Store(**{k: v for k, v in d.items() if hasattr(Store, k) and k not in ('id', 'client_name')})
        db.session.add(s); db.session.commit(); return jsonify(s.to_dict()), 201
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/stores/<int:sid>', methods=['PUT'])
@auth_required
def update_store(sid):
    try:
        s = Store.query.get_or_404(sid)
        for k, v in (request.json or {}).items():
            if hasattr(s, k) and k not in ('id', 'client_name'): setattr(s, k, v)
        db.session.commit(); return jsonify(s.to_dict())
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/stores/<int:sid>', methods=['DELETE'])
@admin_required
def delete_store(sid):
    s = Store.query.get_or_404(sid); db.session.delete(s); db.session.commit()
    return jsonify({'ok': True})

# Equipment
@app.route('/api/equipment', methods=['GET'])
@auth_required
def get_equipment():
    sid = request.args.get('store_id')
    q = Equipment.query.filter_by(active=True)
    if sid: q = q.filter_by(store_id=sid)
    elif g.user.role == 'manager' and g.user.store_id: q = q.filter_by(store_id=g.user.store_id)
    return jsonify([e.to_dict() for e in q.order_by(Equipment.name).all()])

@app.route('/api/equipment', methods=['POST'])
@auth_required
def create_equipment():
    try:
        d = request.json or {}
        e = Equipment(**{k: v for k, v in d.items() if hasattr(Equipment, k) and k not in ('id', 'store_name')})
        db.session.add(e); db.session.commit(); return jsonify(e.to_dict()), 201
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/equipment/<int:eid>', methods=['PUT'])
@auth_required
def update_equipment(eid):
    try:
        e = Equipment.query.get_or_404(eid)
        for k, v in (request.json or {}).items():
            if hasattr(e, k) and k not in ('id', 'store_name'): setattr(e, k, v)
        db.session.commit(); return jsonify(e.to_dict())
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/equipment/<int:eid>', methods=['DELETE'])
@admin_required
def delete_equipment(eid):
    e = Equipment.query.get_or_404(eid); e.active = False; db.session.commit()
    return jsonify({'ok': True})

# Technicians
@app.route('/api/technicians', methods=['GET'])
@auth_required
def get_technicians():
    return jsonify([t.to_dict() for t in Technician.query.filter_by(active=True).order_by(Technician.name).all()])

@app.route('/api/technicians', methods=['POST'])
@admin_required
def create_technician():
    try:
        data = request.json or {}
        t = Technician(**{k: v for k, v in data.items() if hasattr(Technician, k) and k != 'id'})
        db.session.add(t)
        db.session.flush()
        import unicodedata
        def slugify(name):
            n = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
            n = ''.join(c for c in n if c.isalnum() or c.isspace()).strip().lower()
            parts = n.split()
            return (parts[0] + '.' + parts[-1]) if len(parts) >= 2 else (parts[0] if parts else 'tecnico')
        base_username = slugify(t.name)
        username = base_username; counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"; counter += 1
        temp_pw = data.get('temp_password', 'techos123')
        user = User(name=t.name, username=username, email=t.email or None,
                    role='technician', technician_id=t.id, first_login=True, active=True)
        user.set_password(temp_pw)
        db.session.add(user)
        db.session.commit()
        result = t.to_dict()
        result['user_created'] = {'username': username, 'temp_password': temp_pw,
            'message': f'Usuário "{username}" criado com senha temporária "{temp_pw}".'}
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/technicians/<int:tid>', methods=['PUT'])
@admin_required
def update_technician(tid):
    try:
        t = Technician.query.get_or_404(tid)
        for k, v in (request.json or {}).items():
            if hasattr(t, k) and k != 'id': setattr(t, k, v)
        db.session.commit(); return jsonify(t.to_dict())
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/technicians/<int:tid>', methods=['DELETE'])
@admin_required
def delete_technician(tid):
    t = Technician.query.get_or_404(tid); t.active = False; db.session.commit()
    return jsonify({'ok': True})

# Service Orders
@app.route('/api/orders', methods=['GET'])
@auth_required
def get_orders():
    q = os_role_filter(ServiceOrder.query, g.user)
    sid = request.args.get('store_id')
    tid = request.args.get('technician_id')
    st  = request.args.get('status')
    dt  = request.args.get('date')
    if sid: q = q.filter(ServiceOrder.store_id == sid)
    if tid: q = q.filter(ServiceOrder.technician_id == tid)
    if st:  q = q.filter(ServiceOrder.status == st)
    if dt:  q = q.filter(ServiceOrder.service_date == dt)
    return jsonify([o.to_dict() for o in q.order_by(ServiceOrder.created_at.desc()).all()])

@app.route('/api/orders', methods=['POST'])
@auth_required
def create_order():
    try:
        d = request.json or {}
        o = ServiceOrder(os_number=gen_os(),
            **{k: v for k, v in d.items() if hasattr(ServiceOrder, k) and k not in ('id', 'os_number')})
        db.session.add(o); db.session.commit(); return jsonify(o.to_dict()), 201
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/orders/<int:oid>', methods=['GET'])
@auth_required
def get_order(oid):
    return jsonify(ServiceOrder.query.get_or_404(oid).to_dict())

@app.route('/api/orders/<int:oid>', methods=['PUT'])
@auth_required
def update_order(oid):
    try:
        o = ServiceOrder.query.get_or_404(oid)
        for k, v in (request.json or {}).items():
            if hasattr(o, k) and k not in ('id', 'os_number', 'created_at'): setattr(o, k, v)
        o.updated_at = datetime.utcnow(); db.session.commit(); return jsonify(o.to_dict())
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/orders/<int:oid>', methods=['DELETE'])
@auth_required
def delete_order(oid):
    o = ServiceOrder.query.get_or_404(oid); db.session.delete(o); db.session.commit()
    return jsonify({'ok': True})

@app.route('/api/orders/batch-sign', methods=['POST'])
@auth_required
def batch_sign():
    d = request.json or {}
    now = datetime.utcnow(); count = 0
    for oid in (d.get('order_ids') or []):
        o = ServiceOrder.query.get(oid)
        if o:
            o.signer_name = d.get('signer_name', '')
            o.signer_role = d.get('signer_role', '')
            o.client_signature = d.get('signature', '')
            o.signed_at = now; o.status = 'Assinada'; count += 1
    db.session.commit(); return jsonify({'ok': True, 'signed': count})

@app.route('/api/orders/pending-sign', methods=['GET'])
@auth_required
def pending_sign():
    tid = request.args.get('technician_id')
    dt  = request.args.get('date')
    q = os_role_filter(ServiceOrder.query.filter(ServiceOrder.status != 'Assinada'), g.user)
    if tid: q = q.filter(ServiceOrder.technician_id == tid)
    if dt:  q = q.filter(ServiceOrder.service_date == dt)
    return jsonify([o.to_dict() for o in q.order_by(ServiceOrder.service_date.desc(), ServiceOrder.os_number).all()])

@app.route('/api/orders/today-unsigned', methods=['GET'])
@auth_required
def today_unsigned():
    today = date.today().isoformat()
    q = os_role_filter(ServiceOrder.query.filter(
        ServiceOrder.service_date == today, ServiceOrder.status != 'Assinada'), g.user)
    return jsonify([o.to_dict() for o in q.all()])

# Parts Requests
@app.route('/api/parts-requests', methods=['GET'])
@auth_required
def get_parts_requests():
    q = PartsRequest.query
    if g.user.role == 'technician' and g.user.technician_id:
        q = q.filter_by(technician_id=g.user.technician_id)
    elif g.user.role == 'manager' and g.user.store_id:
        q = q.filter_by(store_id=g.user.store_id)
    st = request.args.get('status')
    if st: q = q.filter_by(status=st)
    return jsonify([r.to_dict() for r in q.order_by(PartsRequest.created_at.desc()).all()])

@app.route('/api/parts-requests', methods=['POST'])
@auth_required
def create_parts_request():
    try:
        d = request.json or {}
        items_data = d.pop('items', [])
        pr = PartsRequest(request_number=gen_req(),
            **{k: v for k, v in d.items() if hasattr(PartsRequest, k) and k not in ('id', 'request_number', 'items')})
        db.session.add(pr); db.session.flush()
        for item in items_data:
            db.session.add(PartsRequestItem(request_id=pr.id,
                **{k: v for k, v in item.items() if hasattr(PartsRequestItem, k) and k not in ('id', 'request_id')}))
        db.session.commit(); return jsonify(pr.to_dict()), 201
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 400

@app.route('/api/parts-requests/<int:rid>/status', methods=['PUT'])
@auth_required
def update_parts_status(rid):
    pr = PartsRequest.query.get_or_404(rid)
    d = request.json or {}
    if 'status' in d: pr.status = d['status']
    pr.updated_at = datetime.utcnow(); db.session.commit()
    return jsonify(pr.to_dict())

@app.route('/api/parts-requests/<int:rid>/send-email', methods=['POST'])
@auth_required
def send_parts_email(rid):
    pr = PartsRequest.query.get_or_404(rid)
    co = Company.query.first()
    to = []
    if co and co.parts_email:
        to = [e.strip() for e in co.parts_email.split(',') if e.strip()]
    tech = Technician.query.get(pr.technician_id)
    if tech and tech.email: to.append(tech.email)
    to = list(set(to))
    if not to:
        return jsonify({'ok': False, 'message': 'Configure o email de peças em Minha Empresa.'}), 400
    ok, msg = send_email(
        f"[TechOS] {pr.request_number} — Solicitação de Peças ({pr.urgency})",
        parts_email_html(pr, co), to)
    if ok:
        pr.email_sent = True; pr.email_sent_at = datetime.utcnow(); db.session.commit()
    return jsonify({'ok': ok, 'message': msg})

@app.route('/api/parts-requests/<int:rid>', methods=['DELETE'])
@auth_required
def delete_parts_request(rid):
    pr = PartsRequest.query.get_or_404(rid); db.session.delete(pr); db.session.commit()
    return jsonify({'ok': True})

# Dashboard
@app.route('/api/dashboard', methods=['GET'])
@auth_required
def dashboard():
    today = date.today().isoformat()
    bq = os_role_filter(ServiceOrder.query, g.user)
    pr_q = PartsRequest.query
    if g.user.role == 'technician' and g.user.technician_id:
        pr_q = pr_q.filter_by(technician_id=g.user.technician_id)
    return jsonify({
        'total_orders':    bq.count(),
        'today_orders':    bq.filter(ServiceOrder.service_date == today).count(),
        'signed_today':    bq.filter(ServiceOrder.service_date == today, ServiceOrder.status == 'Assinada').count(),
        'open_orders':     bq.filter(ServiceOrder.status != 'Assinada').count(),
        'pending_parts':   pr_q.filter_by(status='Pendente').count(),
        'total_clients':   Client.query.count(),
        'total_stores':    Store.query.count(),
        'total_equipment': Equipment.query.filter_by(active=True).count(),
        'total_techs':     Technician.query.filter_by(active=True).count(),
    })

# ─── STARTUP ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    db_type = "MySQL" if USE_MYSQL else "SQLite (local)"
    print(f"\n{'='*50}")
    print(f"  🚀 TechOS iniciado com {db_type}")
    print(f"  🌐 Acesse: http://localhost:5000")
    print(f"  🔑 Login: admin / admin123")
    print(f"{'='*50}\n")
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode, port=5000, host='0.0.0.0')