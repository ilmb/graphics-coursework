#version 330 core

in vec4 position_;
in vec3 normal_;
in vec4 color_;
in vec2 texcoord_;

struct Material {
    sampler2D diffuse;
    vec3 specular;
    float shininess;
};

struct Light {
    vec4 position;
    vec3 direction;
    float cutOff;
    float outerCutOff;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float constant;
    float linear;
    float quadratic;
};


uniform vec3 ViewPosition;
uniform vec3 LightIntensity;
uniform Material material;
uniform Light light;

out vec4 OutColor;



void main(){
    vec3 color;

    vec3 normal = normalize(normal_);
    vec3 lightDir;
    vec3 view;
    float intensity = 1.0;

    if(light.position.w == 0.0) {
        lightDir = normalize(light.position.xyz);
        view = normalize(-position_.xyz);
    }
    else {
        lightDir = normalize(light.position.xyz - position_.xyz);
        view = normalize(ViewPosition - position_.xyz);
    }

    vec3 reflect = reflect(-lightDir, normal);

    // затухание
    float distance = length(light.position.xyz - position_.xyz);
    float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));

    // окружающий свет
    color = light.ambient;

    // добавление размытия
    float dotNL = max(dot(normal, lightDir), 0.0);
    color += light.diffuse * dotNL * intensity;

    // добавление текстуры
    color *= texture2D(material.diffuse, texcoord_).rgb;

    // Добавление цвета
    color += color_.rgb;

    // Добавление бликов
    float dotNR = max(dot(view, reflect), 0.0);
    color += pow(dotNR, material.shininess) * light.specular * material.specular * intensity;

    color *= attenuation;

	OutColor = vec4(LightIntensity * color, 1.0f);
}