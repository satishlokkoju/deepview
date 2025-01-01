# BEFORE DEPLOY: Update the python package versions in Canvas and each widget's _version.py file.

yarn
yarn workspace @betterwithdata/canvas_viz build
(cd canvas_ux; rm -rf dist; yarn build; python setup.py bdist_wheel; python setup.py sdist; twine upload dist/*)

for d in widgets/* ; do
	(cd $d; yarn build; rm -rf dist; python setup.py bdist_wheel; python setup.py sdist; twine upload dist/*)
done
