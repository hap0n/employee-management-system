/docker-compose-wait && \
  alembic upgrade head && \
  watchmedo auto-restart --recursive --patterns="*.py" -- python src/api.py
