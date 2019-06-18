

class LineRenderer(SimpleRenderer,xy_bounds,x_data,y_data,color1d_data,size_data):
    """The LineRenderer is ..."""

    def loadShaders(self,subs={}):
        super().loadShaders('lines',subs=subs)
