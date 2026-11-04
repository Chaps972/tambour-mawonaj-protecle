# Tambour antillais porte-clés « Mawonaj » — Anycubic Kobra 3

Projet de fichier STL imprimable en 3D : tambour antillais (gwoka) en porte-clés avec l'inscription **Mawonaj** en relief, écrite en **script (M majuscule)**, crochet **directement intégré à la face du tambour**, inscription **à l'opposé du crochet** (visibilité max), peau bombée avec cerclage et **ficelles de laçage apparentes** descendant du cerclage le long du fût.

## Fichiers du projet

| Fichier | Rôle |
|---|---|
| `gen_tambour.py` | Générateur Python pur (aucune dépendance) |
| `tambour_mawonaj_portecle.stl` | STL final à imprimer (binaire, 57 528 triangles, ~2,88 Mo) — généré par le script |
| `README_impression_Kobra3.md` | Fiche de réglages d'impression Kobra 3 |

## Caractéristiques du modèle (v6)

- Dimensions : **36,1 × 30,0 × 37,3 mm** — un vrai porte-clés, pas un bloc plein
- Volume solide ~20,9 cm³ → environ **8–9 g en PLA à 20 % de remplissage**
- Fût galbé, double bande décorative en bas, deux rangées de chevrons
- **Peau bombée uniforme** (dôme régulier) avec double cerclage métallique
- **8 ficelles de laçage en relief (~0,8 mm de Ø, 0,5 mm de haut)** descendant de la peau en zigzag le long du fût jusqu'à la bande basse, en contournant la zone du texte — style laçage de tambour ka
- **Crochet intégré à la face** : boucle soudée dans la paroi haute du fût (Ø trou ~5,8 mm), aucun bras — **l'inscription est à l'opposé (180°), bien dégagée du crochet**
- Inscription **« Mawonaj » en script épais** (traits ~0,9 mm, relief 1,35 mm, M majuscule)
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
