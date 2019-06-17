High-priority
==============

* Rename all *Renderers to *Visualizers  


Low-priority
============
Make color_data take different formats (RGBA vs. color index)

====
Bugs
====

PointRenderer renders as squares on some versions of openGL
===========================================================

- For some OpenGL? GLSL? versions? the point renderer sometimes draws as squares rather than as points. In this case it is also requiring me to pas a tex_coord0. I don't know if these two issues are related

[INFO   ] [GL          ] OpenGL version <b'3.0 Mesa 18.2.8'>
[INFO   ] [GL          ] OpenGL vendor <b'Intel Open Source Technology Center'>
[INFO   ] [GL          ] OpenGL renderer <b'Mesa DRI Intel(R) UHD Graphics 620 (Kabylake GT2) '>
[INFO   ] [GL          ] OpenGL parsed version: 3, 0
[INFO   ] [GL          ] Shading version <b'1.30'>
