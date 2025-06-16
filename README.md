# 🎬 Movies FASTAPI - Autenticação de Usuários

### Membros:
- Danilo Santana
- Diego Perpétuo
- Luccas Pino
- Milton Kiefer

Este é o backend de autenticação da aplicação **Movies Reviews**, responsável pelo cadastro e login de usuários. Desenvolvido em **Python** com **FastAPI**, este serviço fornece autenticação via JWT que será utilizada por outros serviços, como o sistema de avaliações de filmes.

## 📦 Tecnologias Utilizadas
- Python
- FastAPI
- JWT
- Uvicorn

## 🚀 Como rodar localmente

1. Clone este repositório:
   ```bash
   git clone https://github.com/diegoperpetuo/movies-fastapi.git
   cd movies-fastapi

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt

3. Inicie o servidor:
   ```bash
    uvicorn app.main:app --reload


##📂 Estrutura do Projeto

app/
├── main.py         # Ponto de entrada da aplicação
├── models.py       # Modelos Pydantic
├── routes.py       # Rotas de autenticação
└── auth.py         # Lógica de autenticação com JWT

  
###📌 Observações
Este backend é responsável apenas pelo gerenciamento de usuários (cadastro, login e autenticação).

A autenticação gera um token JWT que é utilizado pelo outro serviço (Movies Rating) para autorizar as ações do usuário.
