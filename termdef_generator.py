
import openai

from openai import OpenAI
client = OpenAI(api_key="sk-") // Introduce tu clave de la API

def cargar_textos(num_contextos: int):
    contextos = []
    for i in range(num_contextos):
        path = input(f"Introduce la ruta del contexto {i}: ")
        with open(path, "r") as f:
            contextos.append(f.read())
    return contextos

def extractor_de_info(termino: str, contextos: list):
    prompt = f"Extrae la información más relevante de cada contexto sobre 'qué es {termino}' de los siguientes contextos, si no te ofrece información sobre qué es o sus características, no prestes atención al contexto:\n"
    for i, contexto in enumerate(contextos):
        prompt += f"[contexto {i}] '{contexto}' [fin contexto {i}]\n"
        respuesta = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.5
        )

        resumen_info = str(respuesta.choices[0].text)
        return resumen_info

def generacion_definicion(termino: str, resumen_info: str):
    prompt = f"Utilizando solo la información necesaria de la que te voy a proporcionar, debes elaborar una definición propia del término '{termino}', siguiendo la siguiente fórmula: Término = hiperónimo + características distintivas. Por ejemplo, 'Las eyectivas son [hiperónimo] [características distintivas]'. La información comienza aquí: {resumen_info}\n"
    respuesta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5
    )

    definicion = str(respuesta.choices[0].text)
    return definicion

def guardar_definicion(termino: str, definicion: str):
    path = input("Introduce la ruta donde guardar la definición: ")
    with open(f"{path}/{termino}.txt", "w") as f:
        f.write(definicion)

def main():
    termino = input("Introduce el término a definir: ")
    num_contextos = int(input("Introduce el número de contextos: "))
    contextos = cargar_textos(num_contextos)
    resumen_info = extractor_de_info(termino, contextos)
    definicion = generacion_definicion(termino, resumen_info)
    guardar_definicion(termino, definicion)

if __name__ == "__main__":
    main()

        

