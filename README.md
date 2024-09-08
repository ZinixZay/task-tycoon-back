# To run
```bash
pip install pipenv

pipenv shell

pipenv install --ignore-pipfile 

docker compose up -d

alembic upgrade head

uvicorn main:app --reload
```