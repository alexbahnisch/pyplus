docs-build:
	cp ./README.md ./docs/index.md
	sed -i -e 's/\[comment\]: <> (DocsUrlPlacemarker)/Whoop/g' ./docs/index.md
	mkdocs build --clean --strict

docs-serve:
	mkdocs serve --dev-addr localhost:8000 --livereload --strict

docs-server:
	python -m

install:
	pip install -e .[docs]
