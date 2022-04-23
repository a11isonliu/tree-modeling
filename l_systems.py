from random import *
from numpy import *
import turtle
from math import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d  # for 3D


from monopodial_tree import *
# from sympodial_tree import *
# from ternary_tree import *


#Split
def split_production(production):
    '''split production
    parameter : a production (string)
    return : list with three strings
    - predecessor
    - condition
    - successor '''
    predecessor=production.split(':')[0]
    condition=production.split(':')[1].split('→')[0]
    successor=production.split(':')[1].split('→')[1]
    
    return [predecessor, condition,successor]


#convert word to modules
def word_to_modules(word,alphabet):
    '''split a parametric word to 
    a list of string modules according 
    the content of alphabet'''
    modules=[]
    module=''
    for character in word:
        if character in alphabet :
            modules.append(module)
            module=character
        else :
            if character not in ['[',']','{','}','°']:
                module=module + character
    modules.append(module) #append last module
    modules=modules[1:]
    
    return modules
        

#number of parameters in a module
def n_parameters(module):
    '''return the number of parameters
    in a module(actual or formal)
    parameter: module (string)
    return : integer'''
    n=0
    for car in module:
        if car==',':
            n=n+1
    if '()' in module:
        return 0
    else:
        return n+1
    

#parameters in a module
def parameters(module):
    '''list of modules's parameters'''
    param=''
    if module not in ['[',']','{','}','°']:
        param=module.split('(')[1].split(')')[0].split(',')
    return param


#matching modules
def match(actual,production):
    '''Return True if modules match, else False
    Parameters : actual module, production (strings)
    return : boolean'''
    [predecessor,condition,successor]=split_production(production)
    if predecessor[0]==actual[0]  and n_parameters(predecessor)==n_parameters(actual) :
        for i in range(n_parameters(actual)):
            exec(parameters(predecessor)[i] + '=' + parameters(actual)[i])
        if eval(condition)==True:
            return True
    return False


#apply production to a matching module
def apply(module,production,alphabet):
    '''parameters : module( a matching module) , production (strings)
       return : result, a parametric word (string)'''
    [predecessor,condition,successor]=split_production(production)
    result=''
    for i in range(n_parameters(module)):
            exec(parameters(predecessor)[i] + '=' + parameters(module)[i])
    successor_modules = word_to_modules(successor,alphabet) #modules in the successor
    for module in successor_modules:
        if module in ['[',']','{','}','°']:
            actual=module
        else:
            actual=module[0]+'('
            for parameter in parameters(module):
                if parameter !='':
                    actual=actual+str(eval(parameter))+','
            if actual[-1]==',':
                actual=actual[:-1] #delete last comma
            actual=actual + ')'
        result=result+ actual
    
    return result


#next word after productions
def next(word,productions,alphabet):
    '''apply production to a parametric word if conditions are met
    parameters : word (string), productions(list of strings)
    return : a parametric word(string)'''
    modules=word_to_modules(word,alphabet)
    result=''
    for module in modules :
        i=0
        for production in productions:
            if match(module,production):
                result=result+apply(module,production,alphabet)
                i=i+1
        if i==0 or module in ['[',']','{','}','°']:
                result=result+module
        
    return result



# parametric word after n steps
def parametric_word(axiome,productions,alphabet,n):
    '''write the parametric word after n steps of productions'
    parameters : axiome(string),productions(list of strings),
                 alphabet (list of strings)
                 n (integer)
    return : word, a paramtric word (string)
    '''
    word = axiome
    for i in range(n):
        word=next(word,productions,alphabet)
    return word



#rotations functions
def RU(a,hlu):
    '''rotate the turtle around U, by angle a
    parameters : a (angle in radians)
                 hlu (turtle orientation in a tuple of list)
    return : H,L,U, turtle orienation after rotation
    '''
    hlu=array([hlu[0],hlu[1],hlu[2]]).transpose()
    ru=array([(cos(a),sin(a),0),
              (-sin(a),cos(a),0),
              (0,0,1)]) #rotaton matrix around U
    hlu=dot(hlu,ru)
    H,L,U=hlu.transpose()[0],hlu.transpose()[1],hlu.transpose()[2]
    return list(H),list(L),list(U)

