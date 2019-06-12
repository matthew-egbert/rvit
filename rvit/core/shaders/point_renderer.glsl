---VERTEX SHADER---
#version 120
#ifdef GL_ES
    precision highp float;
#endif
 
/* Outputs to the fragment shader */
varying vec4 frag_color;

/* vertex attributes */
attribute vec2     v_pos;
{% if uses_color_data %}
attribute float    colors;
{% endif %}
{% if uses_size_data %}
attribute float    sizes;
{% endif %}

/* uniform variables */
uniform mat4       modelview_mat;
uniform mat4       projection_mat;
uniform vec4       color;

vec3 hsv2rgb(vec3 c) {
  vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
  vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
  return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main() {
  {% if uses_color_data %}
  vec3 rgb = hsv2rgb(vec3(colors,1.0,1.0));
  frag_color = vec4(rgb,color.w) ;
  {% else %}
  frag_color = color;
  {% endif %}

  {% if uses_size_data %}
  gl_PointSize = sizes * {{point_size}};
  {% else %}
  gl_PointSize = {{point_size}};
  {% endif %}
  
  gl_Position = projection_mat * modelview_mat * vec4(v_pos.xy, 0.0, 1.0);
}

---FRAGMENT SHADER---
#version 120
#ifdef GL_ES
    precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;

void main (void){
  float a = step(0.5,2.0*(0.5-distance(vec2(0.5,0.5),gl_PointCoord)));
  gl_FragColor = vec4(frag_color.rgba);
}

/* Local Variables: */
/* compile-command: "cd .. && python main.py" */
/* python-main-file: "main.py" */
/* python-working-dir: "../" */
/* End: */
