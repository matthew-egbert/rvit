import re
import os
from jinja2 import Environment, PackageLoader, FileSystemLoader

packageEnv = Environment(
    loader=PackageLoader('rvit', 'shaders'),
    autoescape=select_autoescape(default=False, default_for_string=False)
)

systemEnv = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(default=False, default_for_string=False)
)

envs = {True: packageEnv, False: systemEnv}

# Utilities
def loadShaders(fn, substitutions, packaged=True):
    template = envs[packaged].getTemplate(fn)
    shader_text = template.render(substitutions)
    ss = shader_text.split('---VERTEX SHADER---')
    ss = ss[1].split('---FRAGMENT SHADER---')
    vertex_shader = str(ss[0])
    frag_shader = str(ss[1])
    return {'vs': vertex_shader,
            'fs': frag_shader}
