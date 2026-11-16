"""Runs INSIDE Blender:  blender -b --factory-startup --python backlot/bl/build.py -- spec.json

Builds a tabletop scene from a JSON spec written by backlot.model and renders it with Cycles to
multilayer EXR. The spec is the whole interface: sheets of cut paper (or card, or acetate) standing
in a row, lights among them, a camera with a real lens. See backlot/MANUAL.md for the spec.

World axes: X right, Z up, Y away from the camera. Design pixels (x right, y down) are mapped onto
each sheet at `ppm` pixels per millimetre, centred on the origin.
"""
import bpy, json, sys, math, os
from mathutils import Vector

spec = json.load(open(sys.argv[sys.argv.index('--') + 1]))
MM = .001

def lin(c, a=1.0):
    c = c.lstrip('#'); v = [int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in v) + (a,)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
R = spec.get('render', {})
sc.render.engine = 'CYCLES'
prefs = bpy.context.preferences.addons['cycles'].preferences
try:
    prefs.compute_device_type = R.get('device', 'OPTIX'); prefs.refresh_devices()
    for d in prefs.devices:
        d.use = d.type == prefs.compute_device_type
    sc.cycles.device = 'GPU'
except Exception as e:
    print('GPU unavailable, using CPU:', e); sc.cycles.device = 'CPU'
sc.cycles.samples = R.get('samples', 96)
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = R.get('noise', .02)
sc.cycles.use_denoising = R.get('denoise', True)
sc.cycles.max_bounces = R.get('bounces', 10); sc.cycles.transmission_bounces = R.get('bounces', 10); sc.cycles.volume_bounces = 2
sc.cycles.caustics_refractive = False; sc.cycles.caustics_reflective = False
sc.render.resolution_x, sc.render.resolution_y = R.get('res', [1280, 720]); sc.render.resolution_percentage = 100
sc.render.film_transparent = False
vl = sc.view_layers[0]
vl.use_pass_z = True; vl.use_pass_object_index = True; vl.use_pass_emit = True; vl.use_pass_normal = True
if hasattr(sc.render.image_settings, 'media_type'):            # Blender 5: choose the media type first
    sc.render.image_settings.media_type = 'MULTI_LAYER_IMAGE'
sc.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
sc.render.image_settings.color_depth = '16'; sc.render.image_settings.exr_codec = 'ZIP'

W, H = spec['size']; ppm = spec.get('ppm', 4.0)
def P(x, y):                                           # design pixel -> sheet-local metres
    return ((x - W / 2) / ppm * MM, (H / 2 - y) / ppm * MM)

# ------------------------------------------------------------------ materials
def material(name, m):
    """kinds: paper (diffuse + translucent, fibre bump), card (opaque), acetate (clear tint), emit, mirror."""
    mat = bpy.data.materials.new(name); mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    kind = m.get('kind', 'paper'); colour = lin(m.get('color', '#f4f0e6'))
    def bump():
        tc = nt.nodes.new('ShaderNodeTexCoord'); n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = m.get('grain_scale', 900.0)
        n1.inputs['Detail'].default_value = 6.0
        mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1, 6, 1)
        nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], n1.inputs['Vector'])
        b = nt.nodes.new('ShaderNodeBump'); b.inputs['Strength'].default_value = m.get('grain', .12); b.inputs['Distance'].default_value = .0002
        nt.links.new(n1.outputs[0], b.inputs['Height'])
        return b, n1
    if kind in ('paper', 'card'):
        b, n1 = bump()
        d = nt.nodes.new('ShaderNodeBsdfDiffuse'); d.inputs['Color'].default_value = colour; d.inputs['Roughness'].default_value = .6
        nt.links.new(b.outputs['Normal'], d.inputs['Normal'])
        t = m.get('translucency', .45 if kind == 'paper' else 0.0)
        if t > 0:
            tr = nt.nodes.new('ShaderNodeBsdfTranslucent'); tc_ = lin(m.get('through', m.get('color', '#f4f0e6')))
            tr.inputs['Color'].default_value = tc_
            mix = nt.nodes.new('ShaderNodeMixShader'); mix.inputs['Fac'].default_value = t
            nt.links.new(d.outputs[0], mix.inputs[1]); nt.links.new(tr.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], out.inputs['Surface'])
        else:
            nt.links.new(d.outputs[0], out.inputs['Surface'])
    elif kind == 'acetate':
        p = nt.nodes.new('ShaderNodeBsdfPrincipled'); p.inputs['Base Color'].default_value = colour
        p.inputs['Transmission Weight'].default_value = 1.0; p.inputs['Roughness'].default_value = m.get('roughness', .05); p.inputs['IOR'].default_value = 1.3
        p.inputs['Thin Wall'].default_value = 1.0 if 'Thin Wall' in p.inputs else 0
        nt.links.new(p.outputs[0], out.inputs['Surface'])
    elif kind == 'emit':
        e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Strength'].default_value = m.get('strength', 5.0)
        if 'stops' in m:                               # a vertical gradation, bottom (0) to top (1)
            tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); ramp = nt.nodes.new('ShaderNodeValToRGB')
            nt.links.new(tc.outputs['Generated'], sep.inputs[0]); nt.links.new(sep.outputs[m.get('axis', 'Y')], ramp.inputs['Fac'])
            cr = ramp.color_ramp
            for i, (pos, c) in enumerate(m['stops']):
                el = cr.elements[i] if i < 2 else cr.elements.new(pos)
                el.position = pos; el.color = lin(c)
            nt.links.new(ramp.outputs['Color'], e.inputs['Color'])
        else:
            e.inputs['Color'].default_value = colour
        nt.links.new(e.outputs[0], out.inputs['Surface'])
    elif kind == 'mirror':
        p = nt.nodes.new('ShaderNodeBsdfPrincipled'); p.inputs['Base Color'].default_value = colour; p.inputs['Metallic'].default_value = 1; p.inputs['Roughness'].default_value = m.get('roughness', .2)
        nt.links.new(p.outputs[0], out.inputs['Surface'])
    return mat

