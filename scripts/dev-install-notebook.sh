yarn
yarn workspace @betterwithdata/canvas_viz build
yarn workspace canvas-ux build
pip3 install -e "canvas_ux[docs]"
jupyter nbextension install --sys-prefix --symlink --overwrite --py canvas_ux
jupyter nbextension enable canvas_ux --py --sys-prefix