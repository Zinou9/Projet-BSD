# Projet-BSD - CryptoBox

Outil en Python pour chiffrer et déchiffrer des messages (César, substitution, transposition), sans bibliothèque de cryptographie.

Binôme : BOUDA Mohamed - MATAR Matar

## Chiffrer

```
python CryptoBox.py cesar chiffrer BONJOUR -k 3
python CryptoBox.py cesar brute ERQMRXU
python CryptoBox.py substitution chiffrer ATTAQUE -k QWERTYUIOPASDFGHJKLZXCVBNM
python CryptoBox.py transposition chiffrer RENDEZVOUSAMIDI -k PORTE
python CryptoBox.py test
```

## Déchiffrer

```
python CryptoBox.py cesar dechiffrer ERQMRXU -k 3
python CryptoBox.py substitution dechiffrer QZZQJXT -k QWERTYUIOPASDFGHJKLZXCVBNM
python CryptoBox.py transposition dechiffrer ESIEVMRZANOIDUD -k PORTE
```
