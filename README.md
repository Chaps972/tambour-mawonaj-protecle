# Tambour antillais porte-clés « Mawonaj » — Anycubic Kobra 3

Projet de fichier STL imprimable en 3D : tambour antillais (gwoka) en porte-clés avec l'inscription **Mawonaj** en relief, écrite en **script (M majuscule)**, courbée sur le fût, crochet **directement intégré à la face du tambour**, peau bombée avec cerclage et **8 tendeurs de peau**.

## Fichiers du projet

| Fichier | Rôle |
|---|---|
| `gen_tambour.py` | Générateur Python pur (aucune dépendance) |
| `tambour_mawonaj_portecle.stl` | STL final à imprimer (binaire, 56 920 triangles, ~2,85 Mo) — généré par le script |
| `README_impression_Kobra3.md` | Fiche de réglages d'impression Kobra 3 |

## Caractéristiques du modèle (v4)

- Dimensions : **35,0 × 29,3 × 39,5 mm** — un vrai porte-clés, pas un bloc plein
- Volume solide ~20,9 cm³ → environ **8–9 g en PLA à 20 % de remplissage**
- Fût galbé, 8 cordons de tension ondulés, double bande décorative en bas, deux rangées de chevrons
- **Peau bombée uniforme** (dôme régulier) avec double cerclage métallique et **8 tendeurs de peau coniques** inclinés à 35° autour du haut (imprimables sans support)
- **Crochet intégré à la face** : boucle soudée dans la paroi haute du fût (Ø trou ~5,8 mm), aucun bras
- Inscription **« Mawonaj » en script épais** (traits ~0,9 mm, relief 1,35 mm, M majuscule) — bien lisible à l'impression
- Maillage **étanche** (watertight, 0 arête ouverte)
- **Aucun support nécessaire** : impression à plat, peau vers le haut

## Régénérer le STL

```bash
python3 gen_tambour.py
```

- Inscription : `TEXT = "Mawonaj"` (glyphes script dans `SCRIPT`), taille via `TXT_W` / `TXT_H` / `TXT_RELIEF` / `TXT_HW`
- Boucle : `BOUCLE_CX` / `BOUCLE_Z` / `BOUCLE_R` / `BOUCLE_TUBE`
- Tendeurs : `N_TEND`, `TEND_LEN`, `TEND_TILT`, etc.

## Impression (Anycubic Kobra 3)

Couches 0,12 mm, 4 parois, gyroid 20 %, aucun support, brim 3–4 mm, PLA 200–210 °C / plateau 60 °C, à plat peau vers le haut. Détails dans `README_impression_Kobra3.md`.
