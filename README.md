# TechOS — Sistema de Gestão de Ordens de Serviço

## Instalação

### Pré-requisitos
- Python 3.8 ou superior

### Como rodar

1. **Instale as dependências:**
```bash
pip install flask flask-sqlalchemy flask-cors
```

2. **Inicie o sistema:**
```bash
python iniciar.py
```
   ou diretamente:
```bash
python app.py
```

3. **Acesse no navegador:**
```
http://localhost:5000
```

---

## Funcionalidades

### Cadastros
- **Minha Empresa** — Dados da prestadora de serviços
- **Clientes** — Empresas clientes (nome, CNPJ, telefone, endereço)
- **Lojas** — Unidades do cliente com dados do gerente
- **Equipamentos** — Balanças, PDVs, computadores por loja
- **Técnicos** — Equipe de atendimento

### Ordens de Serviço
- Criação de OS com preenchimento automático dos dados
- Uma OS por equipamento
- Status do atendimento
- Resumo financeiro

### Assinatura Digital em Lote
1. Vá em **Assinar OSs**
2. Selecione técnico e data
3. Revise as OSs pendentes
4. O gerente insere nome e assina com o dedo no celular
5. Sistema aplica a assinatura em todas as OSs de uma vez

### Banco de Dados
- SQLite local (`os_system.db`)
- Sem necessidade de servidor externo

---

## Uso em Celular
O sistema é responsivo e otimizado para uso no celular do técnico.
A assinatura pode ser feita com o dedo na tela touch.

---

## Tipos de Equipamento Suportados
- Balanças (Prix 4, Prix 3 Plus, Toledo, Filizola, etc.)
- Computadores
- PDVs
- Impressoras
- Monitores
- Terminais
- Nobreaks
- Outros
