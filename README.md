# Projet-BSD - CryptoBox
 
Outil en Python (terminal) pour chiffrer et déchiffrer des messages, sans bibliothèque de cryptographie.
 
Binôme : MATAR Matar - BOUDA Mohamed
 
## Contenu
 
| Séance | Algorithmes |
|---|---|
| TP 1 | César (avec force brute), substitution, transposition par colonnes |
| TP 2 | Vigenère (chiffrer, déchiffrer) et casseur de Vigenère |
 
## Lancer l'outil
 
Il faut Python 3.10 ou plus. Rien à installer.
 
```
py -3.10 CryptoBox.py test
```
 
Doit afficher `Tous les tests sont OK.` (sous Linux/Mac : `python3`).
 
## Commandes
 
### César, substitution, transposition (TP 1)
 
```
py -3.10 CryptoBox.py cesar chiffrer BONJOUR -k 3
py -3.10 CryptoBox.py cesar brute ERQMRXU
py -3.10 CryptoBox.py substitution chiffrer ATTAQUE -k QWERTYUIOPASDFGHJKLZXCVBNM
py -3.10 CryptoBox.py transposition chiffrer RENDEZVOUSAMIDI -k PORTE
```
 
Pour déchiffrer, remplacer `chiffrer` par `dechiffrer`.
 
### Vigenère (TP 2)
 
```
py -3.10 CryptoBox.py vigenere chiffrer "ATTAQUE A L'AUBE" -k CLE
py -3.10 CryptoBox.py vigenere dechiffrer "CEXCBYG L P'CFFG" -k CLE
py -3.10 CryptoBox.py vigenere casser -L 9 -f texte.txt
py -3.10 CryptoBox.py vigenere brute -f texte.txt
```
 
- `casser` : retrouve la clé à partir de la longueur `-L`, puis affiche le début du texte déchiffré.
- `brute` : essaie les longueurs de clé 2 à 10. La bonne est la plus petite qui donne un texte lisible.
- `-f fichier.txt` : lit le texte chiffré dans un fichier.
## Comment ça marche
 
### Vigenère
 
Chaque lettre du message est décalée comme dans César, mais le décalage change selon la lettre de la clé (A = 0, B = 1, ..., Z = 25). La clé est répétée.
 
- Le texte est mis en majuscules et les accents sont retirés.
- Espaces, chiffres et ponctuation sont recopiés tels quels.
- La clé n'avance que sur les lettres : sur un espace ou une virgule, on ne consomme pas de lettre de clé.
- Chiffrer : `C = (M + décalage) mod 26`. Déchiffrer : `M = (C - décalage) mod 26`.
Fonctions : `vigenere_chiffrer`, `vigenere_dechiffrer` (elles utilisent `vigenere(texte, cle, sens)` avec `sens = 1` ou `-1`).
 
### Casseur de Vigenère
 
La clé a une longueur L connue. Les lettres 1, 1+L, 1+2L... ont toutes été décalées par la même lettre de clé, donc chaque colonne est un simple César.
 
1. On garde seulement les lettres du texte chiffré.
2. On découpe en L colonnes (`lettres[j::L]`).
3. Dans chaque colonne, on cherche la lettre la plus fréquente : en français, c'est un E chiffré.
4. Décalage = (lettre trouvée - E) mod 26. La lettre de clé est la lettre de ce rang.
5. On assemble les L lettres : c'est la clé. On vérifie en déchiffrant.
Fonction : `vigenere_casser(texte, L)`. Le casseur marche sur tout texte français assez long (le calcul des fréquences est fiable seulement s'il y a assez de lettres par colonne).
 
Mode `brute` : si L est inconnue, on appelle le casseur pour L = 2 à 10 et on lit les débuts de texte.
 
### Structure du code
 
- Utilitaires : `nettoyer`, `normaliser`, vérifications de clés.
- Un groupe de fonctions par algorithme.
- `tests()` : vérifie tous les exemples des énoncés.
- `main()` : interface en ligne de commande (`argparse`).

## Limites
 
- Le casseur suppose un texte en français assez long.
- Après déchiffrement d'une transposition, les `X` de remplissage restent à la fin.
 
