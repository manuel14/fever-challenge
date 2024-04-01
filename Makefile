run:
	python3 -m venv env && source env/bin/activate && pip install -r requirements.txt && flask --app api.events_api run

test:
	python3 -m venv env && source env/bin/activate && python -m unittest -vv tests.test_api