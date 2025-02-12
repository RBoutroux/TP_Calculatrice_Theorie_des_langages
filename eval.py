import ply.lex as lex
import ply.yacc as yacc

# Liste des noms des tokens
tokens = ('NOMBRE', 'PLUS', 'MOINS','FOIS')

# Définition de l'expression rationnelle pour chaque token et de la valeur 
# associée (pour NOMBRE)
t_PLUS  = r'\+' # notez le \+ et pas + qui a une signification pour les expressions rationnelles
t_MOINS = r'-' 
t_FOIS  = r'\*'

def t_NOMBRE(t):
    r'[0-9]+' # on peut aussi écrire r'\d+'
    # initialement t.value est la chaîne de caractères correspondant à 
    # l'expression rationnelle
    t.value = int(t.value) 
    # grâce au typage faible de python c'est maintenant un entier
    # on pourrait aussi traiter l'exception ValueError pour détecter
    # un éventuel débordement de capacité.
    return t

# caractères à ignorer: ici espaces, tabulations, saut de lignes
t_ignore = " \t\n"

# caractères inattendus: tout ce qui n'est pas défini avant
def t_error(t):
    print("Caractère inattendu: ", t.value[0])
    t.lexer.skip(1) # on saute ce caractère et on passe au suivant

# instantiation de l'analyseur lexical
lexer = lex.lex()

# Maintenant la grammaire

# l'axiome: 
def p_expression(p):
    'expression : expr'
    # une expression à calculer 
    print(p[1]) # on affiche la valeur de expr

# une expr est composée (pour l'instant) d'une liste de valeurs
# à additionner (ou soustraire) donc séparées par des '+' ou des '-':
#    'expr: terme | expr PLUS terme | expr MOINS terme'
# On sépare la première alternative des deux autres pour simplifier 
# l'écriture des valeurs associées. On pourrait aussi utiliser len(p) 
# pour distinguer les cas 
def p_expr_terme(p):
    'expr : terme'
    p[0] = p[1] # on transfère juste la valeur dans ce cas
    
def p_expr_ops(p):
    '''expr : expr PLUS  expr2
            | expr MOINS expr2
            | expr2'''

    # valeurs associées: on utilise p[2] pour distinguer les deux règles
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

# une expression peut aussi être un produit de termes
def p_expr2(p):
    '''expr2 : expr2 FOIS terme
            | terme'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '*':
        p[0] = p[1] * p[3]

def p_terme(p):
    'terme : NOMBRE'
    # pour l'instant, un terme est forcément un nombre
    p[0] = p[1]

# gestion minimaliste des erreurs de syntaxe
def p_error(p):
    if p:
        print("Erreur de syntaxe: ", p.value)
    else:
        print("Fin de chaîne inattendue")


# instantiation de l'analyseur syntaxique
parser = yacc.yacc()

# boucle infinie qui lit des lignes au clavier:
while True:
    try:
        ligne = input('eval> ')
    except EOFError: 
        # on sort s'il n'y a plus rien à lire: End Of File (Ctrl-D sous unix)
        break
    # on appelle l'analyseur syntaxique (qui appelle tout seul l'analyseur lexical)
    parser.parse(ligne)

