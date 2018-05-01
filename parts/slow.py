#!/usr/bin/env python 
__author__ = "Patrik Lundin" 
__copyright__ = "Copyright 2018, nothisispatrik.com" 
__license__ = "LGPL v3. Algorithms/constants may be (C) 2014-2018 The Monero project or (C) 2012-2014 The Cryptonote Developers. All code is original."
__email__ = "patrik@nothisispatrik.com"
__status__ = "Prototype"
__doc__ = """ """

from bl256 import bl256
from gr256 import gr256
from jh256 import jh256
from sk256 import sk256
from keccak import keccak
from memhrd import memhrd
from impasp import *

def slowhash(p):
        # padding
    inp = [0]*200
    inp[0:76] = p
    inp[76] = 1
    inp[135] = 0x80 
        # get the nonce, for passing to tweak later
    nonce = inp[35:35+8]


    tmp = keccak(inp)
    print "Kec: ",''.join("%.2x"%(a) for a in tmp)

    pad = asplode(tmp)
    print sum(pad)
    memhrd(pad, tmp, nonce)
    print sum(pad)
    implode(pad, tmp)
    print "Kec: ",''.join("%.2x"%(a) for a in tmp)
    kec = keccak(tmp)
    print "Kec: ",''.join("%.2x"%(a) for a in tmp)

    h = kec[0]&3
    if h==0:
        r = bl256(kec)
    elif h==1:
        r = gr256(kec)
    elif h==2:
        r = jh256(kec)
    else:
        r = sk256(kec)
    return r
