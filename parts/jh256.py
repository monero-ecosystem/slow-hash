#!/usr/bin/env python 
__author__ = "Patrik Lundin" 
__copyright__ = "Copyright 2018, nothisispatrik.com" 
__license__ = "LGPL v3. Algorithms/constants may be (C) 2014-2018 The Monero project or (C) 2012-2014 The Cryptonote Developers. All code is original."
__email__ = "patrik@nothisispatrik.com"
__status__ = "Prototype"
__doc__ = """ JH hash. """

def jh256(data):
    """Calculates JH hash. Takes 200b (as a list of bytes), produces 32b.

    Ex:
    print jh([0]*200)
    # [200, 113, 234, 67, 7, 55, 207, 116, 141, 116, 25, 215, 10, 223, 100, 116, 197, 229, 175, 240, 231, 121, 229, 224, 151, 141, 137, 141, 55, 7, 98, 31]

    """
    hashval = [32]
    A = [0]*256
    rc = [0]*64
    rcx = [0]*256
    tmp = [0]*256
    S = [[9,0,4,11,13,12,3,15,1,10,2,6,7,5,8,14],[3,12,6,13,5,7,1,9,15,2,0,4,11,10,14,8]] 
    rc0 = [0x6,0xa,0x0,0x9,0xe,0x6,0x6,0x7,0xf,0x3,0xb,0xc,0xc,0x9,0x0,0x8,0xb,0x2,0xf,0xb,0x1,0x3,0x6,0x6,0xe,0xa,0x9,0x5,0x7,0xd,0x3,0xe,0x3,0xa,0xd,0xe,0xc,0x1,0x7,0x5,0x1,0x2,0x7,0x7,0x5,0x0,0x9,0x9,0xd,0xa,0x2,0xf,0x5,0x9,0x0,0xb,0x0,0x6,0x6,0x7,0x3,0x2,0x2,0xa]
    d = [254,0,64,128,255,254] 

    H = [1]+[0]*127

    for b in d:
        if b<=128:
            for i in range(64):
                H[i] ^= data[b+i]
        elif b==255:
            H[:8] = [H[i]^data[192+i] for i in range(8)]
            H[8] ^= 128
        rc = rc0[:]

        for i in range(256):
            t0 = (H[i>>3] >> (7 - (i & 7)) ) & 1
            t1 = (H[(i+256)>>3] >> (7 - (i & 7)) ) & 1
            t2 = (H[(i+512 )>>3] >> (7 - (i & 7)) ) & 1
            t3 = (H[(i+768 )>>3] >> (7 - (i & 7)) ) & 1
            tmp[i] = (t0 << 3) | (t1 << 2) | (t2 << 1) | (t3 << 0)
        for i in range(128):
            A[i << 1] = tmp[i]
            A[(i << 1)+1] = tmp[i+128]

        for r in range(42):
            for i in range(256):
                rcx[i] = (rc[i >> 2] >> (3 - (i & 3)) ) & 1
            for i in range(256):
                tmp[i] = S[rcx[i]][A[i]]
            for i in range(0,256,2):
                t0 = tmp[i+1]^(((tmp[i]<<1)^(tmp[i]>>3)^((tmp[i]>>2)&2))&0xf)
                t1 = tmp[i+0]^(((t0<<1)^(t0>>3)^((t0>>2)&2))&0xf)
                t2 = (i>>1)&1
                tmp[i+t2^1] = t0
                tmp[i+t2] = t1
            for i in range(128):
                A[i] = tmp[i<<1] 
                A[(i+128)^1] = tmp[(i<<1)+1] 
            for i in range(64):
                tmp[i] = S[0][rc[i]]
            for i in range(0,64,2):
                tmp[i+1] ^= ((tmp[i]<<1)^(tmp[i]>>3)^((tmp[i]>>2)&2))&0xf
                tmp[i] ^= ((tmp[i+1]<<1)^(tmp[i+1]>>3)^((tmp[i+1]>>2)&2))&0xf
            for i in range(0,64,4):
                t = tmp[i+2]
                tmp[i+2] = tmp[i+3]
                tmp[i+3] = t
            for i in range(32):
                rc[i] = tmp[i<<1]  
                rc[(i+32)^1] = tmp[(i<<1)+1]

        for i in range(128):
            tmp[i] = A[i << 1]
            tmp[i+128] = A[(i << 1)+1]
        for i in range(128):
            H[i] = 0
        for i in range(256):
            t0 = (tmp[i] >> 3) & 1
            t1 = (tmp[i] >> 2) & 1
            t2 = (tmp[i] >> 1) & 1
            t3 = (tmp[i] >> 0) & 1
            H[i>>3] |= t0 << (7 - (i & 7))
            H[(i + 256)>>3] |= t1 << (7 - (i & 7))
            H[(i + 512)>>3] |= t2 << (7 - (i & 7))
            H[(i + 768)>>3] |= t3 << (7 - (i & 7))

        if b<=128:
            for i in range(64):
                H[i+64] ^= data[b+i]
        elif(b==255):
            for i in range(8):
                H[64+i] ^= data[192+i]
            H[8+64] ^= 128
            H[63] ^= 64
            H[62] ^= 6 
    H[127] ^= 64
    H[126] ^= 6
    return H[96:]
