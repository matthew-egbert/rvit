=============
High-priority
=============


unique_name
-----------
Why did I say that this has to be specified last. Make that not the case!

Have considered improvement in terms of how data is read (probably in all cases
this should be a call.. "get_values!" not the name of the variable. 

===============
Medium-priority
===============

The point-renderer should have color configuration widgets in the ctl panel.

============
Low-priority
============

====
Bugs
====

xy_bounds component does not seem to listen to .rvit configurations (has to be
set using GUI)


putting point size before x_data causes crash

====
Fixed
====

- When people install rvit _without_ OpenGL, PointRenderer doesn't load (an
unhelpful error saying it (point_renderer) doesn't exist is given). This needs
to be fixed.







PointRenderer renders as squares on some versions of openGL
===========================================================

- For some OpenGL? GLSL? versions? the point renderer sometimes draws as squares rather than as points. In this case it is also requiring me to pas a tex_coord0. I don't know if these two issues are related

[INFO   ] [GL          ] OpenGL version <b'3.0 Mesa 18.2.8'>
[INFO   ] [GL          ] OpenGL vendor <b'Intel Open Source Technology Center'>
[INFO   ] [GL          ] OpenGL renderer <b'Mesa DRI Intel(R) UHD Graphics 620 (Kabylake GT2) '>
[INFO   ] [GL          ] OpenGL parsed version: 3, 0
[INFO   ] [GL          ] Shading version <b'1.30'>
