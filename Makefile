serve:
	FLASK_ENV=development FLASK_APP=main flask run

es_init:
	./scripts/create_es_index.sh

es_seed:
	./scripts/seed_es.py
