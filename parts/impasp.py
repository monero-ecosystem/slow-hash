from aes import around, kexp

def asplode(kec):
    xkey = kexp(kec[:32])
    st = kec[64:192]
    xk = [ xkey[i:i + 16] for i in range(0, len(xkey), 16) ]
    pad = []
    while len(pad) < 2097152:
        for j in range(0, len(st), 16):
            t = st[j:j + 16]
            for i in range(10):
                t = around(t)
                t = [ a ^ b for a, b in zip(t, xk[i]) ]
            pad.extend(t)
        st = pad[-128:]
    return pad

    # combine final scratchpad into a single block again by xoring and
    # then 10 round AESing the blocks over each other one at a time
def implode(pad,kec):
    xkey = kexp(kec[32:64])
    xk = [ xkey[i:i + 16] for i in range(0, len(xkey), 16) ]
    st = kec[64:192]
    for p in range(0,len(pad),128):
        for i in xrange(128):
            st[i] ^= pad[p+i]
        for i in xrange(0,128,16):
            for r in xrange(10):
                st[i:i+16] = around(st[i:i+16])
                for j in xrange(16):
                    st[i+j] ^= xk[r][j]

    kec[64:192] = st
    return kec

