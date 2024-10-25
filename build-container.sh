VERSION=$1
docker buildx build --no-cache --platform linux/amd64 -t martydingo/j2live:$1 --push .
docker buildx build --platform linux/amd64 -t martydingo/j2live:latest --push .