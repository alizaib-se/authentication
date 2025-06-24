# 🔧 Database Migrations with Alembic

This project uses Alembic for managing database schema migrations.

### ⚙️ Commands

Create a new migration:
```bash
  alembic revision --autogenerate -m "Initial migration"
```
apply migrations to your database

```bash
  alembic upgrade head
```
To roll back the last migration

```bash
  alembic downgrade -1
```



