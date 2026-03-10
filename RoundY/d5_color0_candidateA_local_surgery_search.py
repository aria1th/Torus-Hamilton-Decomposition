#!/usr/bin/env python3
from __future__ import annotations
import itertools, math, json, collections, random
from pathlib import Path

DIM = 5
M = 7

# Candidate A:
BASE_GATES = [
    {'layer':3,'pair':(0,3),'type':'line1','axes':(1,), 'residues':(0,)},
    {'layer':1,'pair':(0,3),'type':'line1','axes':(1,), 'residues':(2,)},
    {'layer':2,'pair':(2,4),'type':'line1','axes':(3,), 'residues':(4,)},
]

def make_orbit_rule(gates, m=M):
    SIGMA=(1,2,3,4,0)
    ID=(0,1,2,3,4)
    def rule(x):
        layer=sum(x)%m
        dirs=list(SIGMA if layer==0 else ID)
        if 1<=layer<=3:
            for gate in gates:
                if gate['layer'] != layer:
                    continue
                typ=gate['type']; pair=tuple(gate['pair'])
                for t in range(DIM):
                    if typ=='plane':
                        ok=True
                    elif typ=='line1':
                        ok=(x[(gate['axes'][0]+t)%DIM] == gate['residues'][0] % m)
                    elif typ=='line2':
                        ok=(x[(gate['axes'][0]+t)%DIM] == gate['residues'][0] % m and x[(gate['axes'][1]+t)%DIM] == gate['residues'][1] % m)
                    else:
                        raise ValueError(typ)
                    if ok:
                        a=(pair[0]+t)%DIM; b=(pair[1]+t)%DIM
                        dirs[a], dirs[b] = dirs[b], dirs[a]
        return tuple(dirs)
    return rule

def x_from_rel(c, rel, m=M):
    q,w,v,u=rel
    arr=[None]*DIM
    arr[(c+1)%DIM]=q; arr[(c+2)%DIM]=w; arr[(c+3)%DIM]=v; arr[(c+4)%DIM]=u
    arr[c]=(-q-w-v-u)%m
    return tuple(arr)

def rel_coords(x,c):
    return tuple(x[(c+k)%DIM] for k in range(1,DIM))

def first_return(rule, c=0, m=M):
    out={}
    for rel in itertools.product(range(m), repeat=4):
        cur=x_from_rel(c, rel, m)
        for _ in range(m):
            d=rule(cur)[c]
            nxt=list(cur); nxt[d]=(nxt[d]+1)%m
            cur=tuple(nxt)
        out[rel]=rel_coords(cur,c)
    return out

def true_cycles(F):
    states=list(F.keys())
    idx={s:i for i,s in enumerate(states)}
    nxt=[idx[F[s]] for s in states]
    color=[0]*len(states)
    cycles=[]
    for i in range(len(states)):
        if color[i]:
            continue
        cur=i; stack=[]; pos={}
        while color[cur]==0:
            color[cur]=1; pos[cur]=len(stack); stack.append(cur); cur=nxt[cur]
        if color[cur]==1:
            cycles.append([states[j] for j in stack[pos[cur]:]])
        for v in stack:
            color[v]=2
    return cycles

def clean_axes(R,m=M):
    goods=[]
    for axis in range(4):
        k=[0]*4; k[axis]=1; k=tuple(k)
        ok=True
        for x,Rx in R.items():
            y=tuple((x[i]+k[i])%m for i in range(4))
            Ry=R[y]
            if tuple((Ry[i]-Rx[i])%m for i in range(4)) != k:
                ok=False; break
        if ok:
            goods.append(axis)
    return goods

def quotient_map(R, fiber_axis, m=M):
    base_axes=[i for i in range(4) if i!=fiber_axis]
    B={}; beta={}
    for base in itertools.product(range(m), repeat=3):
        rel=[0]*4; bi=0
        for i in range(4):
            if i==fiber_axis:
                rel[i]=0
            else:
                rel[i]=base[bi]; bi+=1
        rel=tuple(rel)
        out=R[rel]
        B[base]=tuple(out[i] for i in base_axes)
        beta[base]=(out[fiber_axis]-0)%m
    return B,beta

def strict_clocks(B,m=M):
    return [ax for ax in range(3) if all((B[x][ax]-x[ax])%m==1 for x in B)]

