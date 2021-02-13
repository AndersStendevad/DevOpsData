for a in `docker ps -a -q`
do
  echo "Stopping container - $a"
  docker stop $a
done