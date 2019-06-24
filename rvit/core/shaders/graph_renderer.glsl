---VERTEX SHADER---
#version 120
#ifdef GL_ES
    precision highp float;
#endif
 
/* Outputs to the fragment shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* vertex attributes */
attribute vec2     v_pos;
{{ attributes | join('\n') }}


/* uniform variables */
uniform mat4       modelview_mat;
uniform mat4       projection_mat;
uniform vec4       color;
uniform float      vmin; // scales gradient
uniform float      vmax; // scales gradient

void main() {
  frag_color = color;
  tex_coord0 = vec2(0.0,(v_pos.y-vmin)/(vmax-vmin));
  gl_Position = projection_mat * modelview_mat * vec4(v_pos.xy, 0.0, 1.0);
}

---FRAGMENT SHADER--- 
#version 120
#ifdef GL_ES
    precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* uniform texture samplers */
uniform sampler2D texture0;

uniform vec2 player_pos;
uniform vec2 window_size; // in pixels
void main (void){
  {% if uses_gradient == True %}
  vec4 t = texture2D(texture0, tex_coord0);
  gl_FragColor = vec4(t.rgb,1.0);
  {% else %}
  gl_FragColor = vec4(frag_color);
  {% endif %}

}

/* Local Variables: */
/* compile-command: "cd .. && python main.py" */
/* python-main-file: "main.py" */
/* python-working-dir: "../" */
/* End: */

