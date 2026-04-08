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

    shader_dir = '.rvit/shaders'
    if not os.path.isdir(shader_dir):
        os.makedirs(shader_dir)
    shader_path = os.path.join(shader_dir, '%s.shader'%(fn))
    with open(shader_path, 'w') as shader_file:
        shader_file.write('---VERTEX SHADER---\n')
        shader_file.write(vertex_shader)
        shader_file.write('\n---FRAGMENT SHADER---\n')
        shader_file.write(frag_shader)

    # print(shader_text)
    
    return {'vs': vertex_shader,
            'fs': frag_shader}