def RH(a,hlu):
    '''rotate the turtle around H, by angle a
    parameters : a (angle in radians)
                 hlu (turtle orientation in a tuple of list)
    return : H,L,U, turtle orienation after rotation
    '''
    hlu=array([hlu[0],hlu[1],hlu[2]]).transpose()
    rh=array([(1,0,0),
              (0,cos(a),-sin(a)),
              (0,sin(a),cos(a))]) #rotaton matrix around H
    hlu=dot(hlu,rh)
    H,L,U=hlu.transpose()[0],hlu.transpose()[1],hlu.transpose()[2]
    return list(H),list(L),list(U)

def RL(a,hlu):
    '''rotate the turtle around L, by angle a
    parameters : a (angle in radians)
                 hlu (turtle orientation in a tuple of list)
    return : H,L,U, turtle orientation after rotation
    '''
    hlu=array([hlu[0],hlu[1],hlu[2]]).transpose()
    rl=array([(cos(a),0,-sin(a)),
              (0,1,0),
              (sin(a),0,cos(a))]) #rotaton matrix around L
    hlu=dot(hlu,rl)
    H,L,U=hlu.transpose()[0],hlu.transpose()[1],hlu.transpose()[2]
    return list(H),list(L),list(U)


#translation (x,y,z) to (x',y',z')
def translate(xyz,l,h):
    '''translate a point m from l length with h vector
    parameters : xyz (tuple) coordinates before translation
                 l (float) lenght
                 h (list) translation heading vector
    return : x,y,z (tuple) coordinates after translation'''
    x=xyz[0] + l*h[0]
    y=xyz[1] + l*h[1]
    z=xyz[2] + l*h[2]

    return x,y,z



#keep turtle orientation
def L_horizontal(hlu):
    ''' keep L horizontal
    parameters : hlu (tuple of list) turtle orientation
    return H,L,U (tuple of list) : new turtle orientation'''
    H=hlu[0]
    [xh,yh,zh]=H
    V=[0,0,1]
    L=[-yh,-xh,0]
    U=[xh*zh,-zh*yh,-xh**2-yh**2]

    return H,L,U


#tropism
def normalize(vect):
    '''normalize a vector'''
    norm = linalg.norm(vect)
    if norm == 0: 
       return vect
    return vect / norm

def torque(hlu,t):
    ''' define torque h*t
    parameters : hlu (tuple of list) orientation
                 t (list) tropism vector
    return : torq (list) H*t
    '''
    H=hlu[0]
    [xh,yh,zh]=H
    [xt,yt,zt]=t
    torq=[yh*zt-zh*yt,zh*xt-xh*zt,xh*yt-yh*xt]

    return torq


def rotation(hlu,u,a):
    '''rotate the turtle vector around an axis by angle
    parameters : hlu (tuple of list) turtle orientation before rotation
                 u (list) axis vector
                 a(float) rotation angle in radians
    return  H,L,U (tuple of list) turtle orientation after rotation
    '''
    u=normalize(u)
    [ux,uy,uz]=u
    c=cos(a)
    s=sin(a)
    R=array([(ux**2*(1-c)+c,ux*uy*(1-c)-uz*s,ux*uz*(1-c)+uy*s),
            (ux*uy*(1-c)+uz*s,uy**2*(1-c)+c,uy*uz*(1-c)-ux*s),
            (ux*uz*(1-c)-uy*s,uy*uz*(1-c)+ux*s,uz**2*(1-c)+c)])
    
    [H,L,U]=hlu
    H=array(H)
    L=array(L)
    U=array(U)
    H=R.dot(H)
    L=R.dot(L)
    U=R.dot(U)
    return list(H),list(L),list(U)
    

def tropism(hlu,t):
    ''' define turtle orientation after tropism
    parameters : hlu (tuple of list) orientation without tropism
                 t (tuple) tropism vector
    return : H,L,U (tuple of list) orientation with tropism
    '''
    
    M=torque(hlu,t) # rotation axe
    alpha=linalg.norm(M) # rotation angle
    
    H,L,U = rotation(hlu,M,alpha)
    

    return H,L,U



#fra leaf
def draw_leaf(xyz,hlu,word,alphabet):
    '''draw a defined leaf at xyz coords
    parameters : xyz (tuple) turtle coordinates
                 word (string) parametric word
                 alphabet (list)
    '''
    modules=word_to_modules(word, alphabet)
    polygon=[] # sequence of coordinates for surface
    xyzf=xyz
    for module in modules:
        
        if module[0]=='G':
            turtle.up()
            h=hlu[0]
            xyzf=translate(xyz,eval(parameters(module)[0]),h)
            xf,yf,zf=xyzf
            turtle.goto(xf,zf)
    
        elif module[0]=='^':
            angle=eval(parameters(module)[0])
            hlu=RU(angle,hlu)

        elif module[0]=='{':
            turtle.begin_fill()
        
        elif module[0]=='}':
            #print(polygon)
            turtle.down()
            turtle.color('dark green')
            for v in polygon :
                turtle.goto(v[0],v[2])
            turtle.end_fill()
            polygon=[]
            
        elif module[0]=='°':
            polygon.append(xyzf)
    
    turtle.color('black')
    turtle.up()
    

