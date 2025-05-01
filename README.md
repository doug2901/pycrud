# 🧪 CRUD de Usuários com Flask + Flasgger + Kubernetes

Este repositório contém um projeto simples de CRUD de usuários desenvolvido com **Flask**, documentado com **Flasgger** (Swagger UI) e preparado para ser executado em ambientes **Kubernetes**. Ele está sendo utilizado como base de estudos práticos para a certificação [CKAD - Certified Kubernetes Application Developer](https://www.cncf.io/certification/ckad/).

---

## 🚀 Objetivos

- Criar uma API RESTful simples com Python e Flask.
- Documentar a API com Swagger usando Flasgger.
- Criar arquivos de manifesto Kubernetes para **deployment**, **service**, e testes com **ConfigMap**, **Secrets**, **Volumes**, **Health Checks**, etc.
- Aprimorar práticas DevOps e experiência com deploys em clusters K8s.
- Servir como base para estudo e prática para a prova da CKAD.

---

## 🛠️ Tecnologias Utilizadas

- 🐍 Python 3.12+
- 🔥 Flask
- 📘 Flasgger (Swagger UI para Flask)
- 🐋 Docker
- ☸️ Kubernetes (Kind) | Orquestração de containers e testes de deployment |
- 🧪 Thuder Client (para testes da API)

---

## 🧱 Estrutura da API

### Endpoints principais:

- `POST /users` – Cria um novo usuário
- `GET /users` – Lista todos os usuários
- `GET /users/<id>` – Consulta um usuário por ID
- `PUT /users/<id>` – Atualiza os dados de um usuário
- `DELETE /users/<id>` – Remove um usuário

> A documentação interativa pode ser acessada via `/apidocs`.

---

## 📦 Como Executar Localmente

```bash
# Clonar o repositório
git clone https://github.com/doug2901/pycrud.git
cd pycrud

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
python app.py
