DOCKER_BUILDKIT=1 docker build --platform amd64 -t sthv/test-ifc-scene:latest .

docker tag sthv/test-ifc-scene  cr.yandex/crpfskvn79g5ht8njq0k/contextmachine-test-ifc-scene:latest
#docker push cr.yandex/crpfskvn79g5ht8njq0k/contextmachine-test-ifc-scene:latest
