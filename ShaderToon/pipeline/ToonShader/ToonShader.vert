#version 400

layout (location=0) in vec3 attr_position;
layout (location=1) in vec3 attr_normal;

out vec3 normal;
uniform mat4 MVP;

void main(void) 
{
    gl_Position = MVP*vec4(attr_position,1.0);
    normal = attr_normal;
}
