#!/usr/bin/env python3
"""Generateur STL : tambour antillais porte-cle (Anycubic Kobra 3).
Python pur : maillage manuel, STL binaire, validation, rendu PNG.
"""
import math, struct, zlib

# ---------------- Parametres (mm) ----------------
SCALE    = 0.75    # echelle porte-cle (0.75 => ~42 mm de haut)
H        = 48.0 * SCALE    # hauteur du fut
R_BAS    = 16.0 * SCALE    # rayon en bas
R_HAUT   = 15.0 * SCALE    # rayon en haut (sous la peau)
BULGE    = 4.5 * SCALE     # bombe maximal du fut
DOME     = 0.9 * SCALE     # bombe de la peau
N_CORDES = 8
CORDE_AMP = 0.45 * SCALE
NT = 160           # resolution angulaire
NZ = 96            # resolution verticale du fut
N_RING_PEAU = 26

BANDE_BAS  = (1.6, 4.0, 0.75)
BANDE_BAS  = (BANDE_BAS[0]*SCALE, BANDE_BAS[1]*SCALE, BANDE_BAS[2]*SCALE)
BANDE_HAUT = ((H - 6.0*SCALE), (H - 3.6*SCALE), 0.75*SCALE)
CHEV_Z0, CHEV_Z1, CHEV_AMP, N_CHEV = 0.28*H, 0.42*H, 0.85*SCALE, 8

TEXT       = "MAWONAJ"
TXT_ZBOT   = 0.478 * H
TXT_W      = 0.60 * SCALE
TXT_H      = 0.62 * SCALE
TXT_RELIEF = 1.6 * SCALE
TXT_ZONE   = (TXT_ZBOT - 1.5 * SCALE, TXT_ZBOT + 7 * TXT_H + 1.5 * SCALE)

TORE_CERC_R    = R_HAUT + 0.55 * SCALE
TORE_CERC_TUBE = 1.25 * SCALE
TORE_CERC_Z    = H + 0.25 * SCALE

BOUCLE_R    = 3.6
BOUCLE_TUBE = 1.2
BOUCLE_DX   = 1.2
BOUCLE_Z = H + 0.9 + 1.5 + BOUCLE_R
BOUCLE_CX = R_HAUT + BOUCLE_DX + BOUCLE_R

FONT = {
 'A': ["01110","10001","10001","11111","10001","10001","10001"],
 'B': ["11110","10001","10001","11110","10001","10001","11110"],
 'C': ["01111","10000","10000","10000","10000","10000","01111"],
 'D': ["11110","10001","10001","10001","10001","10001","11110"],
 'E': ["11111","10000","10000","11110","10000","10000","11111"],
 'F': ["11111","10000","10000","11110","10000","10000","10000"],
 'G': ["01111","10000","10000","10111","10001","10001","01111"],
 'H': ["10001","10001","10001","11111","10001","10001","10001"],
 'I': ["11111","00100","00100","00100","00100","00100","11111"],
 'J': ["00111","00010","00010","00010","00010","10010","01100"],
 'K': ["10001","10010","10100","11000","10100","10010","10001"],
 'L': ["10000","10000","10000","10000","10000","10000","11111"],
 'M': ["10001","11011","10101","10101","10001","10001","10001"],
 'N': ["10001","11001","10101","10011","10001","10001","10001"],
 'O': ["01110","10001","10001","10001","10001","10001","01110"],
 'P': ["11110","10001","10001","11110","10000","10000","10000"],
 'Q': ["01110","10001","10001","10001","10101","10010","01101"],
 'R': ["11110","10001","10001","11110","10100","10010","10001"],
 'S': ["01111","10000","10000","01110","00001","00001","11110"],
 'T': ["11111","00100","00100","00100","00100","00100","00100"],
 'U': ["10001","10001","10001","10001","10001","10001","01110"],
 'V': ["10001","10001","10001","10001","10001","01010","00100"],
 'W': ["10001","10001","10001","10101","10101","11011","10001"],
 'X': ["10001","10001","01010","00100","01010","10001","10001"],
 'Y': ["10001","10001","01010","00100","00100","00100","00100"],
 'Z': ["11111","00001","00010","00100","01000","10000","11111"],
 ' ': ["00000","00000","00000","00000","00000","00000","00000"],
 '-': ["00000","00000","00000","11111","00000","00000","00000"],
}

