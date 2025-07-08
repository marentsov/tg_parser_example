install:
		pip install uv
		uv venv
		uv pip install -r requirements.txt
parse:
		uv run main.py
dev:
		uv run manage.py runserver
render-start:
		uv run gunicorn parserexample.wsgi