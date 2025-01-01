yarn
yarn workspace @betterwithdata/canvas_viz build
yarn workspace @betterwithdata/canvas-ui build

for d in widgets/* ; do
	cd $d
  yarn watch & pid=$!
  PID_LIST+=" $pid";
done

trap "kill $PID_LIST" SIGINT

echo "Parallel processes have started.";

wait $PID_LIST

echo
echo "All processes complete.";
