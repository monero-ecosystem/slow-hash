#!/usr/bin/env python 
__author__ = "Patrik Lundin" 
__copyright__ = "Copyright 2018, nothisispatrik.com" 
__license__ = "LGPL v3. Algorithms/constants may be (C) 2014-2018 The Monero project or (C) 2012-2014 The Cryptonote Developers. All code is original."
__email__ = "patrik@nothisispatrik.com"
__status__ = "Prototype"
__doc__ = """Skein hash"""

def sk256(data):
    """Calculates skein hash. Takes 200b (as a list of bytes), produces 32b 

    Ex:
    print sk256([0]*200)
    # [178, 2, 102, 82, 29, 57, 214, 35, 190, 244, 193, 182, 117, 91, 72, 111, 200, 125, 2, 195, 49, 198, 58, 59, 63, 248, 22, 135, 108, 248, 160, 106]

    """
    def M(x): # Mask down to 64 bin
        return x & 0xffffffffffffffffL
    def R64(x, p, n): # Rotate left, 64 bit
        x[p] = M((x[p] << n) | (x[p] >> (64-n)))
    def Add(x, a, b): # 64 bit add, no overflow
        x[a] = M(x[a]+x[b])

    def R512(X,p0,p1,p2,p3,p4,p5,p6,p7,q):
        Rk = [ [46, 36, 19, 37], [33, 27, 14, 42], [17, 49, 36, 39], [44,  9, 54, 56], [39, 30, 34, 24], [13, 50, 10, 17], [25, 29, 39, 43], [ 8, 35, 56, 22]]
        
        Add(X,p0,p1)
        R64(X,p1,Rk[q][0])
        X[p1] ^= X[p0] 

        Add(X,p2,p3)
        R64(X,p3,Rk[q][1])
        X[p3] ^= X[p2]

        Add(X,p4,p5)
        R64(X,p5,Rk[q][2])
        X[p5] ^= X[p4]

        Add(X,p6,p7)
        R64(X,p7,Rk[q][3])
        X[p7] ^= X[p6] 

        # Skein types and lengths. Since it's just five blocks, always
        # same length and such, they're constant. Here as TYPE | LEN,
        # as it is stored in Skeins T(2)
    LC = [ 0x7000000000000040L, 0x3000000000000080L, 0x30000000000000c0L,
        0xb0000000000000c8L, 0xff00000000000008L ]
        # Init vector. Specific to 512-256 hash
    L = [ 0,0,0, 0xCCD044A12FDB3E13L, 0xE83590301A79A9EBL, 
          0x55AEA0614F816E6FL, 0x2A2767A4AE9B94DBL, 0xEC06025E74DD7683L,
          0xE7A436CDC4746251L, 0xC36FBAF9393AD185L, 0x3EEDBA1833EDFC13L, 0]
        # Keeper of data. Extra length so that after the 200b we send,
        # there's enough zeros for another full block, and, for the
        # OUT+FINAL block, one with all zeros. 
    b = [0]*35
        # Offset to current data. Hops around
    w = 0
        # Temp state data
    X = [0]*8;
        # fill b up with 8b words
    for i in range(25):
        b[i] = ( 
            (data[(i*8)+0]<<0)|
            (data[(i*8)+1]<<8)|
            (data[(i*8)+2]<<16)|
            (data[(i*8)+3]<<24)|
            (data[(i*8)+4]<<32)|
            (data[(i*8)+5]<<40)|
            (data[(i*8)+6]<<48)|
            (data[(i*8)+7]<<56))
        # Each block..
    for i in range(5): 
            # T2 = T1^T0, like we stored
        L[2] = LC[i]
            # T0 = length. Extract with &0xff
        L[0] = L[2]&255; 
            # T2 = type+flags. Exract by removing T0
        L[1] = L[2]^L[0];
            # Parity + magic constant.
        L[11] = L[3]^L[4]^L[5]^L[6]^L[7]^L[8]^L[9]^L[10]^0x1BD11BDAA9FC1A22L;
            # Next chunk
        w = ((i&3)<<3)+25*(i>>2);
            # Init X
        for R in range(8):
            X[R]= M(b[w+R] + L[R+3])
        X[5]=M(X[5]+L[0])
        X[6]=M(X[6]+L[1])

            # Rounds
        for R in range(0,18,2):
            R512(X,0,1,2,3,4,5,6,7,0)
            R512(X,2,1,4,7,6,5,0,3,1)
            R512(X,4,1,6,3,0,5,2,7,2)
            R512(X,6,1,0,7,2,5,4,3,3)
            for j in range(8):
                X[j] = M(X[j]+L[3+((R+j+1)%9)])
            X[5] = M(X[5]+L[(R+1)%3])
            X[6] = M(X[6]+L[(R+2)%3])
            X[7] = M(X[7]+R+1)
            R512(X,0,1,2,3,4,5,6,7,4)
            R512(X,2,1,4,7,6,5,0,3,5)
            R512(X,4,1,6,3,0,5,2,7,6)
            R512(X,6,1,0,7,2,5,4,3,7)
            for j in range(8):
                X[j] = M(X[j]+L[3+((R+j+2)%9)])
            X[5] = M(X[5]+L[(R+2)%3])
            X[6] = M(X[6]+L[(R+3)%3])
            X[7] = M(X[7]+R+2)

            # Back into state w/ round results
        for R in range(8):
            L[3+R] = X[R] ^ b[w+R] 

        # Done, make bytes of it
    return [int((l>>n)&255) for l in L[3:7] for n in range(0,64,8)]
