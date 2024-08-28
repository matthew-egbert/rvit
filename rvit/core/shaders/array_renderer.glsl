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
attribute vec2     v_tc0;

/* uniform variables */
uniform mat4       modelview_mat;
uniform mat4       projection_mat;
uniform vec4       color;
uniform float      opacity;

{% if uses_gradient == True %}
uniform float      vmin; // scales gradient
uniform float      vmax; // scales gradient
{% endif %}

{{ vertex_shader_functions | join('\n') }}


void main() {
  frag_color = color * vec4(0.0, 1.0, 1.0, opacity);
  tex_coord0 = v_tc0;
  gl_Position = projection_mat * modelview_mat * vec4(v_pos.xy, 0.0, 1.0);
}

---FRAGMENT SHADER--- 
#version 120
#ifdef GL_ES
    precision highp float;
#endif

varying vec4 frag_color;
varying vec2 tex_coord0;

/* uniform texture samplers */
uniform sampler2D array_texture;

{% if uses_gradient == True -%}
uniform sampler2D gradient_texture;
{% endif -%}


void main (){
  // vec4 t = texture2D(texture0, tex_coord0);
  // //vec4 t = texture(texture0, tex_coord0);
  // //gl_FragColor = vec4(0.0,0.0,1.0,1.0);//t;//vec4(-t.r,t.r,0.0,1.0);
  // gl_FragColor = vec4(t);//vec4(-t.r,t.r,0.0,1.0);

  vec4 value = texture2D(array_texture, tex_coord0);
  //value.r = (value.r-vmin)/(vmax-vmin);

  {% if uses_gradient == True %}
  vec4 t = texture2D(gradient_texture, vec2(0.0,value.r));
  gl_FragColor = vec4(t.rgb,1.0);

  {% else %}
  gl_FragColor = vec4(value);
  {% endif %}

}

/* Local Variables: */
/* compile-command: "cd .. && python main.py" */
/* python-main-file: "main.py" */
/* python-working-dir: "../" */
/* End: */

