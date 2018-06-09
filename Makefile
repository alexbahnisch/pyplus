IMAGE_NAME=alexbahnisch/pyplus
VIRTUAL_ENV=${WORKON_HOME}/PyPlus36

clean:
	-rm -rf .venv

docs-build: docs-make
	.venv/Scripts/mkdocs build --clean --strict

docs-clean:
	rm -f ./docs/index.md
	rm -rf ./site

docs-deploy: docs-make
	mkdocs gh-deploy --clean --force

docs-make: docs-clean
	cp ./README.md ./docs/index.md
	sed -i -e '/\[comment\]: <> (DeleteStart)/,/\[comment\]: <> (DeleteEnd)/d' ./docs/index.md

docs-serve: docs-make
	.venv/Scripts/mkdocs serve --dev-addr localhost:8000 --livereload

install:
	.venv/Scripts/pip install .[develop]

test:
	.venv/Scripts/python setup.py test

tox:
	.venv/Scripts/tox

updgrade:
	.venv/Scripts/pip uninstall --yes pyplus
	.venv/Scripts/pip install .

venv:
	python -m venv .venv