MATS = {k: material(k, v) for k, v in spec.get('materials', {}).items()}
if 'paper' not in MATS:
    MATS['paper'] = material('paper', {'kind': 'paper'})
OBJ = {}

# ------------------------------------------------------------------ sheets cut from 2D patterns
for i, L in enumerate(spec.get('sheets', [])):
    cu = bpy.data.curves.new(L['name'], 'CURVE'); cu.dimensions = '2D'; cu.fill_mode = 'BOTH'
    cu.extrude = L.get('thickness', .25) * MM / 2
    for c in L['cuts']:
        pts = c['pts']
        sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
        for p, (x, y) in zip(sp.points, pts):
            u, v = P(x, y); p.co = (u, v, 0, 1)
        sp.use_cyclic_u = True
    ob = bpy.data.objects.new(L['name'], cu); sc.collection.objects.link(ob)
    ox, oz = L.get('offset', [0, 0])
    ob.rotation_euler = (math.pi / 2 + math.radians(L.get('tilt', 0)), 0, math.radians(L.get('turn', 0)))
    ob.location = (ox * MM, L['depth'] * MM, oz * MM)
    ob.data.materials.append(MATS[L.get('material', 'paper')]); ob.pass_index = i + 1
    OBJ[L['name']] = ob

# ------------------------------------------------------------------ plain panels (back light, walls, floor)
for Pn in spec.get('panels', []):
    w, h = Pn['size']
    me = bpy.data.meshes.new(Pn['name'])
    me.from_pydata([(-w / 2 * MM, 0, -h / 2 * MM), (w / 2 * MM, 0, -h / 2 * MM), (w / 2 * MM, 0, h / 2 * MM), (-w / 2 * MM, 0, h / 2 * MM)], [], [(0, 1, 2, 3)])
    ob = bpy.data.objects.new(Pn['name'], me); sc.collection.objects.link(ob)
    ob.location = [v * MM for v in Pn.get('pos', [0, 0, 0])]
    ob.rotation_euler = [math.radians(a) for a in Pn.get('rot', [0, 0, 0])]
    ob.data.materials.append(MATS[Pn['material']])
    if Pn.get('hidden_from_camera'): ob.visible_camera = False
    OBJ[Pn['name']] = ob

