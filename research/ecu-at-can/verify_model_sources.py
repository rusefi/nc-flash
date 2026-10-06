"""Stock ECU model maps and sources -> CAN215 -> TCU -> ECU spark.

Bounded RTZ arithmetic, original lookup bodies, explicit scheduling and source
fixtures. Physical input identities, full task history and CAN211 sender are
not inferred from the numeric model. The TCU active phase3 remains a fixture.
"""
from fractions import Fraction
import hashlib
import itertools
import json
import math
import struct

from sh_model_float import SHModelFloat
from sh_exact_float import exact_value, exact_bits
from sh_rtz_float import rtz_bits
from sh_subset import MASK
from verify_can201_byte6 import ECU, TCU, w, r
from verify_spark_interaction import f, rf, TRACTION, AT, GATES
from verify_can215_feedback import receive, clamp
from verify_tcu_spark_requests import ramp_fixture

MAPS = [(0xA223C, 0xA2250, 0xA2264), (0xA22A0, 0xA22DC, 0xA2318),
        (0xA228C, 0xA22C8, 0xA2304), (0xA2278, 0xA22B4, 0xA22F0)]


def rounded(x):
    return exact_value(rtz_bits(x))


def number(a):
    return exact_value(int.from_bytes(ECU[a:a+4], 'big'))


def axis(a, n):
    return [number(a+4*i) for i in range(n)]


def position(values, x):
    if x <= values[0]:
        return 0, Fraction(0)
    if x >= values[-1]:
        return len(values)-1, Fraction(0)
    i = next(i for i in range(len(values)-1) if values[i] <= x < values[i+1])
    return i, rounded(rounded(x-values[i])/rounded(values[i+1]-values[i]))


def interpolate(a, b, t):
    # SH-2E FMAC uses rounded multiply followed by rounded addition.
    return a if t == 0 else rounded(a+rounded(t*rounded(b-a)))


def map2_info(address):
    nx, ny, xp, yp, vp = struct.unpack_from('>HHIII', ECU, address)
    assert ECU[address+16] == 0  # float table, no encoded-value postscale
    return axis(xp, nx), axis(yp, ny), vp


def lookup2(address, x, y):
    xs, ys, vp = map2_info(address)
    ix, fx = position(xs, x); iy, fy = position(ys, y)
    nx = len(xs)
    def row(j):
        a = number(vp+4*(j*nx+ix))
        return interpolate(a, number(vp+4*(j*nx+min(ix+1,nx-1))), fx)
    return interpolate(row(iy), row(min(iy+1,len(ys)-1)), fy)


def lookup1(address, x):
    n = int.from_bytes(ECU[address:address+2], 'big')
    assert ECU[address+2] == 0
    xp, vp = struct.unpack_from('>II', ECU, address+4)
    i, f = position(axis(xp,n), x)
    return interpolate(number(vp+4*i), number(vp+4*min(i+1,n-1)), f)


def branch(active, mask, variant):
    return 0 if active == 0 else 1 if mask == 0 else 3 if variant == 1 else 2


def quadratic(a, center, peak, command):
    delta = rounded(center-command)
    return rounded(peak-rounded(rounded(a*delta)*delta))


def initialize_sources(x=2000, y=Fraction(1,2), active=0, mask=0, variant=0,
                       spark=20, baseline=25, count=0, temperature=80, extra=0, count_index=None):
    e = SHModelFloat(ECU)
    for a,v in [(0x6DB4,x), (0x6F20,y), (0x7A74,spark), (0x7A80,baseline),
                (0x6D20,temperature), (0x6CD4,extra), (0x6814,1),
                (0x67DC,2000), (0x6828,0), (0x7258,0)]:
        f(e,a,v)
    for a,v in [(0x718C,active), (0x74F1,mask), (0x657E,variant), (0x71F0,count)]:
        w(e,a,v)
    # These producers appear in this relative order in the saved main-task
    # disassembly, with other work between them that is outside this fixture.
    for fn in [0x407B4,0x40916,0x4097E]:e.run(fn)
    if count_index is not None:
        w(e,0x7182,count_index)
        e.run(0x40660)
    for fn in [0x40560,0x40888,0x409AC]:e.run(fn)
    return e


