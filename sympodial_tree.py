# Sympodial Tree
from math import pi, sqrt
#L-SYSTEM DEFINITION
# Turtle orientation : H,U,L vectors (Heading, Up, Left)
# ^ : Left or Right around U
# & : pitch down or up around L
# | : roll left or right around H
# $ : force L to be horizontal (x,y,0)

ALPHABET=['A','B','C','F','!','^','&','$','|','[',']']
PARAMETERS=['l','w']

#Constants
r1=0.75
r2=0.7
a1=20*pi/180
a2=40*pi/180
wr=1/sqrt(3)

#Production
AXIOM='A(100,10)'
PRODUCTION=['A(l,w):True→!(w)F(l)[&(a1)B(l*r1,w*wr)]|(3*pi/4)[&(a2)B(l*r2,w*wr)]',
             'B(l,w):True→!(w)F(l)[^(a1)$()B(l*r1,w*wr)][^(-a2)$()B(l*r2,w*wr)]'
            ]

AXIOMS=[AXIOM,AXIOM]
PRODUCTIONS=[PRODUCTION,PRODUCTION]