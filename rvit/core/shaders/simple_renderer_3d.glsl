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

{% if 'attribute float color1D;' in attributes %}
varying float frag_color1D;
{% endif %}

/* uniform variables */
uniform mat4       modelview_mat;
uniform mat4       projection_mat;
uniform vec4       color;
uniform float      vmin; // scales gradient
uniform float      vmax; // scales gradient

{{ vertex_shader_functions | join('\n') }}

vec3 hsv2rgb(vec3 c) {
  vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
  vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
  return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main() {
  {% if 'attribute float color1D;' in attributes %}
  //vec3 rgb = hsv2rgb(vec3(color1D,1.0,1.0));
  frag_color = color; //vec4(color1D,color1D,color1D,color.w);
  frag_color1D = color1D;
  {% else %}
  frag_color = color;
  {% endif %}
  
  {% if 'attribute float size;' in attributes %}
  gl_PointSize = size * {{point_size}};
  {% else %}
  gl_PointSize = {{point_size|default('1.0')}};
  {% endif %}

  tex_coord0 = vec2(0,0);
  vec3 v_pos = vec3(x,y,z);  
  gl_Position = projection_mat * modelview_mat * vec4(v_pos, 1.0);
  gl_PointSize *= 1.0-(0.0+0.95*(pow(gl_Position.z,2)*10.0 + 1.0))/2000;
}

---FRAGMENT SHADER---
#version 120
#ifdef GL_ES
    precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

{% if 'attribute float color1D;' in attributes %}
varying float frag_color1D;
{% endif %}

{% if uses_gradient == True %}
/* uniform texture samplers */
uniform sampler2D gradient_texture;
uniform float vmin; // scales gradient
uniform float vmax; // scales gradient
{% endif %}

void main (void){
  {% if uses_gradient == True %}
    float value = (frag_color1D-vmin)/(vmax-vmin);
    vec4 t = texture2D(gradient_texture, vec2(0.0,value));
    t.r*=frag_color.r;
    t.g*=frag_color.g;
    t.b*=frag_color.b;
    gl_FragColor = vec4(t.rgb,frag_color.a);
  {% else %}
    gl_FragColor = frag_color;
  {% endif %}
}
