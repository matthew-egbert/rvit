---VERTEX SHADER---
#version 120

#ifdef GL_ES
    precision highp float;
#endif
 
/* Outputs to the fragment shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* vertex attributes */
// attribute vec2 v_tc0;
attribute float ll_ul_ur_lr;
{{ attributes | join('\n') }}

/* uniform variables */
uniform mat4       modelview_mat;
uniform mat4       projection_mat;
uniform vec4       color;

{{ vertex_shader_functions | join('\n') }}

mat2 rotate2d(float _angle){
    return mat2(cos(_angle),-sin(_angle),
                sin(_angle),cos(_angle));
}


void main() {
  {% if 'attribute float color1D;' in attributes %}
  vec3 rgb = hsv2rgb(vec3(color1D,1.0,1.0));
  frag_color = vec4(rgb,color.w) ;
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

  frag_color = color * vec4(0.0, 1.0, 1.0, 0.5);
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

/* uniform texture samplers */
uniform sampler2D texture0;

void main (){
  vec4 t = texture2D(texture0, tex_coord0);
  gl_FragColor = t;//vec4(t.r,t.g,t.b,1.0);
  //gl_FragColor = vec4(0.0,1.0,0.0,1.0);//vec4(tex_coord0.x,tex_coord0.x,tex_coord0.y,1.0);
}

/* Local Variables: */
/* compile-command: "cd .. && python main.py" */
/* python-main-file: "main.py" */
/* python-working-dir: "../" */
/* End: */

