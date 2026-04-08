---VERTEX SHADER---
#version 120

#ifdef GL_ES
    precision highp float;
#endif
 
/* Outputs to the fragment shader */
varying vec4 frag_color;
varying vec2 tex_coord0;
varying float mde_color1d;

/* vertex attributes */
attribute float ll_ul_ur_lr;
{{ attributes | join('\n') }}

/* uniform variables */
uniform mat4       modelview_mat;
uniform mat4       projection_mat;
uniform vec4       color;
{% if uses_gradient == True %}
uniform float      vmin; // scales gradient
uniform float      vmax; // scales gradient
varying 
{% endif %}

{{ vertex_shader_functions | join('\n') }}

mat2 rotate2d(float _angle){
    return mat2(cos(_angle),-sin(_angle),
                sin(_angle),cos(_angle));
}

vec3 hsv2rgb(vec3 c) {
  vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
  vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
  return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main() {
  {% if 'attribute float color1D;' in attributes %}
  vec3 rgb = hsv2rgb(vec3(0.5+color1D,1.0,1.0));
  frag_color = vec4(rgb,color.w) ;
  mde_color1d = color1D;
  {% else %}
  frag_color = color;
  {% endif %}
  
  {% if 'attribute float size;' in attributes %}
  float r = size * {{sprite_size|default('1.0')}};
  {% else %}
  float r = {{sprite_size|default('1.0')}};
  {% endif %}

  {% if 'attribute float rot;' in attributes %}
  float theta = -rot;
  {% else %}
  float theta = 0.0;
  {% endif %}

  //frag_color = color;// * vec4(0.0, 1.0, 1.0, 0.5);
  vec2 v_pos = vec2(x,y);
  float ox = float(ll_ul_ur_lr > 1.0);
  float oy = float(ll_ul_ur_lr > 0.0 && ll_ul_ur_lr < 3.0);
  tex_coord0 = vec2(ox,oy);//v_tc0;
  vec2 o = rotate2d(theta)*vec2(r*ox-(r/2),
				r*oy-(r/2));
  
  v_pos += o;
  
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
varying float mde_color1d;

/* uniform texture samplers */
uniform sampler2D texture0;
{% if uses_gradient == True -%}
uniform sampler2D gradient_texture;
uniform float vmin; // scales gradient
uniform float vmax; // scales gradient
{% endif -%}

void main (){  
  {% if uses_gradient == True %}

  vec4 sprite_value = texture2D(texture0, tex_coord0);
  vec4 tint = texture2D(gradient_texture, vec2(0.0,mde_color1d));  
  gl_FragColor = sprite_value * tint;
  
  {% else %}
  vec4 t = texture2D(texture0, tex_coord0);
  gl_FragColor = t*frag_color;  
  {% endif %}
}

/* Local Variables: */
/* compile-command: "cd .. && python main.py" */
/* python-main-file: "main.py" */
/* python-working-dir: "../" */
/* End: */