#draw
def draw_turtle(words,alphabet):
    '''draw the 3d pattern according to alphabet
    parameters : patterns (string list), alphabet (list of strings)
    '''
    #environment
    sigma=pi/158#standard variation of rotation angle
    T=[0,0,-0.5] #tropism vector
    e=0.2 # susceptibility to bending
    T=list(e*array(T))
    
    #init coordinates of the turtle
    xyz=(0,0,-300) 
    x,y,z=xyz
    turtle.up()
    turtle.goto(x,z)
    
    #init orientation of the turtle
    teta=pi/6
    HLU=([0,0,1],[-sin(teta),-cos(teta),0],[-cos(teta),sin(teta),0])
    stack=[] # to memorize the turtle state
    polygon=[] #coordinates for surface
    modules_t=word_to_modules(words[0], alphabet) #tree modules
    
    for module in modules_t :
        turtle.down()
        if module[0]=='F':
            turtle.down()
            H=HLU[0]
            xyz=translate(xyz,eval(parameters(module)[0]),H)
            x,y,z=xyz
            turtle.goto(x,z)
            HLU=tropism(HLU,T)
            
        elif module[0]=='^':
            angle=eval(parameters(module)[0])
            HLU=RU(gauss(angle,sigma),HLU)
        
        elif module[0]=='&':
            angle=eval(parameters(module)[0])
            HLU=RL(gauss(angle,sigma),HLU)
        
        elif module[0]=='|':
            angle=eval(parameters(module)[0])
            HLU=RH(gauss(angle,sigma),HLU)

        elif module[0]=='[':
            stack.append((xyz,HLU))
        
        elif module[0]==']':
            turtle.up()
            xyz=stack[-1][0]
            x,y,z=xyz
            turtle.goto(x, z)
            HLU=stack[-1][1]
            stack=stack[:-1]
            turtle.down()
        
        elif module[0]=='!':
            turtle.width(eval(parameters(module)[0]))

        elif module[0]=='$':
            HLU=L_horizontal(HLU)
        
        if module[0]=='G':
            #turtle.up()
            turtle.down()
            turtle.color('green')
            H=HLU[0]
            xyz=translate(xyz,eval(parameters(module)[0]),H)
            x,y,z=xyz
            turtle.goto(x,z)
    
        elif module[0]=='{':
            turtle.begin_fill()
        
        elif module[0]=='}':
            turtle.down()
            turtle.color('dark green')
            for v in polygon :
                turtle.goto(v[0],v[2])
            turtle.end_fill()
            polygon=[]
            turtle.color('black')

        elif module[0]=='°':
            polygon.append(xyz)

    
        elif module[0]=='L':
            draw_leaf(xyz,HLU,words[1],alphabet)

def exporteps(name):
    ts=turtle.getscreen()
    ts.getcanvas().postscript(file =name, colormode = 'color')

