import pandas as pd

train_df = pd.read_csv("./tweets_train.csv", sep=",", header=None, skipinitialspace=True, quotechar='"').values.tolist()
dev_df = pd.read_csv("./tweets_dev.csv", sep=",", header=None, skipinitialspace=True, quotechar='"').values.tolist()
test_df = pd.read_csv("./tweets_test.csv", sep=",", header=None, skipinitialspace=True, quotechar='"').values.tolist()


def separation(train_df):
    """
    sépare les données d'entrainement en deux listes: les tweets positifs 
    d'une part, les tweets négatifs de l'autre.

    Parameters
    ----------
    train_df : list
        les données d'entrainement.

    Returns
    -------
    pos : list
        la liste des tweets positifs.
    neg : list
        la liste des tweets négtifs.

    """
    pos=[]
    neg=[]
    for i in range(len(train_df)):
        if train_df[i][0] == "positive":
            pos.append(train_df[i][1])
        else:
            neg.append(train_df[i][1])
    return pos,neg


def lecture(dev_df, test_df):
    """
    sépare les tweets de leur label pour les données de développement et de
    test.

    Parameters
    ----------
    dev_df : list
        les données de développement.
    test_df : list
        les données de test.

    Returns
    -------
    tweets_dev : list
        la liste des tweets des données d'entrainement.
    label_dev : list
        la lste des labels des données d'entrainement.
    tweets_test : list
        la liste des tweets des données de test.
    label_test : list
        la lste des labels des données de test.

    """
    tweets_dev = []
    tweets_test = []
    label_dev = []
    label_test = []
    for i in range(len(dev_df)):
        tweets_dev.append(dev_df[i][1])
        label_dev.append(dev_df[i][0])
    for i in range(len(test_df)):
        tweets_test.append(test_df[i][1])
        label_test.append(test_df[i][0])
    return tweets_dev,label_dev,tweets_test,label_test






def is_emoji(texte, i):
    """
    vérifie si la zone du texte considéré est un smiley.
    on considére comme smiley un ensemble de 2 ou 3 caractères compris parmi
    :;)(-=<3DPX/ séparé du reste du texte par des espaces (ou en fin de texte).

    Parameters
    ----------
    texte : str
        le texte à étudier.
    i : int
        indice à partir duquel vérifier.

    Returns
    -------
    bool

    """
    if texte[i] == " ":
        nb_carac = 1
        while i + nb_carac < len(texte) and nb_carac <= 3  and texte[i + nb_carac] in ":;)(-=<3DPX/":
            nb_carac += 1
        return nb_carac > 1 and nb_carac < 4 and (i + nb_carac == len(texte) or texte[i + nb_carac] == " ")
    else:
        return False
    

def nettoyage(texte):
    """
    renvoie la liste des mots du texte en minuscule sans ponctuation.
    Les smileys sont conservés.

    Parameters
    ----------
    texte : str
        le texte à étudier.

    Returns
    -------
    list
        la liste des mots du texte.

    """
    i = 0
    texte_propre = ''
    
    #On parcours chaque caractère du texte
    while i < len(texte):
        
        # si c'est une lettre on la met en minuscule
        if texte[i].isalpha():
            texte_propre += texte[i].lower()
            i += 1
                
        # sinon si le prochain mot est un smiley, on le conserve
        elif is_emoji(texte, i):
            texte_propre += texte[i]
            i+=1
            while i < len(texte) and texte[i] != " ":
                texte_propre += texte[i]
                i+= 1
        
        # sinon on remplace le caractère par un espace
        else:
            texte_propre += ' '
            i+=1
    
    # on transforme la chaîne de caractère en liste
    return texte_propre.split()
  

