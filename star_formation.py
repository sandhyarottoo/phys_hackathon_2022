# -*- coding: utf-8 -*-
'''
In gas, induce a rotation
To see, perchance, a star's formation
It's really quite simple,
If your coding is nimble,
You'll get a stellar simulation

- The Limerick Queens

'''





from vpython import *
import random as rand
import numpy as np

scene.width = 1600
scene.height = 900

star_colors = [color.red, color.green, color.blue,
              color.yellow, color.cyan, color.magenta]


G = 6.676e-11
M = 20
R = 50
L = rand.randint(300, 1200)

Nobs = 50


obs = []
ptot = vector(0,0,0)
# =============================================================================
# bigboy = sphere(pos=vector(0,0,0), radius = 20, make_trail = True, retain = 200)
# bigboy.mass = M*10
# bigboy.momentum = v * bigboy.mass
# obs.append(bigboy)
# =============================================================================

for i in range(Nobs):
    r = R+rand.randint(1, 1000) / 100
    ob = sphere(pos=L*vector.random(), radius = r, make_trail = True, retain = 100, color = star_colors[rand.randint(0,5)])
    ob.mass = 10*(M*(r/R)**3 *rand.randint(1,100)/10)
    ob.dtheta = 0
    ob.L = vector(0,0,0)
    ob.cm = ob.pos
    ob.momentum = 0.0000002*vector.random()
    ob.I = 5/2 * ob.mass * ob.radius ** 2
    obs.append(ob)
    ptot = ptot + ob.momentum
    
cm = vector(0,0,0)
massTot = 0
for ball in obs:
    massTot += ball.mass
    cm += ball.pos*ball.mass

cm = cm/massTot

cm_axis = cross(vector(0,1,0),cm)



for ball in obs:
    r = ball.pos-cm_axis
    v = cross(r,cm_axis)
    ball.momentum += 1*(v*ball.mass).hat


Cr = 0.99
dt = 300

def force():
    global obs
    i = 0
    while i < len(obs):
        obi = obs[i]
        F = vector(0,0,0)
        for n in range(len(obs)):
            obn = obs[n]
            if obi == obn:
                continue
            r = obn.pos - obi.pos
            if mag2(r) < (obi.radius + obn.radius)**2:
                    obn.v = obn.momentum/obn.mass
                    obi.v = obi.momentum/obi.mass
   
                    finalPos = (obn.pos*obn.mass + obi.pos*obi.mass)/(obi.mass + obn.mass)
    #                 #finalRadius = (obn.radius**3 + obi.radius**3)**(1/3)
    #                 #new_ob = sphere(pos=finalPos, radius=finalRadius, make_trail=True, retain=200)
    # =============================================================================
                    newmass = obn.mass + obi.mass - rand.randint(1,10)
                    newmoment = obn.momentum + obi.momentum
                    
                    torque = obn.momentum.cross(obn.pos - finalPos)
                    obi.L += torque
                    obn.L += torque
                    w = (obi.L + obn.L) / (obi.I + obn.I)
                    w_scalar = dot(w, norm(finalPos))
                    obi.dtheta = w_scalar
                    obn.dtheta = w_scalar
                    
                    obn.cm = finalPos
                    obi.cm = finalPos
                    
                    obn.momentum =  (Cr*obi.mass*(obi.v-obn.v) + obi.mass*obi.v + obn.mass*obn.v)/(obn.mass+obi.mass) * obn.mass
                    obi.momentum = (Cr*obn.mass*(obn.v-obi.v) + obi.mass*obi.v + obn.mass*obn.v)/(obn.mass+obi.mass) * obi.mass
                    
    # =============================================================================
#                 obs.append(new_ob)
#                 obs.remove(obn)
#                 obs.remove(obi)
# =============================================================================
                
                
            else:
                F += (G * obn.mass * obi.mass / mag2(r))*r
        obi.momentum += F * dt
        i += 1
        

tot = 0
while tot <= 1:
    rate(100)
    force()
    for o in obs:     
        o.pos += o.momentum * dt / o.mass
        o.rotate(angle=o.dtheta, axis=vector(0,1,0), origin=o.cm)
        
        
        
        
        
        
        
        
        
        
        
        
        