def draw_matplotlib3d(words,alphabet):
    '''draw the 3d pattern according to alphabet
    parameters : patterns (string list), alphabet (list of strings)
    '''
    #environment
    sigma=pi/16#standard variation of rotation angle
    T=[0,0,-0.5] #tropism vector
    e=0.5 # susceptibility to bending
    T=list(e*array(T))
    
    #init coordinates
    xyz=(0,0,0) 
    x,y,z=xyz
    
    #init orientation
    teta=pi/6
    HLU=([0,0,1],[-sin(teta),-cos(teta),0],[-cos(teta),sin(teta),0])
    stack=[] # to memorize the turtle state
    # polygon=[] #coordinates for surface
    
    modules_t=word_to_modules(words[0], alphabet) #tree modules

    #init matplotlib
    X,Y,Z=[x],[y],[z] #matplotlib current tabs
    LINEWIDTH=1
    LINES=[] #Lines to draw
    
    
    for module in modules_t :
        if module[0]=='F':
            H=HLU[0]
            xyz=translate(xyz,eval(parameters(module)[0]),H)
            x,y,z=xyz
            X.append(x)
            Y.append(y)
            Z.append(z)
            HLU=tropism(HLU,T)
            
        elif module[0]=='^':
            angle=eval(parameters(module)[0])
            HLU=RU(gauss(angle,sigma),HLU)
        
        elif module[0]=='&':
            angle=eval(parameters(module)[0])
            HLU=RL(gauss(angle,sigma),HLU)
        
        elif module[0]=='|':
            angle=eval(parameters(module)[0])
            HLU=RH(gauss(angle,sigma),HLU)

        elif module[0]=='[':
            stack.append((xyz,HLU))
            LINES.append([(X,Y,Z),LINEWIDTH])
            x,y,z=xyz
            X,Y,Z=[x],[y],[z]
        
        elif module[0]==']':
            xyz=stack[-1][0]
            HLU=stack[-1][1]
            stack=stack[:-1]
            LINES.append([(X,Y,Z),LINEWIDTH])
            x,y,z=xyz
            X,Y,Z=[x],[y],[z]
        
        elif module[0]=='!':
            LINEWIDTH=eval(parameters(module)[0])

        elif module[0]=='$':
            HLU=L_horizontal(HLU)
        
        if module[0]=='G':
            H=HLU[0]
            xyz=translate(xyz,eval(parameters(module)[0]),H)
            x,y,z=xyz
            X.append(x)
            Y.append(y)
            Z.append(z)
    #plotting
    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca(projection='3d')  # 3D display
    for line in LINES:
        X,Y,Z=line[0]
        LINEWIDTH=line[1]
        ax.plot(X, Y, Z, 'k',linewidth=LINEWIDTH)  # Drawing 
    #plt.axis('off')
    plt.show()

def draw_turtlestatic(words,alphabet):
    '''draw the 3d pattern according to alphabet
    parameters : patterns (string list), alphabet (list of strings)
    '''
    #environment
    sigma=pi/36#standard variation of rotation angle
    T=[-0.02,0,-1] #tropism vector
    e=0.22 # susceptibility to bending
    T=list(e*array(T))
    
    #init coordinates of the turtle
    xyz=(0,0,-300) 
    x,y,z=xyz
    turtle.up()
    turtle.goto(x,z)
    
    #init orientation of the turtle
    teta=pi/7
    HLU=([0,0,1],[-sin(teta),-cos(teta),0],[-cos(teta),sin(teta),0])
    stack=[] # to memorize the turtle state
    polygon=[] #coordinates for surface
    modules_t=word_to_modules(words[0], alphabet) #tree modules
    
    for module in modules_t :
        turtle.down()
        if module[0]=='F':
            turtle.down()
            H=HLU[0]
            xyz=translate(xyz,eval(parameters(module)[0]),H)
            x,y,z=xyz
            turtle.goto(x,z)
            HLU=tropism(HLU,T)
            
        elif module[0]=='^':
            angle=eval(parameters(module)[0])
            HLU=RU(gauss(angle,sigma),HLU)
        
        elif module[0]=='&':
            angle=eval(parameters(module)[0])
            HLU=RL(gauss(angle,sigma),HLU)
        
        elif module[0]=='|':
            angle=eval(parameters(module)[0])
            HLU=RH(gauss(angle,sigma),HLU)

        elif module[0]=='[':
            stack.append((xyz,HLU))
        
        elif module[0]==']':
            turtle.up()
            xyz=stack[-1][0]
            x,y,z=xyz
            turtle.goto(x, z)
            HLU=stack[-1][1]
            stack=stack[:-1]
            turtle.down()
        
        elif module[0]=='!':
            turtle.width(eval(parameters(module)[0]))

        elif module[0]=='$':
            HLU=L_horizontal(HLU)
        
        if module[0]=='G':
            #turtle.up()
            turtle.down()
            turtle.color('green')
            H=HLU[0]
            xyz=translate(xyz,eval(parameters(module)[0]),H)
            x,y,z=xyz
            turtle.goto(x,z)
    
        elif module[0]=='{':
            turtle.begin_fill()
        
        elif module[0]=='}':
            turtle.down()
            turtle.color('dark green')
            for v in polygon :
                turtle.goto(v[0],v[2])
            turtle.end_fill()
            polygon=[]
            turtle.color('black')

        elif module[0]=='°':
            polygon.append(xyz)

    
        elif module[0]=='L':
            draw_leaf(xyz,HLU,words[1],alphabet)