def creation_liste_de_mots(l_tweets):
    """
    renvoie une liste de tous les mots compris dans les une liste de textes
    après l'application de la fonction nettoyage.

    Parameters
    ----------
    l_tweets : list
        une liste de texte.

    Returns
    -------
    corpus : list
        la liste de tous les mots de l_tweets.

    """
    corpus = []
    for i in range(len(l_tweets)):
        # pour chaque tweet on récupère la liste des mots néttoyée
        corpus += nettoyage(l_tweets[i])
        
    return corpus


def mots_plus_occurents(l_mots):
    """
    Crée la liste des 50 mots les plus occurrents d'une liste.

    Parameters
    ----------
    l_mots : list
        une liste contenant des mots.

    Returns
    -------
    l_mots_trop_occurrents : list
        la liste des mots trop occurrents.

    """
    # création du dictionnaire et ajout des mots avec leurs occurences
    dico = {}
    
    for i in range(0,len(l_mots)):
        if(l_mots[i] not in dico):
            dico[l_mots[i]] = 1
        else:
            dico[l_mots[i]] = dico[l_mots[i]] + 1
            
    # trie des mots trop et pas assez occurents
    dico_trie = sorted(dico.items(),key=lambda t: t[1],reverse=True)
    l_mots_trop_occurrents = [ t[0] for t in dico_trie[0:50] ]
    
    return l_mots_trop_occurrents


def supprime_stock_words(l_mots_pos, l_mots_neg):
    """
    supprime les mots les plus occurrents à la fois dans la liste des mots 
    positifs et négatifs.

    Parameters
    ----------
    l_mots_pos : list
            la liste des mots positifs.
    l_mots_neg : list
        la liste des mots négatifs.

    Returns
    -------
    l_mots_pos_propre : list
        la liste des mots positifs après suppression des stock words.
    l_mots_neg_propre : list
        la liste des mots négative après suppression des stock words.

    """
    # recherche des mots les plus occurrents dans chacun des corpus
    trop_occu1 = mots_plus_occurents(l_mots_pos)
    trop_occu2 = mots_plus_occurents(l_mots_neg)
    
    # On regarde unniquement les mots qui sont très occurents dans les 2 corpus
    # Donc ces mots ne sont pas spécifiques à l'un des corpus.
    trop_occu = []
    for mot in trop_occu1:
        if mot in trop_occu2:
            trop_occu.append(mot)
    
    # On retire ces mots des 2 corpus
    l_mots_pos_propre = []
    l_mots_neg_propre = []
    for mot in l_mots_pos:
        if mot not in trop_occu:
            l_mots_pos_propre.append(mot)
            
    for mot in l_mots_neg:
        if mot not in trop_occu:
            l_mots_neg_propre.append(mot)
            
    return l_mots_pos_propre, l_mots_neg_propre

#PREPARATION
    
#sépâration des tweets positifs et négatifs
pos,neg = separation(train_df)

#séparation des tweets et des labels pour le dev set et le test set.
tweets_dev, label_dev, tweets_test, label_test = lecture(dev_df, test_df)

# On crée deux listes: une pour tous les mots des tweets positifs et une 
# pour tous les mots des tweets négatifs
mots_pos_tot = creation_liste_de_mots(pos)
mots_neg_tot = creation_liste_de_mots(neg)

# on enlève les mots très occurents dans les deux listes (stock words)
mots_pos_tot, mots_neg_tot = supprime_stock_words(mots_pos_tot, mots_neg_tot)


def mots_diff(l_mots,l_propre = []):
    """
    fais une liste de mots sans doublons.
    ajoute les mots d'une liste à une autre s'il n'y sont pas déjà.

    Parameters
    ----------
    l_mots : list
        une liste de mots.
    l_propre : list, optional
        la liste dans laquelle ajouter les mots. The default is [].

    Returns
    -------
    l_propre : list
        la liste après l'ajout des mots de l_mots.

    """
    for i in l_mots:
        if i not in l_propre:
            l_propre.append(i)
    return l_propre

#APPRENTISSAGE

#probabilité qu'un test quelconque soit positif (ou négatif)
p_pos = len(pos) / len(train_df)
p_neg = len(neg) / len(train_df)

