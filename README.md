# Plagiarism Detection
## Autores
- Leonardo Amaro Rodriguez
- Alfredo Montero Lopez
- Anthuan Montes de Oca Pons

## Descripción
Este proyecto es un detector de plagio que utiliza varios métodos para calcular las tasas de plagio entre dos textos. Los métodos incluyen el uso de huellas digitales, bolsa de palabras (BoW) y detección de plagio basada en citas (CbPD).

## Tecnologías Utilizadas
- Python
- SpaCy
- hashlib

## Uso
El método principal es `plagiarism_rate(text1: str, text2: str)`, que toma dos textos como entrada y devuelve la tasa de plagio.
Para ejecutar el codigo: `make run text1=value1 text2=value2`

## Documentación de Código

### main.py
`plagiarism_rate(text1: str, text2: str)`: Este método calcula la tasa de plagio entre dos textos. Primero limpia los textos, eliminando caracteres especiales y números. Luego divide los textos en párrafos y utiliza diferentes métodos para calcular las tasas de plagio: bolsa de palabras (BoW), huellas digitales y detección de plagio basada en citas (CbPD). Finalmente, calcula la tasa combinada de todos los métodos. Si ningún párrafo supera la tasa de umbral, entonces verifica el plagio basado en citas con un umbral diferente.