def bande(z, z0, z1, h, ramp=0.8):
    if z < z0 - ramp or z > z1 + ramp:
        return 0.0
    if z < z0:
        return h * (z - (z0 - ramp)) / ramp
    if z > z1:
        return h * ((z1 + ramp) - z) / ramp
    return h

def radius(theta, z):
    t = z / H
    r = R_BAS + (R_HAUT - R_BAS) * t + BULGE * math.sin(math.pi * t) ** 1.5 * (1 - 0.35 * t)
    att = math.sin(math.pi * t) ** 2
    cf = 0.10 if (TXT_ZONE[0] <= z <= TXT_ZONE[1]) else 1.0
    r += CORDE_AMP * att * cf * math.cos(N_CORDES * theta)
    r += bande(z, *BANDE_BAS)
    r += bande(z, *BANDE_HAUT)
    if CHEV_Z0 <= z <= CHEV_Z1:
        ph = (N_CHEV * theta / (2 * math.pi)) % 1.0
        tri = 2 * ph if ph < 0.5 else 2 * (1 - ph)
        lissage = math.sin(math.pi * (z - CHEV_Z0) / (CHEV_Z1 - CHEV_Z0))
        r += CHEV_AMP * tri * lissage
    return r

def peau_z(r):
    return H + DOME * (1 - (r / R_HAUT) ** 2) ** 0.65

class Mesh:
    def __init__(self):
        self.verts = []
        self.tris = []
        self._cache = {}
    def v(self, x, y, z):
        key = (round(x, 5), round(y, 5), round(z, 5))
        idx = self._cache.get(key)
        if idx is None:
            idx = len(self.verts)
            self.verts.append((x, y, z))
            self._cache[key] = idx
        return idx
    def tri(self, a, b, c):
        self.tris.append((a, b, c))
    def quad(self, a, b, c, d):
        self.tris.append((a, b, c))
        self.tris.append((a, c, d))

def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

def add_tore(mesh, zc, R, tube, n_phi=30, n_psi=72, cx=0.0):
    g = [[0]*n_psi for _ in range(n_phi)]
    for a in range(n_phi):
        phi = 2 * math.pi * a / n_phi
        for b in range(n_psi):
            psi = 2 * math.pi * b / n_psi
            rr = R + tube * math.cos(phi)
            g[a][b] = mesh.v(cx + rr*math.cos(psi), rr*math.sin(psi), zc + tube*math.sin(phi))
    for a in range(n_phi):
        a2 = (a+1) % n_phi
        for b in range(n_psi):
            b2 = (b+1) % n_psi
            mesh.quad(g[a][b], g[a][b2], g[a2][b2], g[a2][b])

def add_cylindre(mesh, r, z0, z1, n=28):
    bas  = [mesh.v(r*math.cos(2*math.pi*i/n), r*math.sin(2*math.pi*i/n), z0) for i in range(n)]
    haut = [mesh.v(r*math.cos(2*math.pi*i/n), r*math.sin(2*math.pi*i/n), z1) for i in range(n)]
    cb = mesh.v(0, 0, z0); ch = mesh.v(0, 0, z1)
    for i in range(n):
        i2 = (i+1) % n
        mesh.quad(bas[i], bas[i2], haut[i2], haut[i])
        mesh.tri(cb, bas[i2], bas[i])
        mesh.tri(ch, haut[i], haut[i2])

