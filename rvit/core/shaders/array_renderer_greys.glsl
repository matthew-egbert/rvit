---VERTEX SHADER---
#version 150
// #version 300 es


#ifdef GL_ES
    precision highp float;
#endif
 
/* Outputs to the fragment shader */
out vec4 frag_color;
out vec2 tex_coord0;

/* vertex attributes */
in vec2     v_pos;
in vec2     v_tc0;

/* uniform variables */
uniform mat4       modelview_mat;
uniform mat4       projection_mat;
uniform vec4       color;
uniform float      opacity;

void main() {
  frag_color = color * vec4(0.0, 1.0, 1.0, opacity);
  tex_coord0 = v_tc0;
  gl_Position = projection_mat * modelview_mat * vec4(v_pos.xy, 0.0, 1.0);
}

---FRAGMENT SHADER--- 
#version 150
// #version 300 es

#ifdef GL_ES
    precision highp float;
#endif

in vec4 frag_color;
in vec2 tex_coord0;

/* uniform texture samplers */
uniform sampler2D texture0;
out vec4 Out_Color;

void main (){
  vec4 t = texture2D(texture0, tex_coord0);
  //vec4 t = texture(texture0, tex_coord0);
  Out_Color = t;//vec4(-t.r,t.r,0.0,1.0);
}

/* Local Variables: */
/* compile-command: "cd .. && python main.py" */
/* python-main-file: "main.py" */
/* python-working-dir: "../" */
/* End: */

