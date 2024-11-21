from rvit.core.vis.simple_renderer_3d import SimpleRenderer3D


class LineRenderer3D(SimpleRenderer3D) :
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #self.shader_fn='line_renderer.glsl'

    def loadShaders(self,subs={}):
        super().loadShaders('lines',subs=subs)