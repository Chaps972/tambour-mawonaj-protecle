#!/usr/bin/env python3
"""Generateur STL : tambour antillais porte-cle (Anycubic Kobra 3).
Python pur : maillage manuel, STL binaire, validation.
Version 2 : crochet integre au fut, inscription script (M majuscule), plus de details.
"""
import math, struct

# ---------------- Parametres (mm) ----------------
SCALE    = 0.75    # echelle porte-cle (0.75 => ~42 mm de haut)
H        = 48.0 * SCALE    # hauteur du fut
R_BAS    = 16.0 * SCALE    # rayon en bas
R_HAUT   = 15.0 * SCALE    # rayon en haut (sous la peau)
BULGE    = 4.5 * SCALE     # bombe maximal du fut
DOME     = 0.9 * SCALE     # bombe de la peau
N_CORDES = 8
CORDE_AMP = 0.55 * SCALE   # cordons un peu plus marques
NT = 160           # resolution angulaire
NZ = 96            # resolution verticale du fut
N_RING_PEAU = 26

BANDE_BAS  = (1.6, 4.0, 0.75)
BANDE_BAS  = (BANDE_BAS[0]*SCALE, BANDE_BAS[1]*SCALE, BANDE_BAS[2]*SCALE)
BANDE_BAS2 = (0.5, 1.3, 0.45)   # seconde bande basse (plus de details)
BANDE_BAS2 = (BANDE_BAS2[0]*SCALE, BANDE_BAS2[1]*SCALE, BANDE_BAS2[2]*SCALE)
BANDE_HAUT = ((H - 6.0*SCALE), (H - 3.6*SCALE), 0.75*SCALE)
CHEV_Z0, CHEV_Z1, CHEV_AMP, N_CHEV = 0.28*H, 0.42*H, 0.85*SCALE, 8
CHEV2_Z0, CHEV2_Z1, CHEV2_AMP, N_CHEV2 = 0.55*H, 0.72*H, 0.70*SCALE, 8  # 2e rangee de chevrons

TEXT       = "Mawonaj"   # script, M majuscule
TXT_ZBOT   = 0.470 * H
TXT_W      = 0.60 * SCALE
TXT_H      = 0.62 * SCALE
TXT_RELIEF = 1.6 * SCALE
TXT_HW     = 0.55          # demi-largeur des traits (en unites de glyphe)
TXT_ZONE   = (TXT_ZBOT - 2.4*TXT_H - 0.4, TXT_ZBOT + 7.4*TXT_H + 0.4)

TORE_CERC_R    = R_HAUT + 0.55 * SCALE
TORE_CERC_TUBE = 1.25 * SCALE
TORE_CERC_Z    = H + 0.25 * SCALE

# Crochet directement integre a la face du tambour : la boucle (tore horizontal)
# penetre la paroi superieure du fut, aucun bras intermediaire.
BOUCLE_R    = 4.2    # rayon de la boucle
BOUCLE_TUBE = 1.3    # section du tore
BOUCLE_Z    = H - 1.2            # hauteur du centre de la boucle (dans la paroi haute)
BOUCLE_CX   = R_HAUT + 3.55      # deport : le tore mord dans le fut, le trou reste degage

# ---------------- Police script (traits, unites : hauteur 0..7, y vers le haut) ----------------
def _arc(cx, cy, r, a0, a1, n=16):
    return [(cx + r*math.cos(a0 + (a1-a0)*i/n), cy + r*math.sin(a0 + (a1-a0)*i/n)) for i in range(n+1)]

_R = math.radians
SCRIPT = {
 'M': [[(0.0,0.2),(0.15,2.6),(0.5,5.4),(0.95,7.0),(1.5,4.4),(1.9,1.6),(2.3,5.2),(2.75,7.0),(3.25,4.0),(3.65,0.4),(4.4,0.0)]],
 'a': [_arc(1.5,2.6,1.8, _R(75), _R(75)-2*math.pi, 20) + [(3.3,4.5),(3.3,0.3),(3.95,-0.2)]],
 'w': [[(0.0,4.6),(0.8,0.2),(1.6,4.4),(2.4,0.2),(3.2,4.6)]],
 'o': [_arc(1.8,2.6,1.8, _R(90), _R(90)-2*math.pi, 20) + [(1.8,4.4),(2.7,4.7)]],
 'n': [[(0.0,4.6),(0.3,2.2),(0.45,0.2),(1.0,3.4),(1.7,4.6),(2.2,2.2),(2.5,0.2),(3.15,3.8)]],
 'j': [_arc(1.0,6.1,0.45, 0, -2*math.pi, 10),
       [(1.0,4.6),(1.0,0.6),(0.7,-0.8),(-0.1,-1.7),(-0.95,-1.25)]],
}

