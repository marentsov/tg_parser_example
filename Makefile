install:
		pip install uv
		uv venv
		uv pip install -r requirements.txt
parse:
		uv run main.py