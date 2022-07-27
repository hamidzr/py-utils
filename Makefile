default: add-video-dev

clean:
	rm -rf dist

build:
	pipenv run python -m build

publish: build
	pipenv run python -m twine upload dist/*

fmt:
	black .
