#!/usr/bin/env python3
from __future__ import annotations
import itertools, math, json, collections, random
from pathlib import Path

DIM = 5

def make_orbit_rule(gates, m):
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

def x_from_rel(c, rel, m):
    q,w,v,u=rel
    arr=[None]*DIM
    arr[(c+1)%DIM]=q; arr[(c+2)%DIM]=w; arr[(c+3)%DIM]=v; arr[(c+4)%DIM]=u
    arr[c]=(-q-w-v-u)%m
    return tuple(arr)

def rel_coords(x,c):
    return tuple(x[(c+k)%DIM] for k in range(1,DIM))

def first_return(rule, c, m):
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

def clean_axes(R,m):
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

def quotient_map(R, fiber_axis, m):
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
    return B,beta,base_axes

def strict_clocks(B,m):
    return [ax for ax in range(3) if all((B[x][ax]-x[ax])%m==1 for x in B)]

def section_return(B,beta,clock_axis,m):
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

def indegree_hist(F):
    ctr=collections.Counter(F.values())
    hist=collections.Counter(ctr.values())
    zeros=len(F)-len(ctr)
    if zeros:
        hist[0]=zeros
    return {str(k): hist[k] for k in sorted(hist)}

def cycle_monodromies(U, mon, m):
    cycles=true_cycles(U)
    mons=[]
    for cyc in cycles:
        M=0
        for s in cyc:
            M=(M+mon[s])%m
        mons.append(M)
    return cycles, mons

def summarize_candidate(gates, m_list, colors=None):
    out={'gates':gates, 'm':{}}
    for m in m_list:
        rule=make_orbit_rule(gates,m)
        colors_here = colors if colors is not None else [0]
        out['m'][str(m)]={}
        for c in colors_here:
            R=first_return(rule,c,m)
            Rcycles=true_cycles(R)
            entry={
                'clean_axes': clean_axes(R,m),
                'R_cycle_lengths': sorted([len(cyc) for cyc in Rcycles], reverse=True),
                'R_num_cycles': len(Rcycles),
                'R_indegree_hist': indegree_hist(R),
                'frames': []
            }
            for fa in entry['clean_axes']:
                B,beta,base_axes=quotient_map(R,fa,m)
                Bcycles=true_cycles(B)
                frame={
                    'fiber_axis': fa,
                    'base_axes': list(base_axes),
                    'B_cycle_lengths': sorted([len(cyc) for cyc in Bcycles], reverse=True),
                    'B_num_cycles': len(Bcycles),
                    'B_indegree_hist': indegree_hist(B),
                    'clock_axes': strict_clocks(B,m),
                    'sections': []
                }
                for ca in frame['clock_axes']:
                    U,mon=section_return(B,beta,ca,m)
                    Ucycles,mons=cycle_monodromies(U,mon,m)
                    frame['sections'].append({
                        'clock_axis': ca,
                        'U_cycle_lengths': sorted([len(cyc) for cyc in Ucycles], reverse=True),
                        'U_num_cycles': len(Ucycles),
                        'U_indegree_hist': indegree_hist(U),
                        'cycle_monodromies': mons,
                    })
                entry['frames'].append(frame)
            out['m'][str(m)][str(c)] = entry
    return out

def main():
    seed1=[
        {'layer':3,'pair':(0,3),'type':'line1','axes':(1,), 'residues':(0,)},
    ]
    seed2=[
        {'layer':3,'pair':(0,3),'type':'line1','axes':(1,), 'residues':(0,)},
        {'layer':1,'pair':(0,3),'type':'line1','axes':(1,), 'residues':(2,)},
    ]
    candA=[
        {'layer':3,'pair':(0,3),'type':'line1','axes':(1,), 'residues':(0,)},
        {'layer':1,'pair':(0,3),'type':'line1','axes':(1,), 'residues':(2,)},
        {'layer':2,'pair':(2,4),'type':'line1','axes':(3,), 'residues':(4,)},
    ]
    out = {
        'seed1': summarize_candidate(seed1, [5,7,9], colors=[0]),
        'seed2': summarize_candidate(seed2, [5,7,9,11], colors=[0]),
        'candidateA_color0': summarize_candidate(candA, [5,7,9,11,13], colors=[0]),
        'candidateA_all_colors_m7': summarize_candidate(candA, [7], colors=[0,1,2,3,4]),
    }
    out_path = Path('/mnt/data/d5_color0_cyclic_template_diagnostics.json')
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()
