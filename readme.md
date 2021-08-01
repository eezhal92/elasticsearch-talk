# elasticsearch-demo

This repo is a demo of an internal tech talk.

## Requirements
- docker (docker-engine v18.02.0+)
- python 3.8+ and pipenv
- make

## Running on your local

- Run elasticsearch and kibana
```
docker compose up
```

- In another shell, install dependencies
```
pipenv install
pipenv shell
```
- Run `make es_init` to create `journal-articles` index.
- Run `make es_seed` to scrape data and index them into `journal-articles` index.
- Run `make serve` to run web server. Head over to http://localhost:5000
- You can also open kibana at http://localhost:5601
