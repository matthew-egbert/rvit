---VERTEX SHADER---
#version 120
#ifdef GL_ES
    precision highp float;
#endif
 
/* Outputs to the fragment shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* vertex attributes */
{{ attributes | join('\n') }}

/* uniform variables */
uniform mat4       modelview_mat;
uniform mat4       projection_mat;
uniform vec4       color;

{{ vertex_shader_functions | join('\n') }}

vec3 hsv2rgb(vec3 c) {
  vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
  vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
  return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}


void main() {
  {% if 'attribute float color1D;' in attributes %}
  vec3 rgb = hsv2rgb(vec3(color1D,1.0,1.0));
  frag_color = vec4(rgb,color.w) ;
  {% else %}
  frag_color = color;
  {% endif %}
  
  {% if 'attribute float size;' in attributes %}
  gl_PointSize = size * {{point_size}};
  {% else %}
  gl_PointSize = {{point_size|default('1.0')}};
  {% endif %}

  tex_coord0 = vec2(0,0);
  vec2 v_pos = vec2(x,y);
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

void main (void){
  float a = step(0.5,2.0*(0.5-distance(vec2(0.5,0.5),gl_PointCoord))) * frag_color.a;
  // if(float(gl_PointCoord) == float(0.0)) {
  //   a = frag_color.a;
  // }
  a += float(float(gl_PointCoord) == float(0.0)) * frag_color.a;
  gl_FragColor = vec4(frag_color.rgb,a);
}
