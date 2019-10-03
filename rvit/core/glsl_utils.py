import re
import os
from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape
from kivy.logger import Logger

packageEnv = Environment(
    loader=PackageLoader('rvit', 'core/shaders'),
    autoescape=select_autoescape(default=False, default_for_string=False)
)

systemEnv = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(default=False, default_for_string=False)
)

envs = {True: packageEnv, False: systemEnv}

# Utilities
def loadShaders(fn, template_variables, packaged=True):
    Logger.info('Loading shader:: %s'%(fn))
    template = envs[packaged].get_template(fn)
    shader_text = template.render(template_variables)
    ss = shader_text.split('---VERTEX SHADER---')
    ss = ss[1].split('---FRAGMENT SHADER---')
    vertex_shader = str(ss[0])
    frag_shader = str(ss[1])
    print(shader_text)
    # quit()
    return {'vs': vertex_shader,
            'fs': frag_shader}
