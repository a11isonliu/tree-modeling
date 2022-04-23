from math import pi

# Monopodial Tree

ALPHABET=['A','B','C','F','!','^','&','$','|','[',']']
PARAMETERS=['l','w']
# Monopodial Tree
#Constants
r1=0.9 # contraction ratio trunk
r2=0.6 # contraction ratio branches
a0=pi/4 # branching angle trunk
a2=pi/4 # branching angle lateral axes
d=137.5*pi/180 # divergence angle
wr=0.707 # width decrease rate


AXIOM='A(50,10)'
PRODUCTION=['A(l,w):True→!(w)F(l)[&(a0)B(l*r2,w*wr)]|(d)A(l*r1,w*wr)',
             'B(l,w):True→!(w)F(l)[^(-a2)$()C(l*r2,w*wr)]C(l*r1,w*wr)',
             'C(l,w):True→!(w)F(l)[^(a2)$()B(l*r2,w*wr)]B(l*r1,w*wr)'
]

AXIOMS=[AXIOM,AXIOM]
PRODUCTIONS=[PRODUCTION,PRODUCTION]