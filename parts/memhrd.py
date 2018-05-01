from aes import around

def memhrd(pad, kec, nonce):
    tw = [a^b for (a,b) in zip(kec[192:],nonce)]

    def mul(a, b):
        t1 = a[0] << 0 | a[1] << 8 | a[2] << 16 | a[3] << 24 | a[4] << 32 | a[5] << 40 | a[6] << 48 | a[7] << 56
        t2 = b[0] << 0 | b[1] << 8 | b[2] << 16 | b[3] << 24 | b[4] << 32 | b[5] << 40 | b[6] << 48 | b[7] << 56
        r = t1 * t2
        r1 = r >> 64
        r2 = r & 0xffffffffffffffffL
        return [ r1&255, (r1>>8)&255, (r1>>16)&255, (r1>>24)&255, (r1>>32)&255, (r1>>40)&255, (r1>>48)&255, (r1>>56)&255, r2&0xff, (r2>>8)&255, (r2>>16)&255,(r2>>24)&255,  (r2>>32)&255, (r2>>40)&255, (r2>>48)&255, (r2>>56)&255 ]

    def sumhlf(a, b):
        ta1 = a[0] << 0 | a[1] << 8 | a[2] << 16 | a[3] << 24 | a[4] << 32 | a[5] << 40 | a[6] << 48 | a[7] << 56
        ta2 = a[8] << 0 | a[9] << 8 | a[10] << 16 | a[11] << 24 | a[12] << 32 | a[13] << 40 | a[14] << 48 | a[15] << 56
        tb1 = b[0] << 0 | b[1] << 8 | b[2] << 16 | b[3] << 24 | b[4] << 32 | b[5] << 40 | b[6] << 48 | b[7] << 56
        tb2 = b[8] << 0 | b[9] << 8 | b[10] << 16 | b[11] << 24 | b[12] << 32 | b[13] << 40 | b[14] << 48 | b[15] << 56
        r1,r2 = (ta1 + tb1 & 18446744073709551615L, ta2 + tb2 & 18446744073709551615L)
        return [ r1&255, (r1>>8)&255, (r1>>16)&255, (r1>>24)&255, (r1>>32)&255, (r1>>40)&255, (r1>>48)&255, (r1>>56)&255, r2&0xff, (r2>>8)&255, (r2>>16)&255,(r2>>24)&255,  (r2>>32)&255, (r2>>40)&255, (r2>>48)&255, (r2>>56)&255 ]

        # xor two blocks
    def blxor(a, b):
        return [ t1 ^ t2 for t1, t2 in zip(a, b) ]

        # pull 17 bits from a block for use as an address in the scratchpad.
        # Zeroes out the 4 LSB rather than dividing, making it useful as an
        # index in the pad directly. >>4 instead of &.. would give a block
        # index, which could then later be <<4 to give an actual location.
    def toaddr(a):
        return (a[2] << 16 | a[1] << 8 | a[0]) & 2097136

        # make the first two indexes
    A = blxor(kec[0:16], kec[32:48])
    B = blxor(kec[16:32], kec[48:64])

    for R in xrange(1<<19):
        t = toaddr(A)
        C = pad[t:t + 16]
        C = around(C)
        C = blxor(C, A)
        pad[t:(t + 16)] = blxor(B, C)

            # After the Apr 2018 hardfork, this will be/was
            # added to the loop. This is equivalent to VARIANT1_1
            # in the original C. 
        a = pad[t+11]
        a = (~a&1)<<4 | ((~a&1)<<4 & a)<<1 | (a&32)>>1
        pad[t+11] ^= a


        B = C
        t = toaddr(C)
        C = pad[t:t + 16]

        P = mul(B, C)
        A = sumhlf(A, P)
        pad[t:(t + 16)] = A

        # this is the second variant add in, equivalent of VARIENT1_2 in
        # C. 
        for i in range(8):
            pad[t+i+8] ^= tw[i]

        A =  blxor(A, C)
        #if ((R % 10000) == 0):
            #print "A = %.2x %.2x %.2x %.2x %.2x %.2x %.2x %.2x %.2x %.2x %.2x %.2x %.2x %.2x %.2x %.2x "%tuple(A[i] for i in range(16))

    return pad