# ------------------------------------------------------------------ lights
for Lt in spec.get('lights', []):
    li = bpy.data.lights.new(Lt['name'], Lt.get('type', 'POINT').upper())
    li.energy = Lt.get('power', 1.0); li.color = lin(Lt.get('color', '#ffffff'))[:3]
    if li.type in ('POINT', 'SPOT'): li.shadow_soft_size = Lt.get('radius', 1.0) * MM
    if li.type == 'SPOT': li.spot_size = math.radians(Lt.get('cone', 30)); li.spot_blend = Lt.get('blend', .3)
    if li.type == 'AREA':
        li.shape = 'RECTANGLE'; li.size, li.size_y = Lt.get('size', [10, 10])[0] * MM, Lt.get('size', [10, 10])[1] * MM
    ob = bpy.data.objects.new(Lt['name'], li); sc.collection.objects.link(ob)
    ob.location = [v * MM for v in Lt['pos']]
    if 'look' in Lt:
        ob.rotation_euler = (Vector([v * MM for v in Lt['look']]) - ob.location).to_track_quat('-Z', 'Y').to_euler()
    elif 'rot' in Lt:
        ob.rotation_euler = [math.radians(a) for a in Lt['rot']]
    OBJ[Lt['name']] = ob

# ------------------------------------------------------------------ air (haze inside the box, so beams show)
if spec.get('haze'):
    Hz = spec['haze']; bpy.ops.mesh.primitive_cube_add(size=1); cube = bpy.context.object; cube.name = 'haze'
    cube.scale = [v * MM for v in Hz['size']]; cube.location = [v * MM for v in Hz.get('pos', [0, 0, 0])]
    mat = bpy.data.materials.new('haze'); mat.use_nodes = True; nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); vsc = nt.nodes.new('ShaderNodeVolumeScatter')
    vsc.inputs['Density'].default_value = Hz.get('density', 2.0); vsc.inputs['Anisotropy'].default_value = Hz.get('anisotropy', .3)
    vsc.inputs['Color'].default_value = lin(Hz.get('color', '#ffffff'))
    nt.links.new(vsc.outputs[0], out.inputs['Volume']); cube.data.materials.append(mat); cube.visible_shadow = True
    OBJ['haze'] = cube

# ------------------------------------------------------------------ world and camera
world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes.get('Background') or world.node_tree.nodes.new('ShaderNodeBackground')
bg.inputs['Color'].default_value = lin(spec.get('ambient', {}).get('color', '#101216')); bg.inputs['Strength'].default_value = spec.get('ambient', {}).get('strength', .0)
C = spec['camera']
cam = bpy.data.cameras.new('cam'); cam.lens = C.get('lens', 85); cam.sensor_width = 36
cam.clip_start = .01; cam.clip_end = 50
cob = bpy.data.objects.new('cam', cam); sc.collection.objects.link(cob); sc.camera = cob
cob.location = [v * MM for v in C['pos']]
target = bpy.data.objects.new('target', None); sc.collection.objects.link(target); target.location = [v * MM for v in C.get('look', [0, 0, 0])]
tc = cob.constraints.new('TRACK_TO'); tc.target = target; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
OBJ['cam'] = cob; OBJ['target'] = target
if C.get('fstop'):
    cam.dof.use_dof = True; cam.dof.aperture_fstop = C['fstop']
    focus = bpy.data.objects.new('focus', None); sc.collection.objects.link(focus); focus.location = [v * MM for v in C.get('focus', C.get('look', [0, 0, 0]))]
    cam.dof.focus_object = focus; OBJ['focus'] = focus

# ------------------------------------------------------------------ animation: keys on any object or its data
for A in spec.get('anim', []):
    ob = OBJ[A['target']]; holder = ob.data if A['path'].startswith('data.') else ob
    path = A['path'][5:] if A['path'].startswith('data.') else A['path']
    scale = MM if path == 'location' else (math.pi / 180 if 'rotation' in path else 1.0)
    for f, v in A['keys']:
        val = [x * scale for x in v] if isinstance(v, list) else v * scale
        if A.get('index') is not None:
            cur = list(getattr(holder, path)); cur[A['index']] = val; setattr(holder, path, cur)
            holder.keyframe_insert(path, index=A['index'], frame=f)
        else:
            setattr(holder, path, val); holder.keyframe_insert(path, frame=f)
    ad = holder.animation_data
    if ad and ad.action:
        try:
            curves = [fc for layer in ad.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
        except Exception:
            curves = list(getattr(ad.action, 'fcurves', []))
        for fc in curves:
            for kp in fc.keyframe_points: kp.interpolation = A.get('interp', 'LINEAR')

# ------------------------------------------------------------------ render
out = R['out']; os.makedirs(out, exist_ok=True)
if R.get('save_blend'):
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'scene.blend'))
for f in R.get('frames', [1]):
    sc.frame_set(f)
    sc.render.filepath = os.path.join(out, f'f_{f:04d}.exr')
    bpy.ops.render.render(write_still=True)
    print('RENDERED', f, flush=True)
