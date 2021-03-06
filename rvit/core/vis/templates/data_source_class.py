
class {{property_name}}(RVIVisualizer):
    """{{docstring}}
    """

    {{property_name}} = DataTargettingProperty('') #: {{docstring}}
    {{property_name}}_preprocess = StringProperty('') #: the preprocessor for {{property_name}}

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_{{property_name}}(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        {{property_name}} = value
        if {{property_name}} != '':
            ## old 'pointer' solution
            # s = 'self.{{variable_name}} = self.simulation.%s' % ({{property_name}})
            # exec(s)
            # s = 'self.n_elements = len(np.ravel(self.{{variable_name}}))'
            # exec(s)

            ## new get-data-function solution
            if not hasattr(self,'simulation'):
                self.simulation = App.get_running_app().get_simulation()        
            self.get_{{variable_name}}_command = f'self.{{variable_name}} = self.simulation.{value}; self.n_elements = len(np.ravel(self.{{variable_name}}))'

            ## the following line should be run every time the data should be
            ## fetched from its source; each time it is called, it populates the variables
            ##    self.{{variable_name}}
            ##    self.n_elements
            exec(self.get_{{variable_name}}_command)
            

            self.data_index_{{variable_name}} = self.n_data_sources
            self.n_data_sources += 1
        {% if vertex_shader_functions is defined -%}
        self.shader_substitutions['vertex_shader_functions'].append({{vertex_shader_functions}})
        {% endif -%}
        {{ on_set }}
        self.shader_substitutions['attributes'].append('{{attribute_defn}}')
        {% if fmt is defined -%}
        self.fmt.append( {{fmt}} )
        {% endif -%}
        self.format_has_changed = True

    def update(self):
        super().update()
        if hasattr(self,'{{variable_name}}'):
            ## gets data from source and puts it in self.{{variable_name}}
            exec(self.get_{{variable_name}}_command)
            data = np.repeat(
                np.array(self.{{variable_name}}, dtype=np.float32),
                self.vertices_per_datum)
            if hasattr(self,'preprocess_{{variable_name}}') :
                data = self.preprocess_{{variable_name}}(data)
            self.data_to_shader[:,self.data_index_{{variable_name}}] = data.ravel()

    def on_{{property_name}}_preprocess(self, obj, value):
        s = 'self.preprocess_{{variable_name}} = %s' % (value)
        exec(s)
    
