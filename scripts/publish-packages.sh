# BEFORE DEPLOY: Update the python package versions in Canvas and each widget's _version.py file.
python3 -m pip install twine
python3 -m pip install build
(cd src/deepview; rm -rf dist; python3 -m build;python3 -m twine upload --repository pypi dist/* )
(cd src/deepview_tensorflow; rm -rf dist; python3 -m build;python3 -m twine upload --repository pypi dist/* )
(cd src/deepview_data; rm -rf dist; python3 -m build;python3 -m twine upload --repository pypi dist/* )
(cd src/deepview_torch; rm -rf dist; python3 -m build;python3 -m twine upload --repository pypi dist/* )

cd src/deepview_canvas
yarn
yarn workspace @betterwithdata/canvas_viz build
(cd canvas_ux; rm -rf dist; yarn build:prod; python3 setup.py bdist_wheel; python3 setup.py sdist;python3 -m twine upload --repository pypi dist/* )
for d in widgets/* ; do
    # Skip if d is __init__.py or __pycache__
    if [ "$d" = "widgets/__init__.py" ] || [ "$d" = "widgets/__pycache__" ]; then
        continue
    fi

    # Check if the directory has a setup.py and package.json
    if [ -f "$d/setup.py" ] && [ -f "$d/package.json" ]; then
        (
            cd "$d"; rm -rf dist; yarn build:prod; python3 setup.py bdist_wheel; python3 setup.py sdist;python3 -m twine upload --repository pypi dist/* )
    fi
done