def add_texte(m, text, z_bot, w, h, relief):
    cols_per = 6
    total_w = len(text) * cols_per * w
    z_top = z_bot + 7 * h
    r_loc = radius(0.0, z_bot + 3.5 * h)
    th0 = -(total_w / 2) / r_loc
    for li, ch in enumerate(text):
        glyph = FONT.get(ch, FONT[' '])
        rects = []
        used = [[False] * 5 for _ in range(7)]
        for col in range(5):
            row = 0
            while row < 7:
                if glyph[row][col] == '1' and not used[row][col]:
                    r2 = row
                    while r2 + 1 < 7 and glyph[r2 + 1][col] == '1' and not used[r2 + 1][col]:
                        r2 += 1
                    rects.append((col, row, col, r2))
                    for rr in range(row, r2 + 1):
                        used[rr][col] = True
                    row = r2 + 1
                else:
                    row += 1
        merged = []
        taken = set()
        for (c1, r1, c2, r2) in sorted(rects, key=lambda t: (t[1], t[3], t[0])):
            if (c1, r1, c2, r2) in taken:
                continue
            cc = c1
            while cc + 1 <= 4:
                ok = True
                for rr in range(r1, r2 + 1):
                    if glyph[rr][cc + 1] != '1':
                        ok = False
                        break
                if ok:
                    same = True
                    for rr in range(7):
                        if glyph[rr][cc + 1] == '1' and not (r1 <= rr <= r2):
                            same = False
                            break
                    if not same:
                        ok = False
                if not ok:
                    break
                cc += 1
            for c in range(c1, cc + 1):
                for rr in range(r1, r2 + 1):
                    taken.add((c, rr))
            merged.append((c1, r1, cc, r2))
        for (c1, r1, c2, r2) in merged:
            x0 = li * cols_per + c1
            x1 = li * cols_per + c2 + 1
            a1 = th0 + (x0 * w - 0.08 * w) / r_loc
            a2 = th0 + (x1 * w + 0.08 * w) / r_loc
            zz1 = z_top - (r2 + 1) * h - 0.08 * h
            zz2 = z_top - r1 * h + 0.08 * h
            rb = radius(0.0, zz1) + relief
            rt = radius(0.0, zz2) + relief
            Ain  = m.v(radius(a1, zz1)*math.cos(a1), radius(a1, zz1)*math.sin(a1), zz1)
            Bin  = m.v(radius(a2, zz1)*math.cos(a2), radius(a2, zz1)*math.sin(a2), zz1)
            Cin  = m.v(radius(a2, zz2)*math.cos(a2), radius(a2, zz2)*math.sin(a2), zz2)
            Din  = m.v(radius(a1, zz2)*math.cos(a1), radius(a1, zz2)*math.sin(a1), zz2)
            Aout = m.v(rb*math.cos(a1), rb*math.sin(a1), zz1)
            Bout = m.v(rb*math.cos(a2), rb*math.sin(a2), zz1)
            Cout = m.v(rt*math.cos(a2), rt*math.sin(a2), zz2)
            Dout = m.v(rt*math.cos(a1), rt*math.sin(a1), zz2)
            m.quad(Aout, Bout, Cout, Dout)
            m.quad(Ain, Din, Cin, Bin)
            m.quad(Ain, Bin, Bout, Aout)
            m.quad(Din, Dout, Cout, Cin)
            m.quad(Ain, Aout, Dout, Din)
            m.quad(Bin, Cin, Cout, Bout)

def build():
    m = Mesh()
    grid = [[0]*NT for _ in range(NZ)]
    for j in range(NZ):
        z = H * j / (NZ - 1)
        for i in range(NT):
            th = 2 * math.pi * i / NT
            r = radius(th, z)
            grid[j][i] = m.v(r*math.cos(th), r*math.sin(th), z)
    for j in range(NZ - 1):
        for i in range(NT):
            i2 = (i+1) % NT
            m.quad(grid[j][i], grid[j][i2], grid[j+1][i2], grid[j+1][i])
    c0 = m.v(0, 0, 0)
    for i in range(NT):
        i2 = (i+1) % NT
        m.tri(c0, grid[0][i2], grid[0][i])
    cc = m.v(0, 0, peau_z(0))
    rings = []
    for k in range(1, N_RING_PEAU + 1):
        rk = R_HAUT * k / N_RING_PEAU
        rings.append([m.v(rk*math.cos(2*math.pi*i/NT), rk*math.sin(2*math.pi*i/NT), peau_z(rk)) for i in range(NT)])
    for i in range(NT):
        i2 = (i+1) % NT
        m.tri(rings[0][i], rings[0][i2], cc)
    for k in range(N_RING_PEAU - 1):
        for i in range(NT):
            i2 = (i+1) % NT
            a, b, c, d = rings[k][i], rings[k+1][i], rings[k+1][i2], rings[k][i2]
            m.quad(a, b, c, d)
    add_tore(m, TORE_CERC_Z, TORE_CERC_R, TORE_CERC_TUBE, 24, 96)
    x_in, x_out = R_HAUT - 1.0, BOUCLE_CX - BOUCLE_R + BOUCLE_TUBE - 0.2
    yc0, yc1 = -2.0, 2.0
    zb, zt = H - 0.6, BOUCLE_Z + 0.7
    p1 = m.v(x_in, yc0, zb); p2 = m.v(x_out, yc0, zb)
    p3 = m.v(x_out, yc1, zb); p4 = m.v(x_in, yc1, zb)
    p5 = m.v(x_in, yc0, zt); p6 = m.v(x_out, yc0, zt)
    p7 = m.v(x_out, yc1, zt); p8 = m.v(x_in, yc1, zt)
    m.quad(p1, p2, p3, p4)
    m.quad(p5, p8, p7, p6)
    m.quad(p1, p4, p8, p5)
    m.quad(p2, p6, p7, p3)
    m.quad(p1, p5, p6, p2)
    m.quad(p4, p3, p7, p8)
    add_tore(m, BOUCLE_Z, BOUCLE_R, BOUCLE_TUBE, 26, 64, cx=BOUCLE_CX)
    add_cylindre(m, 2.6, H - 0.8, H + 0.15, n=20)
    add_texte(m, TEXT, TXT_ZBOT, TXT_W, TXT_H, TXT_RELIEF)
    return m

