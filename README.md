# Tambour antillais porte-clés « Mawonaj » — Anycubic Kobra 3

Projet de fichier STL imprimable en 3D : tambour antillais (gwoka) en porte-clés avec l'inscription **Mawonaj** en relief, écrite en **script (M majuscule)**, courbée sur le fût, et crochet porte-clés **intégré au fût**.

## Fichiers du projet

| Fichier | Rôle |
|---|---|
| `gen_tambour.py` | Générateur Python pur (aucune dépendance) |
| `tambour_mawonaj_portecle.stl` | STL final à imprimer (binaire, 47 604 triangles, ~2,38 Mo) — généré par le script |
| `README_impression_Kobra3.md` | Fiche de réglages d'impression Kobra 3 |

## Caractéristiques du modèle (v2)

- Dimensions : **35,7 × 29,6 × 43,2 mm** — un vrai porte-clés, pas un bloc plein
- Volume solide ~20,5 cm³ → environ **8–9 g en PLA à 20 % de remplissage**
- Fût galbé, 8 cordons de tension ondulés, **double bande décorative en bas**, **deux rangées de chevrons**, peau bombée, cerclage métallique
- **Crochet intégré** : bras épais (5,6 mm) ancré dans le fût (pénètre la paroi de 3 mm), aminci vers la boucle porte-clés horizontale (Ø ~9,6 mm, passage mousqueton standard)
- Inscription **« Mawonaj » en script** (traits cursifs, M majuscule) en relief 1,2 mm épousant la courbure du fût
- Maillage **étanche** (watertight, 0 arête ouverte)
- **Aucun support nécessaire** : impression à plat, peau vers le haut, boucle horizontale

## Régénérer le STL

```bash
python3 gen_tambour.py
```

Pour changer l'inscription, modifier `TEXT = "Mawonaj"` dans `gen_tambour.py` (les glyphes script sont dans le dictionnaire `SCRIPT`).

## Impression (Anycubic Kobra 3)

Couches 0,12 mm, 4 parois, gyroid 20 %, aucun support, brim 3–4 mm, PLA 200–210 °C / plateau 60 °C, à plat peau vers le haut. Détails dans `README_impression_Kobra3.md`.
