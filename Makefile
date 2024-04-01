run:
	python3 -m venv env && source env/bin/activate && pip install -r requirements.txt && flask --app events_api run

install:
	python3 -m venv env && source env/bin/activate && pip install -r requirements.txt

test:
	python3 -m venv env && source env/bin/activate && python -m unittest -vv tests.test_api