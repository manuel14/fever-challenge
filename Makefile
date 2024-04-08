run:
	python3 -m venv env && source env/bin/activate && pip install -r requirements.txt && uvicorn api.main:app --reload --port 5000

test:
	python3 -m venv env && source env/bin/activate && pip install -r requirements.txt && python -m unittest -vv tests.test_api