def section_return(B,beta,clock_axis,m=M):
    rem=[i for i in range(3) if i!=clock_axis]
    U={}; mon={}
    for a in itertools.product(range(m), repeat=2):
        base=[0]*3; ai=0
        for j in range(3):
            if j==clock_axis:
                base[j]=0
            else:
                base[j]=a[ai]; ai+=1
        base=tuple(base)
        cur=base; M=0
        for _ in range(m):
            M=(M+beta[cur])%m
            cur=B[cur]
        U[a]=tuple(cur[j] for j in rem)
        mon[a]=M
    return U,mon

def cycle_monodromies(U, mon, m=M):
    cycles=true_cycles(U)
    mons=[]
    for cyc in cycles:
        M=0
        for s in cyc:
            M=(M+mon[s])%m
        mons.append(M)
    return cycles, mons

def indegree_hist(F):
    ctr=collections.Counter(F.values())
    hist=collections.Counter(ctr.values())
    zeros=len(F)-len(ctr)
    if zeros:
        hist[0]=zeros
    return {str(k): hist[k] for k in sorted(hist)}

def bad_count(hist):
    return sum(v for k,v in hist.items() if k != '1')

def best_color0_frame(gates, m=M):
    rule=make_orbit_rule(gates,m)
    R=first_return(rule,0,m)
    Rcycles=true_cycles(R)
    out={
        'R_num_cycles': len(Rcycles),
        'R_cycle_lengths': sorted([len(c) for c in Rcycles], reverse=True),
        'R_indegree_hist': indegree_hist(R),
        'frames': [],
    }
    for fa in clean_axes(R,m):
        B,beta=quotient_map(R,fa,m)
        Bcycles=true_cycles(B)
        for ca in strict_clocks(B,m):
            U,mon=section_return(B,beta,ca,m)
            Ucycles,mons=cycle_monodromies(U,mon,m)
            out['frames'].append({
                'fiber_axis':fa,
                'clock_axis':ca,
                'B_num_cycles': len(Bcycles),
                'B_cycle_lengths': sorted([len(c) for c in Bcycles], reverse=True),
                'B_indegree_hist': indegree_hist(B),
                'U_num_cycles': len(Ucycles),
                'U_cycle_lengths': sorted([len(c) for c in Ucycles], reverse=True),
                'U_indegree_hist': indegree_hist(U),
                'cycle_monodromies': mons,
                'num_unit_monodromies': sum(math.gcd(M,m)==1 for M in mons),
            })
    return out

def main():
    pairs=[p for p in itertools.combinations(range(DIM),2)]
    resvals=[0,1,2,4,6]
    catalog=[]
    for layer in [1,2,3]:
        for pair in pairs:
            catalog.append({'layer':layer,'pair':pair,'type':'plane'})
            for ax in range(DIM):
                for r in resvals:
                    catalog.append({'layer':layer,'pair':pair,'type':'line1','axes':(ax,), 'residues':(r,)})
            for axpair in itertools.combinations(range(DIM),2):
                for r1 in resvals:
                    for r2 in resvals:
                        catalog.append({'layer':layer,'pair':pair,'type':'line2','axes':axpair,'residues':(r1,r2)})

    base = best_color0_frame(BASE_GATES, M)
    base_bad = bad_count(base['R_indegree_hist'])

    random.seed(123)
    sample = random.sample(catalog, 1000)
    same_core = 0
    better_bad = 0
    best_bad = None
    best_bad_gate = None
    examples = []
    for extra in sample:
        if extra in BASE_GATES:
            continue
        diag = best_color0_frame(BASE_GATES + [extra], M)
        good = [fr for fr in diag['frames'] if diag['R_num_cycles']==1 and fr['B_num_cycles']==1 and fr['U_num_cycles']==1 and fr['num_unit_monodromies']==1]
        if not good:
            continue
        same_core += 1
        bad = bad_count(diag['R_indegree_hist'])
        examples.append({'extra_gate': extra, 'R_bad_indeg': bad, 'frame': good[0]})
        if best_bad is None or bad < best_bad:
            best_bad = bad
            best_bad_gate = extra
        if bad < base_bad:
            better_bad += 1

    out = {
        'base_gates': BASE_GATES,
        'base_diag': base,
        'base_bad_indeg': base_bad,
        'sample_size': 1000,
        'num_sampled_with_same_single_core_and_unit_monodromy': same_core,
        'num_sampled_with_strict_improvement_in_bad_indeg': better_bad,
        'best_bad_indeg_found': best_bad,
        'best_extra_gate': best_bad_gate,
        'best_examples': sorted(examples, key=lambda x: x['R_bad_indeg'])[:20],
    }
    out_path = Path('/mnt/data/d5_color0_candidateA_local_surgery_search.json')
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()
