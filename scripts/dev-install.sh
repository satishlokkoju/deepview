#yarn
#yarn workspace @betterwithdata/canvas_viz build
#yarn workspace canvas-ux build
#pip3 install -e "canvas_ux[docs]"
#jupyter labextension develop --overwrite canvas_ux
cd canvas_viz
jlpm prebuild; jlpm ; jlpm install;jlpm build
cd ../canvas_ux
jlpm clean;jlpm install;jlpm run build;pip install .
cd ../widgets/canvas_list
jlpm clean;jlpm install;jlpm run build;pip install .