# le nombre total de mots dans le corpus
n_corp = len(mots_pos_tot) + len(mots_neg_tot)

# on crée une liste de tout les mots différents du corpus
mots_corp = mots_diff(mots_pos_tot)
mots_corp = mots_diff(mots_neg_tot, l_propre=mots_corp)
"""
# On crée une liste du nombre d'occurence de chaque mots de mots_corp dans le corpus
occur_corp = []
for i in range(len(mots_corp)):
    occur_corp.append(mots_pos_tot.count(mots_corp[i]) + mots_neg_tot.count(mots_corp[i]))
    
    
# On recommence les 3 étapes précédentes pour le corpus positif et pour le corpus négatif    
n_pos = len(mots_pos_tot)
n_neg = len(mots_neg_tot)

mots_pos = mots_diff(mots_pos_tot)
mots_neg = mots_diff(mots_neg_tot)

occur_pos = []
for i in range(len(mots_pos)):
    occur_pos.append(mots_pos_tot.count(mots_pos[i]))
    
occur_neg = []
for i in range(len(mots_neg)):
    occur_neg.append(mots_neg_tot.count(mots_neg[i]))
"""

def extraction_mots_tweet(tweet, l_mots):
    """
    Permet de passer des mots du tweet brut aux mots traités et selectionnés pour une certaine catégorie
    (pos ou neg)

    Parameters
    ----------
    tweet : list
        liste des mots du tweet
    l_mots : list
        liste des mots d'une catégorie
        (pos ou neg)

    Returns
    -------
    mots_tweet_propre : liste
        liste des mots du tweet propre et selectionnés pour une certaine catégorie
        (pos ou neg)

    """
    
    # on récupère la liste des mots nettoyés du tweet.
    mots_tweet = nettoyage(tweet)
    
    #on enlève les mots du tweet non présent dans le corpus
    mots_tweet_propre = []
    for mot in mots_tweet:
        if mot in l_mots:
            mots_tweet_propre.append(mot)
    
    return mots_tweet_propre


def calcul_proba(l_mots, p_cat, occur_cat, n_cat, mots_cat, occur_corp, n_corp, mots_corp):
    """
    calcul la probabilité que les tweets de la liste donnée soit d'une certaine catégorie
    (pos ou neg)

    Parameters
    ----------
    l_mots : list
        liste des tweets
    p_cat : float
        probabilité que un tweet quelconque soit d'une certaine catégorie
        (pos ou neg) calculé avec le train_df
    occur_cat : list
        liste des occurences de chaque mots de la catégorie
        (pos ou neg)
    n_cat : int
        nombre d'éléments dans la liste de cette catégorie
        (pos ou neg)
    mots_cat : list
        liste des mots correspondant à cette catégorie
        (pos ou neg)
    occur_corp : list
        liste des occurences de chaque mots du corpus
    n_corp : int
        nombre d'éléments dans la liste du corpus
    mots_corp : list
        liste des mots du corpus

    Returns
    -------
    res : float
        la probabilité que le tweet soit de la catégorie désigné
        (pos ou neg)

    """
    
    # calcul de la probabilité d'obtenir ce texte connaissant sa catégorie
    p_T_cat = 1
    for mot in l_mots:
        i = mots_cat.index(mot)
        p_T_cat *= occur_cat[i]/n_cat
        
    # calcul de la probabilité d'obtenir ce texte
    p_T = 1
    for mot in l_mots:
        i = mots_corp.index(mot)
        p_T *= occur_corp[i]/n_corp
        
    # formule de Bayes
    res = (p_cat * p_T_cat)/ p_T
    
    return res
    
