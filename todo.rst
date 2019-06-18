High-priority
==============
Make color_data take different formats (RGBA vs. color index).

The shader needs to depend upon which properties are set.

on_color_data should be replaced with

  on_color_data_1D (although! this could be automatically determined by the
  shape of the data stream?)
  on_color_data_3D
  on_color_data_4D

and new properties should be added

  color_1D_scheme: viridis
  color_3D_scheme: RGB
  color_4D_scheme: HSVA

and these should dynamically modify the shader code accordingly  

Low-priority
============

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
