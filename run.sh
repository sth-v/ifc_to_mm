#docker run --rm -p 0.0.0.0:4777:4777  -p 0.0.0.0:5777:5777 --tty --env HASURA_GQL_ENDPOINT=http://51.250.47.166:8080/v1/graphql  --name test-ifc-scene sthv/test-ifc-scene
eval "$(bin/load_dotenv .env)"
docker run --rm -p 0.0.0.0:8080:80  --tty --env HASURA_GQL_ENDPOINT=$HASURA_GQL_ENDPOINT --env CXM_API_PREFIX=$CXM_API_PREFIX --env CXM_APP_PORT=$CXM_APP_PORT --name test-ifc-scene sthv/test-ifc-scene
