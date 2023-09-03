import httpx
import asyncio

# Lista de objetos a enviar por POST
objetos = [

{"id":"	Usuario212742	1	","fecha_ingreso":"	8/25/2023	","pais":"	Ecuador	","hora_ingreso":"	21:48:31	","ciudad":"	Quito	","ruta":"	/blog	","tiempo":"	0:00:17	","dispositivo":"	celular	"},
{"id":"	Usuario197525	2	","fecha_ingreso":"	8/17/2023	","pais":"	Chile	","hora_ingreso":"	22:07:25	","ciudad":"	Santiago	","ruta":"	/convocatoriaalaintelectualidad	","tiempo":"	0:00:42	","dispositivo":"	celular	"},


    # Agrega más objetos aquí si los tienes
]

# URL de la endpoint donde enviar los objetos
url = "https://backendusuariostime.onrender.com/estadisticas/"

# Función asincrónica para enviar objetos
async def enviar_objetos():
    async with httpx.AsyncClient() as client:
        for objeto in objetos:
            try:
                response = await client.post(url, json=objeto)
                response.raise_for_status()  # Verifica si hay errores en la solicitud
                print(f"Objeto enviado con éxito: {objeto}")
            except httpx.HTTPError as e:
                print(f"Error al enviar objeto: {e}")

# Ejecutar la función asincrónica
if __name__ == "__main__":
    asyncio.run(enviar_objetos())
