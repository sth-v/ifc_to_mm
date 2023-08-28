import json
import random
import uuid
import os
import ifcopenshell
from ifcopenshell import geom
from OCC.Core.Tesselator import ShapeTesselator
from mmcore.base import AGroup, AMesh
from mmcore.geom.materials import ColorRGB
from mmcore.base.geom.utils import create_buffer_from_dict

NAME = "export"
EXPORT_PATH = f"{os.getcwd()}/tmp"


UUID = NAME.lower().replace("-","_")
mep = AGroup(name=NAME,uuid=UUID)
DISABLE_TRIANGULATION = True
NO_WIRE_INTERSECTION_CHECK = True



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

def thr(source, path=EXPORT_PATH,prefix=NAME):
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

def dump_all_to_fs(path, prefix=NAME):
    if not os.path.exists(path + "/" + prefix):
        os.mkdir(path + "/" + prefix)
    for k, n in nms.items():
        if any([k=="", k is None]):

            k = f"Undefined-{uuid.uuid4().hex}"
        k=k.replace("/","-").replace("\\","-")
        n.dump(path+"/"+prefix+"/"+k + ".json")


if __name__=="__main__":
    thr(source='/Users/andrewastakhov/dev/W1-W4.Ifc', prefix=NAME, path=EXPORT_PATH)
