import string
import math

# Définir les mots vides

stopwords = ['le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'et', 'à','dans','en','pour','qui','ne','dune','son','que','sa','se','part','en','telle','ses','plus'
             ,'qu’il','se','au','aux','ou','on','2020','environ','nombre','rang','plus','par',"'l",'ses','p','ont','sont','ont','est','peut']

#Définir la plage de fréquence

min_freq = 2
max_freq = 10

# Ouvrir le fichier d'entrée
with open('doc.txt', 'r', encoding='utf-8') as f:
    # Read the file contents
    contents = f.read()

# Diviser le contenu en documents
documents = contents.split('######')

# Créer un dictionnaire pour stocker les fréquences de termes pour chaque document
term_freqs = {}

# Itérer sur les documents
for idx, doc in enumerate(documents):
    # initialiser le compteur de fréquence de termes pour le document courant
    term_freqs[idx] = {}
    
    #  Diviser le document en paragraphes
    paragraphs = doc.split('\n\n')
    
    # Itérer sur les paragraphes
    for para in paragraphs:
        # Diviser le paragraphe en phrases
        sentences = para.split('. ')
        
        #  Itérer sur les phrases
        for sent in sentences:
            # Supprimer la ponctuation et convertir en minuscules
            sent = sent.translate(str.maketrans('', '', string.punctuation))
            sent = sent.lower()
            
            # Diviser la phrase en mots
            words = sent.split()
            
            # Itérer sur les mots
            for word in words:
                # Vérifier si le mot est un mot vide
                if word in stopwords:
                    continue
                
                #  Incrémenter le compteur de fréquence de termes pour le document courant
                if word in term_freqs[idx]:
                    term_freqs[idx][word] += 1
                else:
                    term_freqs[idx][word] = 1

# Ouvrir le fichier de sortie pour les fréquences de termes
with open('frequency.txt', 'w', encoding='utf-8') as f:
    #  Itérer sur les document
    for idx, freqs in term_freqs.items():
        #  Écrire l'identifiant du document
        f.write(f'Document {idx}:\n')
        
        # Itérer sur les fréquences de termes pour le document courant
        for term, freq in freqs.items():
            # Vérifier si la fréquence de terme est dans la plage spécifiée
            if freq >= min_freq and freq <= max_freq:
                # Écrire le terme et sa fréquence dans le fichier de sortie
                f.write(f'{term}: {freq}\n')
        
        # Écrire un séparateur entre les documents
        f.write('--------------------------\n')

# Ouvrir le fichier de sortie pour les termes pondérés
def new_func(line):
    document_id, term, frequency = line.strip().split()
    return term,document_id,frequency

with open('resultat.txt', 'w', encoding='utf-8') as f:
    # Itérer sur les documents
    for idx, freqs in term_freqs.items():
        # Écrire l'identifiant du document
        f.write(f'Document {idx}:\n')
        
        #  Calculer le nombre total de termes dans le document courant
        total_terms = sum(freqs.values())
        
        # Itérer sur les fréquences de termes pour le document courant
        for term, freq in freqs.items():
            # Vérifier si la fréquence de terme est dans la plage spécifiée
            if freq >= min_freq and freq <= max_freq:
                # Calculer le poids du terme en cours
                #weight = (1 + math.log10(freq)) * math.log10(len(documents) / total_terms)
                weight = (1 + math.log10(freq)) * math.log10(total_terms/len(documents))

                
                # Écrire le terme et son poids dans le fichier de sortie
                f.write(f'{term}: {weight:.2f}\n')
        
        # Écrire un séparateur entre les documents
        f.write('--------------------------\n') 




# Ouverture des fichiers contenant le corpus, les fréquences et les résultats
with open('doc.txt', 'r') as corpus_file, \
     open('frequency.txt', 'r') as frequency_file, \
     open('resultat.txt', 'r') as resultat_file, \
     open('score.txt', 'w') as score_file:
  
    # Lecture des fréquences des mots clés et stockage dans un dictionnaire
    frequencies = {}
    for line in frequency_file:
        parts = line.strip().split(':')
        if len(parts) == 2:
            term = parts[0].strip()
            frequency_str = parts[1].strip()
            if frequency_str.replace('.', '', 1).isdigit():
                frequency = float(frequency_str)
                frequencies[term] = frequency
  
    # Lecture de la requête de l'utilisateur
    query = input("Entrez votre requête : ")
  
    # Initialisation de la liste de documents pertinents
    relevant_documents = []
      
    # Boucle pour chaque ligne du corpus
    for document in corpus_file:
      
        # Initialisation du score à 0
        score = 0
      
        # Boucle pour chaque terme de la requête
        for term in query.strip().split():
          
            # Vérification si le terme est présent dans le document
            if term in document:
              
                # Ajout du poids du terme au score
                score += frequencies.get(term, 0)
              
        # Ajout du document à la liste des documents pertinents s'il est pertinent
        if score >= 0:
            relevant_documents.append((document.strip(), score))
  
    # Tri des documents pertinents par ordre décroissant de score
    relevant_documents.sort(key=lambda x: x[1], reverse=True)

    # Affichage des documents pertinents et leur score
    if len(relevant_documents) > 0:
        print("Documents pertinents :")
        for document, score in relevant_documents:
            print(f"{document} : {score}")
            score_file.write(f"{document} : {score}\n")
    else:
        print("Aucun document pertinent trouvé.")