def _adv(ch):
    g = SCRIPT.get(ch, SCRIPT['o'])
    return max(p[0] for stroke in g for p in stroke) + 1.1

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
    r += bande(z, *BANDE_BAS2)
    r += bande(z, *BANDE_HAUT)
    for (z0, z1, amp, nch, phase) in ((CHEV_Z0, CHEV_Z1, CHEV_AMP, N_CHEV, 0.0),
                                       (CHEV2_Z0, CHEV2_Z1, CHEV2_AMP, N_CHEV2, math.pi / N_CHEV2)):
        if z0 <= z <= z1:
            ph = ((nch * theta / (2 * math.pi)) + phase) % 1.0
            tri = 2 * ph if ph < 0.5 else 2 * (1 - ph)
            lissage = math.sin(math.pi * (z - z0) / (z1 - z0))
            r += amp * tri * lissage
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

def _render_stroke(m, poly, x_off, z_bot, w, h, relief, th0, r_loc):
    """Extrude un trait (polyligne en unites de glyphe) en relief courbe sur le fut."""
    n = len(poly)
    # direction en chaque point (moyenne des segments adjacents)
    dirs = []
    for i in range(n):
        if i == 0:
            dx, dy = poly[1][0]-poly[0][0], poly[1][1]-poly[0][1]
        elif i == n-1:
            dx, dy = poly[n-1][0]-poly[n-2][0], poly[n-1][1]-poly[n-2][1]
        else:
            dx = poly[i+1][0]-poly[i-1][0]; dy = poly[i+1][1]-poly[i-1][1]
        ln = math.hypot(dx, dy) or 1.0
        dirs.append((dx/ln, dy/ln))
    Lin, Lout, Rin, Rout = [], [], [], []
    for i, (px, py) in enumerate(poly):
        dx, dy = dirs[i]
        ox, oy = -dy * TXT_HW, dx * TXT_HW   # perpendiculaire
        for (sx, out) in ((1, 'L'), (-1, 'R')):
            gx = x_off + px + sx*ox
            gy = py + sx*oy
            a = th0 + (gx * w) / r_loc
            z = z_bot + gy * h
            rs = radius(a, z)
            ro = rs + relief
            vi = m.v(rs*math.cos(a), rs*math.sin(a), z)
            vo = m.v(ro*math.cos(a), ro*math.sin(a), z)
            if out == 'L':
                Lin.append(vi); Lout.append(vo)
            else:
                Rin.append(vi); Rout.append(vo)
    for i in range(n-1):
        m.quad(Lout[i], Rout[i], Rout[i+1], Lout[i+1])      # dessus
        m.quad(Lin[i], Lin[i+1], Rin[i+1], Rin[i])          # dessous (sur la peau)
        m.quad(Lin[i], Lout[i], Lout[i+1], Lin[i+1])        # paroi gauche
        m.quad(Rin[i], Rin[i+1], Rout[i+1], Rout[i])        # paroi droite
    m.quad(Lin[0], Lout[0], Rout[0], Rin[0])                # cap debut
    m.quad(Lin[n-1], Lout[n-1], Rout[n-1], Rin[n-1])        # cap fin

def add_texte(m, text, z_bot, w, h, relief):
    r_loc = radius(0.0, z_bot + 3.5 * h)
    total_units = sum(_adv(ch) for ch in text)
    th0 = -(total_units * w / 2) / r_loc
    x_off = 0.0
    for ch in text:
        for poly in SCRIPT.get(ch, SCRIPT['o']):
            _render_stroke(m, poly, x_off, z_bot, w, h, relief, th0, r_loc)
        x_off += _adv(ch)

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
    # --- crochet integre directement a la face du tambour : boucle seule, ---
    # --- le tore penetre la paroi haute du fut (pas de bras) ---
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
