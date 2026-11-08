# Sistema de Gestão Comunitária – AMACE

Sistema web desenvolvido como MVP para apoiar a gestão de beneficiários e doações da Associação de Moradores e Apoio Comunitário do Bairro Esperança (AMACE).

## Funcionalidades

- Cadastro, consulta, edição e exclusão de beneficiários.
- Cadastro e consulta de produtos doados.
- Registro de entradas e saídas de estoque.
- Histórico de movimentações.
- Relatórios básicos de estoque e beneficiários.
- Autenticação e controle de acesso por perfil.
- Gerenciamento de usuários.

## Tecnologias utilizadas

- Python
- Django
- Bootstrap
- SQLite (ambiente de desenvolvimento)

## Como executar o projeto

1. Clone o repositório.
2. Crie e ative um ambiente virtual.
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute as migrações:

   ```bash
   python manage.py migrate
   ```

5. Crie um usuário administrador:

   ```bash
   python manage.py createsuperuser
   ```

6. Inicie o servidor:

   ```bash
   python manage.py runserver
   ```

7. Acesse `http://127.0.0.1:8000/contas/login/`.

## Testes

Para executar os testes automatizados:

```bash
python manage.py test
```

O projeto também possui integração contínua configurada com GitHub Actions para executar verificações e testes.

## Observação

Este projeto é um MVP acadêmico, desenvolvido para fins de estudo e validação das funcionalidades propostas.