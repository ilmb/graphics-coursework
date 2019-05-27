#version 330 core


in vec3 position_vertex;
in vec3 normal_vertex;
in vec2 texcoord_vertex;
in vec4 color_vertex;

out vec4 position_;
out vec3 normal_;
out vec4 color_;
out vec2 texcoord_;

uniform mat3 NormalMatrix;
uniform mat4 MVP;
uniform mat4 ModelMatrix;


void main(){
	
	position_ = ModelMatrix * vec4(position_vertex, 1.0);
	normal_ = NormalMatrix * normal_vertex;
	color_ = color_vertex;
	texcoord_ = texcoord_vertex;

    gl_Position = MVP * vec4(position_vertex, 1.0);
}
