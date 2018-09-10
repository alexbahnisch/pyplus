
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
	.venv/Scripts/pydoc2markdown pyplus.abstract --output ./docs/abstract.md --usage-dir ./docs/usage/abstract
	.venv/Scripts/pydoc2markdown pyplus.common --output ./docs/common.md --usage-dir ./docs/usage/common
	.venv/Scripts/pydoc2markdown pyplus.data --output ./docs/data.md --usage-dir ./docs/usage/data
	.venv/Scripts/pydoc2markdown pyplus.decorators --output ./docs/decorators.md --usage-dir ./docs/usage/decorators
	.venv/Scripts/pydoc2markdown pyplus.json --output ./docs/json.md --usage-dir ./docs/usage/json
	.venv/Scripts/pydoc2markdown pyplus.object --output ./docs/object.md --usage-dir ./docs/usage/object
	.venv/Scripts/pydoc2markdown pyplus.parse --output ./docs/parse.md --usage-dir ./docs/usage/parse
	.venv/Scripts/pydoc2markdown pyplus.path --output ./docs/path.md --usage-dir ./docs/usage/path
	.venv/Scripts/pydoc2markdown pyplus.string --output ./docs/string.md --usage-dir ./docs/usage/string
	.venv/Scripts/pydoc2markdown pyplus.table --output ./docs/table.md --usage-dir ./docs/usage/table
	sed -i -e '/<!---StartDelete--->/,/<!---EndDelete--->/d' ./docs/index.md

docs-serve: docs-make
	.venv/Scripts/mkdocs serve --dev-addr localhost:8001 --livereload

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
