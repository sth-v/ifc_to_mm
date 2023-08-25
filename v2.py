import json
import random
import uuid

import ifcopenshell
from OCC.Core.Tesselator import ShapeTesselator
from ifcopenshell.ifcopenshell_wrapper import SerializerSettings
from ifcopenshell import geom
from mmcore.addons.step import step_to_nodes, step_refcheck, p21,stepdct
from mmcore.base import AGroup, AMesh
from mmcore.geom.materials import ColorRGB
from mmcore.base.geom.utils import create_buffer_from_dict
from mmcore.gql.lang.parse import parse_simple_query
NAME="W1-W4"
import os

EXPORT_PATH="/Users/andrewastakhov/PycharmProjects/viewer_test_ifc_scene/tmp"


UUID=NAME.lower().replace("-","_")
mep=AGroup(name=NAME,uuid=UUID)
DISABLE_TRIANGULATION=True
NO_WIRE_INTERSECTION_CHECK=True

from ifcopenshell import geom


#with open("/Users/andrewastakhov/dev/SW_walls.ifc", "r", encoding="utf-8") as f:
##nodes=step_to_nodes(data.data)

#import dill
#with open("data/v2.pkl","wb") as fl:
#    dill.dump
mats={}
gms={}
colors={}
nms={}
def props(f):
    props = dict(context=f.data.context, type=f.data.type, parent_id=f.data.parent_id)
    for k in f.data.product.get_attribute_names():
        val=f.data.product.get_argument(k)


        props[k] = f'{val}'

    return props

from mmcore.base.registry import objdict, amatdict,ageomdict

cb=lambda nam:nam.split(":")[0]

def thr(source='/Users/andrewastakhov/dev/W1-W4.Ifc', path=EXPORT_PATH,prefix=NAME):
    fl = ifcopenshell.open(source)
    settings = geom.settings(USE_PYTHON_OPENCASCADE=True, DISABLE_TRIANGULATION=True,
                             NO_WIRE_INTERSECTION_CHECK=NO_WIRE_INTERSECTION_CHECK)

    itr = geom.iterate(file_or_filename=fl, settings=settings)
    for o in itr:

        try:
            _name = cb(o.data.name)
            if _name not in nms.keys():
                nms[_name] = AGroup(name=_name, uuid=_name)
                mep.add(nms[_name] )
                colors[_name] = ColorRGB(int(random.random() * 200), int(random.random() * 200),int(random.random() * 200)).decimal
                amatdict[hex(hash(_name))+"_mat"] = AMesh.material_type(uuid=hex(hash(_name))+"_mat", color=colors[_name])
            gmuid = uuid.uuid4().hex


            tess = ShapeTesselator(o.geometry)
            tess.Compute(compute_edges=False,
                         mesh_quality=1.0,
                         parallel=True)

            ageomdict[gmuid]=create_buffer_from_dict(json.loads(tess.ExportShapeToThreejsJSONString(gmuid)))

            nms[_name].add(AMesh(name=o.data.name, geometry=ageomdict[gmuid],material=amatdict[hex(hash(_name))+"_mat"], uuid=str(o.data.id), properties=props(o)))


        except Exception as err:
            print(err)
            pass
    dump_all_to_fs(path=path, prefix=prefix)
    print("All Done")
def dump_group(name):
    return nms[name].root()

def dump_all_to_fs(path="/Users/andrewastakhov/PycharmProjects/viewer_test_ifc_scene/tmp", prefix=NAME):
    if not os.path.exists(path + "/" + prefix):
        os.mkdir(path + "/" + prefix)
    for k, n in nms.items():
        if any([k=="", k is None]):

            k = f"Undefined-{uuid.uuid4().hex}"
        k=k.replace("/","-").replace("\\","-")
        n.dump(path+"/"+prefix+"/"+k + ".json")

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from mmcore.base.sharedstate import serve
serve.app.add_middleware(CORSMiddleware,allow_origins=['*'])
serve.app.add_middleware(GZipMiddleware)
if __name__=="__main__":

    import threading as th
    #main_th=th.Thread(target=thr, args=(itr,))
    #main_th.start()
    thr(source='/Users/andrewastakhov/dev/W1-W4.Ifc')
    #serve.start()
    #import IPython,mmcore
    #IPython.embed(header=f"[mmcore {mmcore.__version__()}]")