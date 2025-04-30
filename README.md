# 🔐 FastAPI Auth API

Uma API de autenticação moderna e segura com **FastAPI**, usando **JWT com Refresh Token**, **controle de usuários e permissões**, e **estrutura pronta para produção**.

---

## 📦 Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [JWT (python-jose)](https://github.com/mpdavis/python-jose)
- [Passlib (bcrypt)](https://passlib.readthedocs.io/)

---

## 🚀 Funcionalidades

- ✅ Registro de usuários com senha criptografada (bcrypt)
- ✅ Login com geração de **access token** e **refresh token**
- ✅ Validação e proteção de rotas autenticadas
- ✅ Sistema de **Refresh Token** para renovar o login
- ✅ Controle de permissão com `is_admin`
- ✅ Rotas exclusivas para administradores
- ✅ Alembic configurado para migração de banco
- ✅ Pronto para deploy e integração com frontend

---

## 📁 Estrutura do Projeto
fast-auth/ ├── app/ │ ├── main.py │ ├── config.py │ ├── database.py │ ├── models.py │ ├── schemas.py │ └── auth/ │ ├── routes.py │ ├── deps.py │ ├── jwt_handler.py │ └── utils.py ├── alembic/ │ └── versions/ ├── .env ├── alembic.ini ├── requirements.txt └── README.md


---

## ⚙️ Instalação e Execução

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/fastapi-auth.git
cd fastapi-auth


python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


pip install -r requirements.txt


DATABASE_URL=postgresql://usuario:senha@localhost:5432/fast-auth
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7



alembic upgrade head


| Método | Endpoint                   | Descrição                             |
|--------|----------------------------|----------------------------------------|
| POST   | `/auth/register`           | Registro de novo usuário              |
| POST   | `/auth/login`              | Login e geração de tokens             |
| POST   | `/auth/refresh`            | Gera novo access token com refresh    |
| GET    | `/auth/protected`          | Rota protegida por autenticação       |
| GET    | `/auth/admin/protected`    | Rota exclusiva para admins            |
| PATCH  | `/auth/admin/promote/{id}` | Promove um usuário a admin            |



http://127.0.0.1:8000/docs



