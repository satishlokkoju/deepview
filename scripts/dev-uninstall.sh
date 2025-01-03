#!/bin/bash

# First uninstall canvas_ux
pip uninstall -y canvas_ux

# Find and uninstall all canvas widget packages
for d in src/deepview_canvas/widgets/*/ ; do
    if [ -d "$d" ]; then
        NAME=$(basename "$d")
        case "$NAME" in
            canvas_*)
                pip uninstall -y "$NAME"
                ;;
        esac
    fi
done
