===============
API Reference
===============

API: Core
##########

.. autofunction:: rvit.core.init_rvit.init_rvit


API: Visualizers
################

.. autosummary:: rvit.core.vis.rvi_element.RVIElement
   :nosignatures:
            
.. autosummary:: rvit.core.vis.point_renderer.PointRenderer
   :nosignatures:

.. autosummary:: rvit.core.vis.sprite_renderer.SpriteRenderer
   :nosignatures:      
      
.. autosummary:: rvit.core.vis.scalar_tracker.ScalarTracker
   :nosignatures:
      
.. autoclass:: rvit.core.vis.rvi_element.RVIElement
   :members: unique_name, show_controls, self_update, fps
   	  
.. autoclass:: rvit.core.vis.point_renderer.PointRenderer
   :members:
   :show-inheritance: True

.. autoclass:: rvit.core.vis.sprite_renderer.SpriteRenderer
   :members:
   :show-inheritance: True

.. autoclass:: rvit.core.vis.scalar_tracker.ScalarTracker
   :members:
   :show-inheritance: True
		      
		      
      
API: Components
###############
.. automodsumm:: rvit.core.vis.components
   :skip: BooleanProperty,NumericProperty,ObjectProperty,OptionProperty,RVIElement,StringProperty,DictProperty,ListProperty,Property,ConfigParserProperty,BoundedNumericProperty,VariableListProperty,AliasProperty,ReferenceListProperty,Window
   :nosignatures:

.. automodule:: rvit.core.vis.components
   :members:

API: Data Sources
#################
      
.. automodsumm:: rvit.core.vis.data_sources
   :skip:
      BooleanProperty,NumericProperty,ObjectProperty,OptionProperty,RVIElement,StringProperty,DictProperty,ListProperty,Property,ConfigParserProperty,BoundedNumericProperty,VariableListProperty,AliasProperty,ReferenceListProperty
   :nosignatures:

.. automodule:: rvit.core.vis.data_sources
   :members:


API: Interactors
################# 
.. autosummary:: rvit.core.int.rvi_button.RVIButton
   :nosignatures:

.. autoclass:: rvit.core.int.rvi_button.RVIButton
   :members: function 
      
