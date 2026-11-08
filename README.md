# Tambour antillais porte-clés « Mawonaj » — Anycubic Kobra 3

Projet de fichier STL imprimable en 3D : tambour antillais (gwoka) en porte-clés avec l'inscription **Mawonaj** en relief, écrite en **script (M majuscule)**, crochet **en bas, soudé à la paroi basse du fût** (impression peau vers le haut => définition max, zéro support), inscription **à l'opposé du crochet** (180°, visibilité max), peau bombée avec cerclage et **ficelles de laçage apparentes** descendant du cerclage le long du fût.

## Fichiers du projet

| Fichier | Rôle |
|---|---|
| `gen_tambour.py` | Générateur Python pur (aucune dépendance) |
| `tambour_mawonaj_portecle.stl` | STL final à imprimer (binaire, 57 528 triangles, ~2,88 Mo) — généré par le script |
| `README_impression_Kobra3.md` | Fiche de réglages d'impression Kobra 3 |

## Caractéristiques du modèle (v9)

- Dimensions : **37,8 × 30,2 × 37,5 mm** — un vrai porte-clés, pas un bloc plein
- Volume solide ~20,9 cm³ → environ **8–9 g en PLA à 20 % de remplissage**
- Fût galbé, double bande décorative en bas, deux rangées de chevrons
- **Peau bombée uniforme et nette** (dôme 1,5 mm, 40 anneaux) avec double cerclage métallique
- **8 ficelles de laçage en relief (~0,8 mm de Ø, 0,5 mm de haut)** descendant de la peau en zigzag le long du fût jusqu'à la bande basse, en contournant la zone du texte — style laçage de tambour ka
- **Crochet EN BAS intégré à la paroi du fût** : boucle horizontale soudée **à la base même du fût (z=0, repose sur le plateau)** (Ø trou ~5,8 mm), aucun bras — reposant directement sur le plateau à l'impression : définition optimale, aucune bavure, **aucun support** — **inscription à l'opposé (180°)**
- Inscription **« Mawonaj » en script très épais** (traits ~1,6 mm, relief 1,9 mm, M majuscule, w/n redessinés en courbes, traits sous-échantillonnés (pas de trous aux angles)) — très lisible
- Maillage **étanche** (watertight, 0 arête ouverte)
- **Aucun support nécessaire** : impression à plat, peau vers le haut

## Régénérer le STL

```bash
python3 gen_tambour.py
```

- Inscription : `TEXT = "Mawonaj"` (glyphes script dans `SCRIPT`), taille via `TXT_W` / `TXT_H` / `TXT_RELIEF` / `TXT_HW`
- Ficelles de laçage : `N_LACE`, `LACE_ZIG`, `LACE_AMP`, `LACE_HW_MM`, `LACE_RELIEF`, `LACE_BOW`
- Boucle : `BOUCLE_CX` / `BOUCLE_Z` / `BOUCLE_R` / `BOUCLE_TUBE`

## Impression (Anycubic Kobra 3)

Couches 0,12 mm, 4 parois, gyroid 20 %, aucun support, brim 3–4 mm, PLA 200–210 °C / plateau 60 °C, à plat peau vers le haut. Détails dans `README_impression_Kobra3.md`.
