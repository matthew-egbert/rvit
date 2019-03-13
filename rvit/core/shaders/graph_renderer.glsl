---VERTEX SHADER---
#ifdef GL_ES
    precision highp float;
#endif
 
/* Outputs to the fragment shader */
varying vec4 frag_color;


/* vertex attributes */
attribute vec2     v_pos;

/* uniform variables */
uniform mat4       modelview_mat;
uniform mat4       projection_mat;
uniform vec4       color;
uniform float zero_scaled; // the y-values have been scaled to between 0 and 1. This is where 0 is.

void main() {
  //frag_color = vec4(1.0,abs(v_pos.y)<5.05,abs(v_pos.y)<5.05,1.0);
  frag_color = color;
  //frag_color.y = 0.0;
  gl_Position = projection_mat * modelview_mat * vec4(v_pos.xy, 0.0, 1.0);
}

---FRAGMENT SHADER--- 
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
  gl_FragColor = frag_color;
}

/* Local Variables: */
/* compile-command: "cd .. && python main.py" */
/* python-main-file: "main.py" */
/* python-working-dir: "../" */
/* End: */

