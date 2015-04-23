# Run as: blender -b -P <this_script> -- <mesh.obj>
import bpy, sys, os

argv = sys.argv
argv = argv[argv.index("--") + 1:]

full_path = argv[0]
bpy.ops.import_scene.obj(filepath=full_path)
#bpy.ops.object.mode_set(mode='OBJECT')
#print(bpy.data.objects[:])
C = bpy.context
scene = bpy.context.scene
#bpy.ops.object.select_all(action='DESELECT')
obs = []
for ob in scene.objects:
    if ob.type == 'MESH':
        print('selecting'+ob.name)
        #scene.objects.link(ob)
        ob.select = True
        obs.append(ob)
    else: 
        ob.select = False
#print(C.scene.objects.active)
#print(bpy.data.objects[:])
C.scene.objects.active = obs[0]
bpy.ops.object.join()
print(scene.objects[:])
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')

bpy.ops.object.select_all(action='DESELECT')
C.scene.camera.select = True
mesh = list(filter(lambda x: x.type=='MESH', scene.objects[:]))[0]
C.scene.camera.constraints.new(type='LIMIT_DISTANCE')
C.scene.camera.constraints["Limit Distance"].target = mesh
C.scene.camera.constraints["Limit Distance"].distance = 5.0
C.scene.camera.constraints.new(type='TRACK_TO')
C.scene.camera.constraints["Track To"].target = list(filter(lambda x: x.type=='MESH', scene.objects[:]))[0]
C.scene.camera.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
C.scene.camera.constraints["Track To"].up_axis = 'UP_Z'

bpy.context.scene.render.filepath += full_path.split('/')[-1]

bpy.ops.render.render(write_still=True)

