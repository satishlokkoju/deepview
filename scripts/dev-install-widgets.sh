for d in widgets/* ; do
	#pip3 install -e $d
	NAME=`basename $d`
	echo $NAME
	cd widgets/$NAME
	#jupyter labextension develop --overwrite widgets/$NAME
	pip uninstall $NAME -y
	#jlpm clean;jlpm install;jlpm run build;pip install .
	cd ../../
done
