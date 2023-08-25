import uuid

import dotenv
from OCC.Core.Tesselator import ShapeTesselator

dotenv.load_dotenv(".env")
from typing import Generic, TypeVar

import ifcopenshell

from ifcopenshell import geom


import mmcore.base.models.gql
from mmcore.base.basic import *
from mmcore.geom.tess import TessellateIfc

import os, uvicorn
import json

from mmcore.base import AMesh
from mmcore.base.geom.utils import create_buffer_from_dict
from mmcore.base.models.gql import MeshPhongMaterial

root_group = AGroup(name="root")
def mesh_from_threejs_json(jsn: dict, material: MeshPhongMaterial = None) -> AMesh:

        geom = jsn
        object_dict = geom["object"]
        object_dict.pop("material"), object_dict.pop("geometry")
        childs = None
        if "children" in object_dict.keys():
            childs = object_dict.pop("children")
        if material is None:
            material = MeshPhongMaterial(**geom["materials"][0])

        mesh = AMesh(geometry=create_buffer_from_dict(geom["geometries"][0]), material=material, **object_dict)
        if childs is not None:
            for i, m in enumerate(childs):
                child_mesh = mesh_from_threejs_json(m)
                mesh.__setattr__(f"part-{i}", child_mesh)
        return mesh
TYPE_CHECKING = False

T = TypeVar("T")

import OCC.Extend.DataExchange
def convertor(input_path, cpu_count=4):

    use_occ = True

    fl = ifcopenshell.open(input_path)

    settings = geom.settings(USE_PYTHON_OPENCASCADE=use_occ)
    dct = dict()
    for item in geom.iterate(file_or_filename=fl, settings=settings, num_threads=cpu_count):

        try:
            tess=TessellateIfc(item)



            root_group.add(tess.tessellate())

        except Exception as err:
            print("error", err)
    print("done")

    # subsyst = GroupRootFix(name="subsystem")
    # profile_1 = ObjectRootFix(name="Опорный профиль-1")
    # profile_1.inlay_profile = dct["Вставка в опорный профиль-1"]
    # profile_1.mesh = dct["Опорный профиль"]
    # subsyst.add(dct["Кронштейн-1"])
    # subsyst.add(profile_1)
    # face = GroupRootFix(name="face")
    # panel = ObjectRootFix(name="Панель 600х400")
    # panel.mesh = dct["Панель 600х400"]
    #
    # panel.spring_2_1 = dct["Пружина 2"]
    # panel.spring_2_2 = dct["Пружина 2-2"]
    #
    # panel2 = ObjectRootFix(name="Панель 600х400-2")
    # panel2.spring_2_1 = dct["Пружина 2-1"]
    # panel2.spring_2_2 = dct["Пружина 2-2"]
    # panel2.mesh = dct["Панель 600х400-1"]
    # mo = copy.deepcopy(panel2.matrix)
    # panel2.matrix = [-1, 0, 0, 0,
    #                0, 1, 0, 0,
    #                0, 0, 1, 0,
    #                0, 0, 0, 1
    #                ]

    # face.add(panel)
    # face.add(panel2)
    # print(panel2.matrix, panel.matrix)



from mmcore.geom.transform import Transform, XY_TO_YZ
from mmcore.gql.server.fastapi import MmGraphQlAPI
app = MmGraphQlAPI(gql_endpoint="/v2/graphql")


t = Transform()





@app.post(app.gql_endpoint)
def graphql_query_resolver(data: dict):

        ##print(data)
        # qt2 = parse_simple_query(data['query'])
        return {"data": {"root": root_group.root()}}



print(f'http://localhost:{os.getenv("CXM_SERVICE_PORT")}')

if __name__=="__main__":
    from mmcore.gql.lang.parse import parse_simple_query



    import os

    convertor("/Users/andrewastakhov/dev/W1-W4.Ifc", cpu_count=1)
    root_group.dump("W1-W4.json")
    from mmcore.base.sharedstate import serve
    serve.start()
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("CXM_SERVICE_PORT")), reload=False)
