IMAGE_NAME=alexbahnisch/pyplus
VIRTUAL_ENV=${WORKON_HOME}/PyPlus36

clean:
	-rm -rf .venv

docs-make:
	cp ./README.md ./docs/index.md
	sed -i -e 's/\[comment\]: <> (DocsUrlPlacemarker)//g' ./docs/index.md

docs-build:
	.venv/Scripts/mkdocs build --clean --strict

docs-serve:
	.venv/Scripts/mkdocs serve --dev-addr 0.0.0.0:8000 --livereload --strict

install:
	.venv/Scripts/pip install .[develop]

test:
	.venv/Scripts/python setup.py test

test-tox:
	.venv/Scripts/tox

updgrade:
	.venv/Scripts/pip uninstall --yes pyplus
	.venv/Scripts/pip install .

venv:
	python -m venv .venv
