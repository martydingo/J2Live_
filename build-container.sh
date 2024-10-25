VERSION=$1
docker buildx build --platform linux/amd64 -t martydingo/j2live:$1 --push .