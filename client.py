import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv('.env', usecwd=True))
from mmcore.gql.client import GQLReducedQuery, GQLClient, GQL_PLATFORM_URL


class TestQuery(GQLReducedQuery):
    client = GQLClient(url=f"http://localhost:{os.getenv('CXM_SERVICE_PORT')}{os.getenv('CXM_API_PREFIX')}", headers={})
class TestQuery3(GQLReducedQuery):
    client = GQLClient(url=f"http://51.250.100.3:{os.getenv('CXM_SERVICE_PORT')}{os.getenv('CXM_API_PREFIX')}", headers={})


query = TestQuery(
    # language=GraphQL
    """
    query {
  rootless {
    object {
      name
      children {
        ... on GqlGroup {
          children {
            ... on GqlObject3D {
              children {
                ... on GqlGeometry {
                  name
                  geometry
                  material
                  layers
                  castShadow
                  receiveShadow
                  type
                  uuid
                  userData {
                    properties
                  }
                  matrix
                }
              }
              layers
              matrix
              name
              type
              uuid
              userData {
                properties
              }

            }
          }
          name
          matrix
          layers
          type
          uuid
          userData {
            gui {
              colors
              id
              key
              require
              name
            }
            properties
          }
        }
      }
      layers
      matrix
      receiveShadow
      type
      uuid
    }
    geometries {
      data {
        ... on Data1 {

          attributes {
            ... on Attributes3 {

              normal {
                array
                itemSize
                normalized
                type
              }
              position {
                array
                itemSize
                normalized
                type
              }
            }
          }
        }
      }
      type
      uuid
    }
    metadata {
      generator
      type
      version
    }
    materials {
      ... on MeshPhongMaterial {
        uuid
        color
        depthFunc
        colorWrite
        depthTest
        depthWrite
        emissive
        flatShading
        name
        reflectivity
        refractionRatio
        shininess
        side
        specular
        stencilFail
        stencilFunc
        type
        stencilZPass
        stencilZFail
        stencilWriteMask
        stencilWrite
        stencilRef
        stencilFuncMask
      }
    }
  }
}

    """
)

class Client(GQLClient):
    url = GQL_PLATFORM_URL
    headers = {
        "content-type": "application/json",
        "X-Hasura-Role": "admin",
        "X-Hasura-Admin-Secret": "mysecretkey"
    }
class ClusterQuery(GQLReducedQuery):
    client = Client()


cluster_query = ClusterQuery(
    # language=GraphQL
    """
{
  test1 {
    rootless {
      object {
        name
        children {
          ... on GqlGroup {
            children {
              ... on GqlObject3D {
                children {
                  ... on GqlGeometry {
                    name
                    geometry
                    material
                    layers
                    castShadow
                    receiveShadow
                    type
                    uuid
                    userData {
                      properties
                    }
                    matrix
                  }
                }
                layers
                matrix
                name
                type
                uuid
                userData {
                  properties
                }
              }
            }
            name
            matrix
            layers
            type
            uuid
            userData {
              gui {
                colors
                id
                key
                require
                name
              }
              properties
            }
          }
        }
        layers
        matrix
        receiveShadow
        type
        uuid
      }
      geometries {
        data {
          ... on Data1 {
            attributes {
              ... on Attributes3 {
                normal {
                  array
                  itemSize
                  normalized
                  type
                }
                position {
                  array
                  itemSize
                  normalized
                  type
                }
              }
            }
          }
        }
        type
        uuid
      }
      metadata {
        generator
        type
        version
      }
      materials {
        ... on MeshPhongMaterial {
          uuid
          color
          depthFunc
          colorWrite
          depthTest
          depthWrite
          emissive
          flatShading
          name
          reflectivity
          refractionRatio
          shininess
          side
          specular
          stencilFail
          stencilFunc
          type
          stencilZPass
          stencilZFail
          stencilWriteMask
          stencilWrite
          stencilRef
          stencilFuncMask
        }
      }
    }
  }
}

""")

test_query2 = TestQuery(
    # language=GraphQL
    """
    query MyQuery {
      rootlessByName(name: "Панель 600х400") {
        object {
          name
          uuid
          children {
            ... on GqlGeometry {
              name
              uuid
              type
              receiveShadow
              matrix
              material
              layers
              geometry
              castShadow
            }
          }
          layers
          matrix
          receiveShadow
          type
          userData {
            properties
          }
        }
        geometries {
          type
          uuid
          data {
            ... on Data1 {
        
              attributes {
                ... on Attributes3 {
                 
                  normal {
                    array
                    itemSize
                    normalized
                    type
                  }
                  position {
                    itemSize
                    normalized
                    type
                    array
                  }
                }
              }
            }
          }
        }
        materials {
          ... on MeshPhongMaterial {
            uuid
            color
            colorWrite
            depthFunc
            depthTest
            emissive
            depthWrite
            flatShading
            name
            opacity
            reflectivity
            refractionRatio
            shininess
            side
            specular
            stencilFail
            type
            transparent
            stencilZFail
            stencilZPass
            stencilWriteMask
            stencilWrite
            stencilRef
            stencilFuncMask
            stencilFunc
          }
        }
        metadata {
          generator
          type
          version
        }
      }
    }
    """)
test_query3 = TestQuery3("""
{ root }
""")
if __name__ == "__main__":
    import json

    with open("data/model.json", "w") as f:
        json.dump(test_query3(), f, ensure_ascii=False)