def write_stl(path, m):
    with open(path, 'wb') as f:
        f.write(b'\x00' * 80)
        f.write(struct.pack('<I', len(m.tris)))
        for (a, b, c) in m.tris:
            va, vb, vc = m.verts[a], m.verts[b], m.verts[c]
            n = cross(sub(vb, va), sub(vc, va))
            ln = math.sqrt(dot(n, n)) or 1.0
            n = (n[0]/ln, n[1]/ln, n[2]/ln)
            f.write(struct.pack('<12fH', n[0], n[1], n[2], va[0], va[1], va[2],
                                vb[0], vb[1], vb[2], vc[0], vc[1], vc[2], 0))

def validate(m):
    edges = {}
    for (a, b, c) in m.tris:
        for e in ((a,b),(b,c),(c,a)):
            key = (min(e), max(e))
            edges[key] = edges.get(key, 0) + 1
    bad = sum(1 for v in edges.values() if v != 2)
    vol = 0.0
    for (a, b, c) in m.tris:
        vol += dot(m.verts[a], cross(m.verts[b], m.verts[c])) / 6.0
    xs = [v[0] for v in m.verts]; ys = [v[1] for v in m.verts]; zs = [v[2] for v in m.verts]
    parent = list(range(len(m.verts)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for (a, b, c) in m.tris:
        for u, v in ((a,b),(b,c),(c,a)):
            ru, rv = find(u), find(v)
            if ru != rv: parent[ru] = rv
    comp = {}
    for (a, b, c) in m.tris:
        comp.setdefault(find(a), [0, 0])
        comp[find(a)][0] += 1
    comp_edges = {}
    for (a, b, c) in m.tris:
        r = find(a)
        for e in ((a,b),(b,c),(c,a)):
            key = (r, min(e), max(e))
            comp_edges[key] = comp_edges.get(key, 0) + 1
    open_shells = 0
    for r in comp:
        cnt = {}
        for (rr, e1, e2), v in comp_edges.items():
            if rr == r:
                cnt[(e1, e2)] = v
        if any(v != 2 for v in cnt.values()):
            open_shells += 1
    print(f"triangles        : {len(m.tris)}")
    print(f"vertices         : {len(m.verts)}")
    print(f"aretess non fermees (global) : {bad}")
    print(f"composantes (shells)         : {len(comp)}  (ouverts: {open_shells})")
    print(f"volume signe total : {vol:,.1f} mm^3")
    print(f"dimensions       : {max(xs)-min(xs):.2f} x {max(ys)-min(ys):.2f} x {max(zs)-min(zs):.2f} mm")
    return bad == 0 and open_shells == 0

if __name__ == '__main__':
    m = build()
    ok = validate(m)
    write_stl('tambour_mawonaj_portecle.stl', m)
    print("STL : tambour_mawonaj_portecle.stl")
    print("maillage ferme (watertight) :", "OUI" if ok else "NON")
