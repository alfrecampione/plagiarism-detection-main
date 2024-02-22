import hashlib
import spacy
from bow import bow as vector_similarity
from math import sqrt


# Cargar el modelo de procesamiento de lenguaje que utilizara spacy.
nlp = spacy.load("en_core_web_sm")


# Tokenizar un texto usando spacy.
def tokenize(text):
    doc = nlp(text)
    return [token.text for token in doc if not token.is_stop and not token.is_punct]


def Fingerprints(textA: list[str], textB: list[str]) -> list:
    # Creamos las listas donde se guardaran los textos tokenizados.
    tokenizeA = []
    tokenizeB = []

    # Tokenizamos cada parrafo del texto y lo guardamos en la lista.
    for paragraph in textA:
        tokenizeA.append(tokenize(paragraph))

    for paragraph in textB:
        tokenizeB.append(tokenize(paragraph))

    # Convierte un string a binario y utiliza hashlib para hashearlo con el formato MD5 y devuelve el hash en hexadecimal.
    def do_hash(text):
        return hashlib.md5(text.encode()).hexdigest()
    
    # Creamos las listas donde se guardaran los textos hasheados.
    hash_docA = []
    hash_docB = []

    # Hasheamos cada palabra del parrafo y unimos esos hash para crear el hash de cada parrafo.
    for paragraph in tokenizeA:
        hash_docA.append(" ".join([do_hash(word) for word in paragraph]))
        #hash_docA.append(do_hash(paragraph))

    for paragraph in tokenizeB:
        hash_docB.append(" ".join([do_hash(word) for word in paragraph]))
        #hash_docB.append(do_hash(paragraph))

    textA = "\n".join(hash_docA)
    textB = "\n".join(hash_docB)

    # Devolvemos la lista de salida con la distancia vectorial entre los hash
    return vector_similarity(textA, textB, hash_docA, hash_docB)
