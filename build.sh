#!/bin/bash

# 1. Instala as dependências
pip install -r requirements.txt

# 2. Roda o collectstatic
python manage.py collectstatic --no-input