components := deepview deepview_data deepview_tensorflow deepview_torch deepview_canvas

# Clean directories for different components
python_clean_dirs := src/deepview*/dist src/deepview_canvas/*/dist */.pytest_cache src/deepview*/.pytest_cache .pytest_cache .mypy_cache
python_clean_dirs += src/deepview/**/__pycache__ src/deepview/*/**/__pycache__ src/deepview/*/*/**/__pycache__
python_clean_dirs += src/deepview_canvas/**/__pycache__ src/deepview_canvas/*/**/__pycache__ src/deepview_canvas/*/*/**/__pycache__ 
python_clean_dirs += src/deepview_tensorflow/**/__pycache__ src/deepview_tensorflow/*/**/__pycache__ src/deepview_canvas/canvas_ux/build
python_clean_dirs += src/deepview_data/**/__pycache__ src/deepview_data/*/**/__pycache__
python_clean_dirs += src/deepview_torch/**/__pycache__ src/deepview_torch/*/**/__pycache__ __pycache__

js_clean_dirs := src/deepview_canvas/node_modules src/deepview_canvas/*/node_modules src/deepview_canvas/*/*/node_modules
js_clean_dirs += src/deepview_canvas/canvas_viz/storybook-static src/deepview_canvas/widgets/*/dist
js_clean_dirs += src/deepview_canvas/widgets/*/build src/deepview_canvas/widgets/*/*/dist 
js_clean_dirs += src/deepview_canvas/widgets/*/*/standalone src/deepview_canvas/widgets/*/*/labextension
js_clean_dirs += src/deepview_canvas/widgets/*/*/lib src/deepview_canvas/*/*/lib

docs_clean_dirs := docs/_build docs/_static/storybook-static

test_clean_dirs := junit*.xml coverage .coverage* notebooks/.verify notebooks/.ipynb_checkpoints

env_clean_dirs := .env*

export PIP_INDEX_URL := https://pypi.org/simple

################
# INSTALLATION #
################
all: install

install: cmd = install -s --deps=develop --extras=notebook,image,dimreduction,dataset-report,tf
install: $(components)
	@echo "Done installing DeepView."

$(components):
	@if [ "$@" = "deepview_canvas" ]; then \
		sh ./scripts/dev-install.sh; \
	else \
		pip install -U flit$(FLIT_VER) flit_core$(FLIT_VER) && \
		flit -f src/$@/pyproject.toml $(cmd); \
	fi

uninstall-component:
	@if [ "$(component)" = "deepview_canvas" ]; then \
		sh ./scripts/dev-uninstall.sh; \
	else \
		pip uninstall -y $(component); \
	fi

uninstall:
	@for comp in $(components); do \
		make uninstall-component component=$$comp; \
	done

########
# TEST #
########
test: test-pytest test-notebooks
	@echo "Done running tests."

test-all: test-pytest-all test-notebooks test-canvas
	@echo "Done running tests."

test-canvas:
	@echo "Running canvas tests."
	@cd src/deepview_canvas && yarn test

test-pytest:
	@echo "Running pytest."
	@pytest

test-pytest-all:
    # runs all tests including ones marked @pytest.mark.slow (see conftest.py)
	@echo "Running pytest (all)."
	@pytest --runslow --durations=10

test-smoke:
	@echo "Running pytest smoke tests."
	@pytest -m "not regression"

test-notebooks:
	@echo "Converting notebooks"
	@jupyter nbconvert --to python --output-dir notebooks/.verify notebooks/*/*.ipynb
	@echo "Check notebooks"
	@mypy notebooks/.verify


#########
# OTHER #
#########
doc:
	@cd src/deepview_canvas && yarn install && yarn run build:storybook
	@rm -rf docs/_static/storybook-static
	@cp -r src/deepview_canvas/canvas_viz/storybook-static docs/_static/
	@cp resources/deepviewlogo.png docs/_static/
	@pip install -r docs/requirements.txt
	@$(MAKE) -C docs html
	@echo "\nOpen docs/_build/html/index.html to get started.\n"

clean: clean-python clean-js clean-docs clean-test clean-env
	@echo "All clean targets executed successfully"

clean-python:
	@echo "Cleaning Python build and cache files..."
	@-rm -rf $(python_clean_dirs)

clean-js:
	@echo "Cleaning JavaScript/TypeScript build files..."
	@-rm -rf $(js_clean_dirs)

clean-docs:
	@echo "Cleaning documentation build files..."
	@-rm -rf $(docs_clean_dirs)

clean-test:
	@echo "Cleaning test artifacts..."
	@-rm -rf $(test_clean_dirs)

clean-env:
	@echo "Cleaning environment files..."
	@-rm -rf $(env_clean_dirs)

.PHONY: all install install-tf1-gpu install-tf1 uninstall-component uninstall $(components) test test-all test-pytest test-pytest-all test-smoke test-notebooks doc clean clean-python clean-js clean-docs clean-test clean-env
