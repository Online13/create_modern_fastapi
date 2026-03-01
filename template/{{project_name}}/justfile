# install ----------------------------------------------------------

i-dev packages:
    uv add --group dev {{packages}} 

# run ----------------------------------------------------------

start:
    uv run uvicorn main:app.api --reload --port 8000

# test ----------------------------------------------------------

test-unit:
    uv run pytest tests/unit/

test-coverage:
    uv run coverage run -m pytest tests/unit/
    uv run coverage report -m

test-clean:
    uv run pytest tests/clean