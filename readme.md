## Local setup

```
# Initialize veirtual env
poetry config virtualenvs.in-project true
poetry init -n --python '^3.12'
poetry env use $(which python3)

# if you have requiremets.txt, install dependencies from there
poetry add $(cat requirements.txt | awk '{print $1}')

# Install all dependencies from the pyproject.toml file without installing the current project as a package into the virtual environment
poetry install --no-root

# verify virtual environment
poetry env info

# Activate virtual environment
eval $(poetry env activate)

# add new dependencies
poetry add fastapi uvicorn

# alembic migrations
poetry add alembic
alembic init migrations
alembic revision --autogenerate -m "Create initial tables"
alembic upgrade head

# run app
docker compose up
python main.py

# run tests
PYTHONPATH=$PYTHONPATH:. pytest tests/
PYTHONPATH=$PYTHONPATH:. pytest tests/ --cov=src --cov-report=term
pytest --cov=src
```

# Run application

```
uvicorn main:app --reload
```

curl localhost:8000/healthcheck

# Ingest knowledge base into postgres as vectors
# One time operation
```
poetry run python -m src.db.ingest_knowledge
```
