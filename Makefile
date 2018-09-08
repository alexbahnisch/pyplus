
clean:
	-rm -rf .coverage .pytest_cache build dist site src/main/pyplus.egg-info

clean-all: clean
	-rm -rf .tox .venv

docs-build: docs-make
	.venv/Scripts/mkdocs build --clean --strict

docs-clean:
	rm -f ./docs/index.md
	rm -rf ./site

docs-deploy: docs-make
	mkdocs gh-deploy --clean --force --remote-name https://$(GITHUB_TOKEN)@github.com/alexbahnisch/pyplus.git

docs-make: docs-clean
	cp ./README.md ./docs/index.md
	sed -i -e '/<!---StartDelete--->/,/<!---EndDelete--->/d' ./docs/index.md

docs-serve: docs-make
	.venv/Scripts/mkdocs serve --dev-addr localhost:8000 --livereload

init:
	python -m venv .venv
	.venv/Scripts/python -m pip install --upgrade pip

install:
	.venv/Scripts/pip install -e .[develop]

test:
	.venv/Scripts/python setup.py test

tox:
	.venv/Scripts/tox

uninstall:
	.venv/Scripts/pip uninstall pyplus[develop]
