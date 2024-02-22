from bow import bow
from Fingerprints import Fingerprints
from CbPD import detect_plagiarism


CBPD_THRESHOLD = 0.5
COMBINED_THRESHOLD = 1.2

FINGERPRINT_WEIGHT = 1
BOW_WEIGHT = 1
CBPD_WEIGHT = 0.5


def plagiarism_rate(text1: str, text2: str):
    # Cleans texts, removing special characters and numbers
    clean_text1 = cleanup_text(text1)
    clean_text2 = cleanup_text(text2)

    # Splits texts in paragraphs, removing empty elements properly
    pgphs1 = get_paragraphs(clean_text1)
    pgphs2 = get_paragraphs(clean_text2)
    
    # Use different methods to calculate plagiarism rates
    bow_rate = bow(clean_text1, clean_text2, pgphs1, pgphs2)
    fgrprint_rate = Fingerprints(pgphs1, pgphs2)
    cbpd_rate = detect_plagiarism(text1, text2)

    # We calculate the combined rate of all the methods, so that independently they can't
    # ensure plagiarism, but combined they can, if no paragraph goes over the threshold rate
    # then we check for Citation-Based plagiarism with a different threshold

    combined_rate = []

    found_over_threshold = False

    # The threshold is reduced if no citations are found
    threshold = COMBINED_THRESHOLD if cbpd_rate > 0.01 else (COMBINED_THRESHOLD - CBPD_THRESHOLD)

    for i in range(len(bow_rate)):
        rate = bow_rate[i] * BOW_WEIGHT + fgrprint_rate[i] * FINGERPRINT_WEIGHT + cbpd_rate * CBPD_WEIGHT

        if rate > threshold:
            found_over_threshold = True
    
        combined_rate.append(rate)

    if not found_over_threshold:
        if cbpd_rate > CBPD_THRESHOLD:
            print(f"Se encontró plagio basado en citas en el documento con valor: {cbpd_rate}")
        else:
            print(f"No se encontró plagio.\nBoW: {bow_rate}\nFingerprint: {fgrprint_rate}\nCitation-based: {cbpd_rate}")
    else:
        for i in range(len(combined_rate)):
            if combined_rate[i] > threshold:
                print(f"Se encontró plagio en el párrafo {i + 1} con valor: {combined_rate[i]}")


# removes all special characters and numbers from text
def cleanup_text(text: str) -> str:
    clean_text = ''
    
    for c in text:
        if c.isalpha() or c.isspace():
            clean_text += c.casefold()
            
    return clean_text


# splits a text by line endings, returning a list of paragraphs
def get_paragraphs(text: str) -> list[str]:
    raw_pgphs = text.splitlines()
    
    pgphs = []
    
    for p in raw_pgphs:
        if p != '' and not p.isspace():
            pgphs.append(p)
            
    return pgphs


with open("text1.txt") as f:
    txt1 = f.read()

with open("text2.txt") as f:
    txt2 = f.read()
    
with open("text3.txt") as f:
    txt3 = f.read()
    
with open("text4.txt") as f:
    txt4 = f.read()

plagiarism_rate(txt1, txt2)