def compare(label, prediction):
    """
    compare le resultat de l'algorithme avec les labels

    Parameters
    ----------
    label : list
        liste des tweets avec typage
        (pos ou neg)
    prediction : list
        liste resultat de l'algorithme

    Returns
    -------
    res : float
        pourcentage de prédiction correctes de l'algorithme par rapport aux labels

    """
    # on compte le nombre de prédictions juste
    nb_bon = 0
    for i in range(len(label)):
        if label[i] == prediction[i]:
            nb_bon += 1
    
    return 100*nb_bon / len(label)





    

#def main():
    """
    Effectue tout le protocole de l'algorithme en créant les variables nécéssaires
    et en appelant les différentes fonctions précédentes

    Parameters
    ----------

    Returns : float
    -------   le pourcentage de prédiction correct
    
        
    """
    """
    #PREPARATION
    
    #sépâration des tweets positifs et négatifs
    pos,neg = separation(train_df)
    
    #séparation des tweets et des labels pour le dev set et le test set.
    tweets_dev, label_dev, tweets_test, label_test = lecture(dev_df, test_df)
    
    # On crée deux listes: une pour tous les mots des tweets positifs et une 
    # pour tous les mots des tweets négatifs
    mots_pos_tot = creation_liste_de_mots(pos)
    mots_neg_tot = creation_liste_de_mots(neg)
    
    # on enlève les mots très occurents dans les deux listes (stock words)
    mots_pos_tot, mots_neg_tot = supprime_stock_words(mots_pos_tot, mots_neg_tot)
    
    
    #APPRENTISSAGE
    
    #probabilité qu'un test quelconque soit positif (ou négatif)
    p_pos = len(pos) / len(train_df)
    p_neg = len(neg) / len(train_df)
    
    # le nombre total de mots dans le corpus
    n_corp = len(mots_pos_tot) + len(mots_neg_tot)
    
    # on crée une liste de tout les mots différents du corpus
    mots_corp = mots_diff(mots_pos_tot)
    mots_corp = mots_diff(mots_neg_tot, l_propre=mots_corp)
    
    # On crée une liste du nombre d'occurence de chaque mots de mots_corp dans le corpus
    occur_corp = []
    for i in range(len(mots_corp)):
        occur_corp.append(mots_pos_tot.count(mots_corp[i]) + mots_neg_tot.count(mots_corp[i]))
        
        
    # On recommence les 3 étapes précédentes pour le corpus positif et pour le corpus négatif    
    n_pos = len(mots_pos_tot)
    n_neg = len(mots_neg_tot)
    
    mots_pos = mots_diff(mots_pos_tot)
    mots_neg = mots_diff(mots_neg_tot)
    
    occur_pos = []
    for i in range(len(mots_pos)):
        occur_pos.append(mots_pos_tot.count(mots_pos[i]))
        
    occur_neg = []
    for i in range(len(mots_neg)):
        occur_neg.append(mots_neg_tot.count(mots_neg[i]))


    #CLASSIFICATION
    
    # Pour chaque tweet du test set, on souhaite prédire s'il est positif ou négatif
    prediction = []
    for tweet in tweets_test:
        
        #On extrait une liste des mots du tweet présent dans le corpus positif
        mots_tweet_pos = extraction_mots_tweet(tweet, mots_pos)
        #On calcule la probabilité que le tweet en question soit positif avec la formule de Bayes
        proba_pos_T = calcul_proba(mots_tweet_pos, p_pos, occur_pos, n_pos, mots_pos, occur_corp, n_corp, mots_corp)
        
        # De même pour trouver la probabilité qu'il soit négatif
        mots_tweet_neg = extraction_mots_tweet(tweet, mots_neg)
        proba_neg_T = calcul_proba(mots_tweet_neg, p_neg, occur_neg, n_neg, mots_neg, occur_corp, n_corp, mots_corp)
        
        # La prédiction correspond à la probabilité la plus élevée
        if proba_pos_T > proba_neg_T:
            prediction.append("positive")
        else:
            prediction.append("negative")
    
    # On compare nos predictions avec les vrais labels
    return compare(label_test, prediction)
    
    """
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    