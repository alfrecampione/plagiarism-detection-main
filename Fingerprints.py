import hashlib
import Levenshtein
import spacy

#Cargar el modelo de procesamiento de lenguaje que utilizara spacy.
nlp = spacy.load("en_core_web_sm")

#Tokenizar un texto usando spacy.
def tokenize(text):
    doc = nlp(text)
    return [token.text for token in doc if not token.is_stop and not token.is_punct]

#Elimina los caracteres especiales y los signos de puntuacion utilizando spacy
def remove_noise(tokenized_docs):
  return [[token for token in doc if token.is_alpha] for doc in tokenized_docs]

#Elimina las palabras que no aportan informacion relevante utilizando spacy
def remove_stopwords(tokenized_docs):
  stopwords = spacy.lang.en.stop_words.STOP_WORDS
  return [
      [token for token in doc if token.text not in stopwords] for doc in tokenized_docs
  ]

def Fingerprints(docA: list[str], docB: list[str]) -> list:

    #Creamos las listas donde se guardaran los textos tokenizados.
    tokenizeA = []
    tokenizeB = []

    #Tokenizamos cada parrafo del texto y lo guardamos en la lista.
    for paragraph in docA:
        tokenizeA.append(tokenize(paragraph))

    for paragraph in docB:
        tokenizeB.append(tokenize(paragraph))

    #Creamos una lista donde se guardaran los textos luego de que se le eliminen el ruido y las stopwords.
    clean_text_A = []
    clean_text_B = []

    #Eliminamos el ruido y las stopwords de ambos texto y los guardamos en sus respectivas listas.
    for paragraph in tokenizeA:
        clean_text_A.append(remove_stopwords(remove_noise(paragraph)))
    
    for paragraph in tokenizeB:
        clean_text_B.append(remove_stopwords(remove_noise(paragraph)))

    #Convierte un string a binario y utiliza hashlib para hashearlo con el formato MD5 y devuelve el hash en hexadecimal.
    def do_hash(text):
        return hashlib.md5(text.encode()).hexdigest()
    
    #Creamos las listas donde se guardaran los textos hasheados.
    hash_docA = []
    hash_docB = []

    #Hasheamos cada palabra del parrafo y unimos esos hash para crear el hash de cada parrafo.
    for paragraph in clean_text_A:
        hash_docA.append("".join([do_hash(word) for word in paragraph]))
        #hash_docA.append(do_hash(paragraph))

    for paragraph in clean_text_B:
        hash_docB.append("".join([do_hash(word) for word in paragraph]))
        #hash_docB.append(do_hash(paragraph))

    #Creamos una lista donde para cada parrafo de A guardamos su radio de plagio con los parrafos de B.
    plagiarism_rate = []

    #Calculamos el radio de plagio usando distancia de Levenshtein entre los hash y los guardamos en la lista.
    for hashA in hash_docA:
        pr_i = []
        for hashB in hash_docB:
            pr_i.append(Levenshtein.ratio(hashA, hashB))
        plagiarism_rate.append(pr_i)
    
    #Creamos la lista donde se guardaran los resultados de la salida.
    out_list = []

    #Para cada parrafo de A guardamos el la salida el mayor radio de plagio que tuvo con un parrafo de B.
    for pr in plagiarism_rate:
        out_list.append(max(pr))

    #Devolvemos la lista de salida.
    return out_list
