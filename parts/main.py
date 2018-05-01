#!/usr/bin/env python 
__author__ = "Patrik Lundin" 
__copyright__ = "Copyright 2018, nothisispatrik.com" 
__license__ = "GPL v3. Algorithms/constants may be (C) 2014-2018 The Monero project or (C) 2012-2014 The Cryptonote Developers. All code is original"
__email__ = "patrik@nothisispatrik.com"
__status__ = "Prototype"
__doc__ = """ """

from slow import slowhash
import time

def main():
    oinp = [
        0x05, 0x05, 0x84, 0xe2, 0xfa, 0xcc, 0x05, 0xfe, 
        0x5c, 0x31, 0x96, 0xe9, 0x95, 0xae, 0x88, 0x31, 
        0x0b, 0xa8, 0x6e, 0xae, 0x4a, 0xb6, 0x25, 0xab, 
        0xd2, 0x6e, 0x19, 0x2f, 0x26, 0xf3, 0x2c, 0x7d, 
        
        0xcb, 0x6d, 0xb1, 0xd1, 0x08, 0xd7, 0x68, 0x5d, 
        0x00, 0x08, 0x57, 0xd6, 0x62, 0xea, 0x60, 0x02, 
        0xe5, 0x19, 0xa2, 0x76, 0xb9, 0xd6, 0x9a, 0xb9,
        0xf0, 0xdf, 0x14, 0xc9, 0xf5, 0x86, 0xe1, 0x1a,

        0xe4, 0x57, 0xb1, 0xb5, 0x74, 0x05, 0xaf, 0xbf, 
        0x9c, 0xc0, 0xcb, 0x06 ]
    oinp = [0]*76;
    inp = [0]*76;
    st = time.time()
    
    for i in [0]:
        inp[:] = oinp
        inp[0] = (inp[0]+i)%256
        r = slowhash(inp)
        print "+%d: "%(i) + ''.join("%.2x"%(a) for a in r)

    et = time.time()

    # "fc24238f960c14727386295bd0fcecbace8f2aef74ad7108771c7c832b0a9f00"
    # "80563c40ed46575a9e44820d93ee095e2851aa22483fd67837118c6cd951ba61" [0]*76

    print "Total %ds (%f H/s)"%(et-st, 1./(et-st))
    correct_result_new = [0xfc,0x24,0x23,0x8f,0x96,0x0c,0x14,0x72,0x73,0x86,0x29,0x5b,0xd0,0xfc,0xec,0xba,0xce,0x8f,0x2a,0xef,0x74,0xad,0x71,0x08,0x77,0x1c,0x7c,0x83,0x2b,0x0a,0x9f,0x00]

    print "Pass" if correct_result_new==r else "Fail"

res = [
    "fc24238f960c14727386295bd0fcecbace8f2aef74ad7108771c7c832b0a9f00",
    "a6c3144b3a2a01d762f317c113a8ea4bbf8fac063b020d07425cf025c95132b3",
    "346558755f911fe15a8af826990aca7bc439468ae37f1cc32965f6c95e85db64",
    "57f1659185d1873d739a52207ecef33aaa1e8c2c66784868b441d9e11e79d75a",
    "4a5aa85c5d0948b352ff52999592dee24d3aa006a7ea6fd27a77302e38b47895",
    "bd5eea1302118d3ad254e49faa160792210a17077ace5a8273a1ca607fbc6e0e",
    "26d2e51c0727847f5946961fe2fc474ca7dd878f086ac90a2f08e950a7873d91",
    "7e31a24c7302ba8f9c46d85b0ecc375a732269c997215988a131d385a7f0e889",
    "4becb6cee2796c8fae0556c3a7358d4491eb0b96a857d8cee4e1af8d8daca8be",
    "4fbf6fedb67f10f37e7264c0bba9561ab489aee05dfc8d606dc30679fbc564ee",
    "1670fcd3144586c65f7b7266cc1693f658181bfb31be8d7b940200cb3a399c84",
    "003208d5411069b20bdf28ea397e706fada0a209bd65cc742573d355420a2b03",
    "e5ab33a48f2225ee13b5b3215ad85c5dbc203dd2f92f35577cb11d6874c3866f",
    "fe10b195b1f0e8739602237c495e2ecb169194771f48b807d7f5f9bd961639e7",
    "5e144070245d9ed55c8d39eab269345f96445a28bf0f5f5e00ba9753597d3580",
    "d0d084f842e6d1b0aa0cd8dfa83f27314637e2555196d11be7481b26e64eea6f",
    "efa177c61ae8cdfa4a6f976c25ae93e40f8a9ee0bc2de09b27ae94612499d585",
    "d213db5327a9bc1ed31c22cfcdfea11625ceb531d8e12beb188f2e465658e2f7",
    "62e5385d31798aaae89f56dc897f60e10ff7f1a288ca4494cd7e7562f6a4811a",
    "c5d1a81636cfb7a89749ab3705866f428f44b5844f7f64e5554241bc6b43af57",
    "a1ed7ca61a1d972bac78535bf4fec86c95f16a96562a64949c60a6589fd51672",
    "da00b86fcf245a7d7a37fba3cadb94432e2adaa32ffb028f38cb161fa92b409e" ]

if __name__=="__main__":
    main()
