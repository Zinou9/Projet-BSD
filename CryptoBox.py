import argparse
import string

ALPHABET = string.ascii_uppercase


# ---------- Utilitaires ----------
def nettoyer(texte):
    """Met en majuscules, retire accents (cas courants), espaces et ponctuation."""
    accents = {"É": "E", "È": "E", "Ê": "E", "Ë": "E", "À": "A", "Â": "A",
               "Ä": "A", "Î": "I", "Ï": "I", "Ô": "O", "Ö": "O", "Ù": "U",
               "Û": "U", "Ü": "U", "Ç": "C", "Œ": "OE", "Æ": "AE"}
    texte = texte.upper()
    texte = "".join(accents.get(c, c) for c in texte)
    return "".join(c for c in texte if c in ALPHABET)


def verifier_cle_substitution(cle):
    cle = cle.upper()
    if len(cle) != 26 or set(cle) != set(ALPHABET):
        raise ValueError("La clé de substitution doit contenir les 26 lettres "
                         "de l'alphabet, chacune une seule fois.")
    return cle


def verifier_motcle(motcle):
    motcle = nettoyer(motcle)
    if not motcle:
        raise ValueError("Le mot-clé doit contenir au moins une lettre.")
    return motcle


# ---------- César ----------
def cesar_chiffrer(message, k):
    return "".join(ALPHABET[(ALPHABET.index(c) + k) % 26] for c in nettoyer(message))


def cesar_dechiffrer(message, k):
    return cesar_chiffrer(message, -k)


def cesar_force_brute(message):
    """Retourne la liste des 25 candidats [(k, texte), ...]."""
    return [(k, cesar_dechiffrer(message, k)) for k in range(1, 26)]


# ---------- Substitution ----------
def substitution_chiffrer(message, cle):
    cle = verifier_cle_substitution(cle)
    return "".join(cle[ALPHABET.index(c)] for c in nettoyer(message))


def substitution_dechiffrer(message, cle):
    cle = verifier_cle_substitution(cle)
    return "".join(ALPHABET[cle.index(c)] for c in nettoyer(message))


# ---------- Transposition par colonnes ----------
def _ordre_colonnes(motcle):
    """Indices des colonnes dans l'ordre alphabétique (à égalité : de gauche à droite)."""
    return sorted(range(len(motcle)), key=lambda i: (motcle[i], i))


def transposition_chiffrer(message, motcle):
    motcle = verifier_motcle(motcle)
    msg = nettoyer(message)
    n = len(motcle)
    if len(msg) % n:
        msg += "X" * (n - len(msg) % n)
    return "".join(msg[col::n] for col in _ordre_colonnes(motcle))


def transposition_dechiffrer(message, motcle):
    motcle = verifier_motcle(motcle)
    msg = nettoyer(message)
    n = len(motcle)
    if len(msg) % n:
        raise ValueError(f"Longueur du message ({len(msg)}) non multiple de "
                         f"la taille du mot-clé ({n}).")
    lignes = len(msg) // n
    colonnes = {}
    for rang, col in enumerate(_ordre_colonnes(motcle)):
        colonnes[col] = msg[rang * lignes:(rang + 1) * lignes]
    return "".join(colonnes[c][r] for r in range(lignes) for c in range(n))


# ---------- Tests ----------
def tests():
    assert cesar_chiffrer("BONJOUR", 3) == "ERQMRXU"
    assert cesar_dechiffrer("ERQMRXU", 3) == "BONJOUR"
    assert (3, "BONJOUR") in cesar_force_brute("ERQMRXU")
    cle = "QWERTYUIOPASDFGHJKLZXCVBNM"
    assert substitution_chiffrer("ATTAQUE", cle) == "QZZQJXT"
    assert substitution_dechiffrer("QZZQJXT", cle) == "ATTAQUE"
    assert transposition_chiffrer("RENDEZVOUSAMIDI", "PORTE") == "ESIEVMRZANOIDUD"
    assert transposition_dechiffrer("ESIEVMRZANOIDUD", "PORTE") == "RENDEZVOUSAMIDI"
    # Mot-clé à lettres répétées + remplissage par X
    m = transposition_chiffrer("BONJOUR", "ABBA")
    assert transposition_dechiffrer(m, "ABBA") == "BONJOURX"
    print("Tous les tests sont OK.")


# ---------- Interface terminal ----------
def main():
    p = argparse.ArgumentParser(description="CryptoBox - brique 1")
    sub = p.add_subparsers(dest="algo")

    c = sub.add_parser("cesar", help="chiffrement de César")
    c.add_argument("action", choices=["chiffrer", "dechiffrer", "brute"])
    c.add_argument("message")
    c.add_argument("-k", "--cle", type=int, help="décalage (0-25)")

    s = sub.add_parser("substitution", help="substitution monoalphabétique")
    s.add_argument("action", choices=["chiffrer", "dechiffrer"])
    s.add_argument("message")
    s.add_argument("-k", "--cle", required=True, help="alphabet de 26 lettres")

    t = sub.add_parser("transposition", help="transposition par colonnes")
    t.add_argument("action", choices=["chiffrer", "dechiffrer"])
    t.add_argument("message")
    t.add_argument("-k", "--cle", required=True, help="mot-clé")

    sub.add_parser("test", help="lance les tests")
    a = p.parse_args()

    try:
        if a.algo == "cesar":
            if a.action == "brute":
                for k, txt in cesar_force_brute(a.message):
                    print(f"k={k:2d} : {txt}")
            else:
                if a.cle is None:
                    p.error("-k est requis pour chiffrer/dechiffrer")
                f = cesar_chiffrer if a.action == "chiffrer" else cesar_dechiffrer
                print(f(a.message, a.cle))
        elif a.algo == "substitution":
            f = substitution_chiffrer if a.action == "chiffrer" else substitution_dechiffrer
            print(f(a.message, a.cle))
        elif a.algo == "transposition":
            f = transposition_chiffrer if a.action == "chiffrer" else transposition_dechiffrer
            print(f(a.message, a.cle))
        elif a.algo == "test":
            tests()
        else:
            p.print_help()
    except ValueError as e:
        p.exit(1, f"Erreur : {e}\n")


if __name__ == "__main__":
    main()