def feedback(active, mask, variant, count, request, elapsed, count_index=None):
    e = initialize_sources(active=active, mask=mask, variant=variant, count=count, count_index=count_index)
    count,mask=r(e,0x71F0),r(e,0x74F1)
    sources = {hex(a): float(rf(e,a)) for a in [0x71A8,0x71AC,0x71B0,0x71F4,0x71F8,
               0x71CC,0x71D0,0x71D8,0x71E0,0x71C4,0x71EC,0x71B4,0x71C0]}
    w(e,0x734A,0x80)
    e.run(0x369D6);e.run(0x36A28)
    payload=bytes(r(e,0x6B50+i) for i in range(8))
    raw=[int.from_bytes(payload[i:i+2],'big') for i in [0,2,4]]
    t=ramp_fixture(elapsed=elapsed)
    receive(t,payload)
    # No pending faults; calculate shared validity and summaries from originals.
    w(t,0xA939,1)
    for fn in [0x583DC,0x570F6,0x57258,0x516E6,0x517B2,0x216D8,0x2C234,0x1FB8C]:t.run(fn)
    first=clamp(10*(raw[0]-raw[2]),-1000,9240)
    assert r(t,0x80B4,2)==first & 65535
    base=int(Fraction(first*32,10))
    expected_source=max(base-320*(10-elapsed)//10,0) if elapsed<10 else 32767
    assert r(t,0x915A,2)==expected_source
    w(t,0x9454,0);w(t,0x92C6,0x20)
    t.run(0x18F10,1);t.run(0x18F8C,1)
    for a,v in {**GATES,0x734A:0x80,0x734C:1,0x6A5D:1,0x6590:1,0x6566:1,
                0xA488:1,0x6567:1,0x65F0:1}.items():w(e,a,v)
    for a,v in [(0x7140,50),(0x7A84,25),(0x7D38,100),(0x7F0C,4),(0x7A7C,-60),
                (0x7C94,30),(0x7ACC,60)]:f(e,a,v)
    for i in range(8):w(e,0x6A40+i,r(t,0x8EFD+i))
    w(e,0x6A10,10000+request,2)
    for fn in AT+TRACTION:e.run(fn)
    decoded=65022 if expected_source==32767 else expected_source//32
    assert rf(e,0x6E04)==decoded
    assert r(e,0x6E3A)==(rf(e,0x71C0)>decoded)
    # Independently evaluate the two inverse models using the produced stock
    # coefficients, then the original bounded quarter-step root algorithm.
    a,center,peak=rf(e,0x71A8),rf(e,0x71AC),rf(e,0x71B0)
    def inverted(q):
        return rounded(center-Fraction(math.isqrt(int(max(q,0)*16)),4))
    qa=rounded(rounded(rounded(rounded(peak-decoded)-rf(e,0x71E0))-rf(e,0x71CC))+rf(e,0x71D0))
    qa=rounded(max(qa,0)/a)
    qt=rounded(rounded(rounded(peak-rf(e,0x7170))+rf(e,0x71D0))+rf(e,0x71D8))
    qt=rounded(max(qt,0)/a)
    assert rf(e,0x6E08)==inverted(qa)
    assert rf(e,0x7174)==inverted(qt)
    ac=min(rounded(25-inverted(qa)),number(0xBFAE4)) if r(e,0x6E3A)==r(e,0x6E2F)==1 else 0
    tc=clamp(rounded(25-inverted(qt)),0,100) if r(e,0x718C)!=0 else 0
    assert rf(e,0x7C74)==ac and rf(e,0x7D2C)==tc
    for fn in [0x4FD9C,0x4FBDA,0x4FB4E]:e.run(fn)
    total=rounded(rounded(Fraction(4)+tc)+ac)
    # Final limits may intervene with stock model coefficients; verify the
    # original ordinary branch's bound as well as four unchanged stock trims.
    assert rf(e,0x7A90)==total
    expected=clamp(rounded(Fraction(30)-total),rf(e,0x7AD0),50)
    assert rf(e,0x7A78)==expected
    outputs=[rf(e,a) for a in [0x7A9C,0x7AA0,0x7AA4,0x7AA8]]
    assert outputs==[expected]*4
    return {'source_flags':[active,mask,variant],'count':count,'count_source_index':count_index,'can211_request':request,
            'phase3_timer':elapsed,'model_sources':sources,'can215':payload.hex(' '),
            'tcu_base':base,'tcu_source':expected_source,'at_decoded':decoded,
            'at_enabled':r(e,0x6E3A),'traction_active':r(e,0x718C),
            'at_correction':float(ac),'traction_correction':float(tc),
            'spark':[float(v) for v in outputs]}


def main():
    transfers=0
    for reg,value,sr in itertools.product(range(16),[0,1,0x80000000,0xFFFFFFFF,0x12345678],[0,0x3F1]):
        for load in [False,True]:
            opcode=(0x4006 if load else 0x4002)|(reg<<8)
            e=SHModelFloat(opcode.to_bytes(2,'big'))
            e.r[reg]=0xFFFFB004;e.mach=value;e.macl=0xABCDEF01;e.sr=sr
            e.write(0xFFFFB004,value^0xFFFFFFFF,4)
            assert e.instruction(0)==(2,False)
            assert e.r[reg]==(0xFFFFB008 if load else 0xFFFFB000)
            assert e.mach==(value^0xFFFFFFFF if load else value)
            if not load:assert e.read(0xFFFFB000,4)==value
            assert e.macl==0xABCDEF01 and e.sr==sr
            transfers+=1
    products=0
    for n,m,pair in itertools.product(range(16),range(16),[(0,0),(-1,2),(-32768,-32768),(32767,32767),(-32768,32767)]):
        e=SHModelFloat((0x200F|n<<8|m<<4).to_bytes(2,'big'));a,b=pair
        e.r[n]=0xABCD0000|(a&65535);e.r[m]=0x12340000|(b&65535)
        old=e.r[:];e.mach=0x87654321;e.sr=0x3F1
        e.instruction(0)
        assert e.macl==((b*b if n==m else a*b)&MASK)
        assert e.r==old and e.mach==0x87654321 and e.sr==0x3F1
        products+=1

    negations=0
    for reg,bits in itertools.product(range(16),[0,0x80000000,0x3F800000,0xBF800000,0x7F7FFFFF,0xFF7FFFFF]):
        e=SHModelFloat((0xF04D|reg<<8).to_bytes(2,'big'));e.fr[reg]=bits;e.sr=0x3F1
        e.instruction(0)
        assert e.fr[reg]==bits^0x80000000 and e.sr==0x3F1
        negations+=1
    rejections=0
    for bits in [1,0x80000001,0x7F800000,0x7FC12345]:
        e=SHModelFloat(bytes.fromhex('f04d'));e.fr[0]=bits
        try:e.instruction(0)
        except ValueError:rejections+=1
        else:raise AssertionError('FNEG accepted outside bounded domain')

    map_cases=0
    for address in [a for group in MAPS for a in group]+[0xA232C]:
        xs,ys,vp=map2_info(address)
        points=list(itertools.product(xs,ys))
        points+=list(itertools.product([(a+b)/2 for a,b in zip(xs,xs[1:])],[(a+b)/2 for a,b in zip(ys,ys[1:])]))
        points+=list(itertools.product([xs[0]-1,xs[-1]+1],[ys[0]-1,ys[-1]+1]))
        for x,y in points:
            e=SHModelFloat(ECU);e.fr[4]=exact_bits(x);e.fr[5]=exact_bits(y)
            e.mach=0x12345678;e.macl=0x87654321
            e.run(0x236C,address)
            assert exact_value(e.fr[0])==lookup2(address,x,y),(hex(address),x,y)
            assert e.mach==0x12345678 and e.macl==0x87654321
            map_cases+=1
    curves=0
    for address in [0xA2218,0xA2224,0xA2230]:
        n=int.from_bytes(ECU[address:address+2],'big');xp=int.from_bytes(ECU[address+4:address+8],'big');xs=axis(xp,n)
        for x in xs+[(a+b)/2 for a,b in zip(xs,xs[1:])]+[xs[0]-1,xs[-1]+1]:
            e=SHModelFloat(ECU);e.fr[4]=exact_bits(x);e.run(0x22F8,address)
            assert exact_value(e.fr[0])==lookup1(address,x)
            curves+=1

    producers=0
    for active,mask,variant,point,sparks in itertools.product([0,1,2],[0,1,255],[0,1,2],
                  [(1000,Fraction(0)),(2250,Fraction(15,32)),(8000,Fraction(1))],[(20,25),(30,10),(0,0)]):
        x,y=point;command,baseline=sparks;e=initialize_sources(x,y,active,mask,variant,command,baseline)
        a,b,c=[lookup2(addr,x,y) for addr in MAPS[branch(active,mask,variant)]]
        assert [rf(e,z) for z in [0x71A8,0x71AC,0x71B0]]==[a,b,c]
        assert rf(e,0x71F4)==quadratic(a,b,c,command)
        assert rf(e,0x71F8)==quadratic(a,b,c,baseline)
        cc=lookup2(0xA232C,x,80);d0=cc
        d8=rounded(max(rounded(lookup1(0xA2218,x)-d0),0)*lookup1(0xA2224,0))
        assert [rf(e,z) for z in [0x71CC,0x71D0,0x71D8]]==[cc,d0,d8]
        assert rf(e,0x71C4)==rounded(cc+d8)
        assert rf(e,0x71EC)==rounded(rounded(rf(e,0x71F8)+d0)+d8)
        assert rf(e,0x71B4)==rounded(rounded(rf(e,0x71F4)+d0)+d8)
        assert rf(e,0x71C0)==rounded(rf(e,0x71EC)-rf(e,0x71C4))
        producers+=1

    auxiliary_cases=0
    for x,temp,extra in itertools.product([1000,2250,8000],[-40,0,80,100],[0,25,50,100]):
        e=SHModelFloat(ECU)
        for a,v in [(0x6DB4,x),(0x6D20,temp),(0x6CD4,extra)]:f(e,a,v)
        e.run(0x407B4)
        cc=lookup2(0xA232C,x,temp);d0=lookup2(0xA232C,x,80)
        d8=rounded(max(rounded(lookup1(0xA2218,x)-d0),0)*lookup1(0xA2224,extra))
        assert [rf(e,a) for a in [0x71CC,0x71D0,0x71D8]]==[cc,d0,d8]
        auxiliary_cases+=1
    auxiliary_ratio_cases=0
    for divisor,numerator,x,gate in itertools.product([0,Fraction(-1,4),Fraction(1,4),Fraction(1,2),1,2],[-4,0,4],[1000,2250,6500],[0,1,2]):
        e=SHModelFloat(ECU)
        for a,v in [(0x6814,divisor),(0x6828,numerator),(0x67DC,x),(0x7200,9)]:f(e,a,v)
        w(e,0x67AC,gate);e.run(0x40916)
        value=rounded(rounded(Fraction(numerator,divisor))*lookup1(0xA2230,x)) if abs(divisor)>number(0x40A30) else Fraction(9)
        assert rf(e,0x7200)==value
        assert rf(e,0x71E0)==(rounded(value+number(0xC1428)) if gate==1 else value)
        auxiliary_ratio_cases+=1

    count_producer_cases=0
    for flags,force,active,index,phase,variant in itertools.product([0,0x20,0x40,0x60],[0,1,2],[0,1,2],range(6),range(5),range(2)):
        e=SHModelFloat(ECU)
        for a,v in [(0x73C4,flags),(0x73B8,force),(0x718C,active),(0x7182,index),(0x74F2,phase),(0x6542,variant)]:w(e,a,v)
        e.run(0x40660)
        mask=r(e,0x74F1)
        expected=8 if flags&0x60 or force==1 else mask.bit_count() if active==1 else 0
        assert r(e,0x71F0)==expected
        count_producer_cases+=1

    count_cases=0
    for count,first,second in itertools.product(range(256),[-16,0,32],[-8,0,24]):
        e=SHModelFloat(ECU);w(e,0x71F0,count)
        for a,v in [(0x71F4,first),(0x71F8,second),(0x71D0,2),(0x71D8,4),
                    (0x71CC,3),(0x71E0,5),(0x7258,7)]:f(e,a,v)
        for fn in [0x4097E,0x40888,0x409AC]:e.run(fn)
        scaled=Fraction((first+6)*max(8-count,0),8)
        assert rf(e,0x71B4)==scaled and rf(e,0x71EC)==second+6
        assert rf(e,0x71C4)==19 and rf(e,0x71B8)==scaled-19
        assert rf(e,0x71BC)==first+6-19 and rf(e,0x71C0)==second+6-19
        count_cases+=1

    examples=[feedback(*flags,count,request,elapsed) for flags,count,request,elapsed in itertools.product(
        [(0,0,0),(1,0,0),(1,1,0),(1,1,1)],[0,2,4,8],[0,16,50],[0,5,10])]
    produced_count_feedback=[feedback(1,0,0,0,request,elapsed,count_index=index)
        for index,request,elapsed in itertools.product(range(6),[0,16,50],[0,5,10])]
    print(json.dumps({'scope':__doc__.strip(),'rom_sha256':{'ECU':hashlib.sha256(ECU).hexdigest(),'TCU':hashlib.sha256(TCU).hexdigest()},
                     'mach_transfer_cases':transfers,'signed_multiply_cases':products,'finite_negation_cases':negations,
                     'expected_nonfinite_subnormal_rejections':rejections,'map_cases':map_cases,
                     'curve_cases':curves,'full_source_producer_cases':producers,'auxiliary_map_cases':auxiliary_cases,
                     'auxiliary_ratio_cases':auxiliary_ratio_cases,'count_producer_cases':count_producer_cases,
                     'count_and_offset_cases':count_cases,'produced_count_feedback_cases':len(produced_count_feedback),
                     'produced_count_feedback':produced_count_feedback,
                     'feedback_cases':len(examples),'feedback':examples,
                     'limits':'Original stock coefficients and source producers execute; source sensor/state values, count and TCU phase3 are fixtures. Global ECU scheduler, upstream count-index producer, physical units, CAN211 sender and roof integration remain incomplete.'},indent=2))


if __name__=='__main__':main()
