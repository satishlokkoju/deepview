#!/bin/bash
#yarn
#yarn workspace @betterwithdata/canvas_viz build
#yarn workspace canvas-ux build
#jupyter labextension develop --overwrite canvas_ux
pip install jupyterlab
cd src/deepview_canvas/canvas_viz
jlpm prebuild; jlpm ; jlpm install;jlpm build
cd ../canvas_ux
jlpm clean;jlpm install;jlpm run build;pip install .[test]
cd ../widgets/canvas_summary
jlpm clean;jlpm install;jlpm run build;pip install .
cd ../canvas_list
jlpm clean;jlpm install;jlpm run build;pip install .
cd ../canvas_scatterplot
jlpm clean;jlpm install;jlpm run build;pip install .
cd ../canvas_data_map
jlpm clean;jlpm install;jlpm run build;pip install .
cd ../canvas_familiarity
jlpm clean;jlpm install;jlpm run build;pip install .
cd ../canvas_duplicates
jlpm clean;jlpm install;jlpm run build;pip install .
