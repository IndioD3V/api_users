#!/bin/bash

echo "Rodando testes iniciais..."

pytest --maxfail=1 --disable-warnings -q

if [ $? -eq 0 ]; then
    echo "Testes passaram, iniciando a aplicação"
    alembic revision --autogenerate
    alembic upgrade head
    python app.py
else
    echo "Testes falharam, contêiner não será iniciado"
    exit 1
fi
