

class {{property_name}}(RVIElement):
    """{{docstring}}
    """

    {{property_name}} = StringProperty('') #: {{docstring}}
    {{property_name}}_preprocess = StringProperty('') #: the preprocessor for {{property_name}}

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_{{property_name}}(self, obj, value):
        self.{{property_name}} = value
        if self.simulation is not None and self.{{property_name}} != '':
            s = 'self.{{variable_name}} = self.simulation.%s' % (self.{{property_name}})
            exec(s)
            s = 'self.n_elements = len(self.{{variable_name}})'
            exec(s)
            self.data_index_{{variable_name}} = self.n_data_streams
            self.n_data_streams += 1
        {% if vertex_shader_functions is defined -%}
        self.shader_substitutions['vertex_shader_functions'].append({{vertex_shader_functions}})
        {% endif -%}
        {{ on_set }}
        self.shader_substitutions['attributes'].append('{{attribute_defn}}')
        self.fmt.append( {{fmt}} )
        self.format_has_changed = True

    def update(self):
        super().update()
        if hasattr(self,'{{variable_name}}'):
            data = np.array(self.{{variable_name}}, dtype=np.float32)#.reshape(N, 1)
            if hasattr(self,'preprocess_{{variable_name}}') :
                data = self.preprocess_{{variable_name}}(data)
            self.data_to_shader[:,self.data_index_{{variable_name}}] = data.ravel()

    def on_{{property_name}}_preprocess(self, obj, value):
        s = 'self.preprocess_{{variable_name}} = %s' % (value)
        exec(s)

    
