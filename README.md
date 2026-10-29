# Tambour antillais porte-clés « MAWONAJ » — Anycubic Kobra 3

Projet de fichier STL imprimable en 3D : tambour antillais (gwoka) en porte-clés avec l'inscription **MAWONAJ** en relief courbe sur le fût et anneau porte-clés intégré.

## Fichiers du projet

| Fichier | Rôle |
|---|---|
| `gen_tambour.py` | Générateur Python pur (aucune dépendance) |
| `tambour_mawonaj_portecle.stl` | STL final à imprimer (binaire, 47 288 triangles, ~2,36 Mo) — généré par le script |
| `README_impression_Kobra3.md` | Fiche de réglages d'impression Kobra 3 |

## Caractéristiques du modèle

- Dimensions : **35,6 × 29,6 × 43,2 mm** — un vrai porte-clés, pas un bloc plein
- Volume solide ~20,5 cm³ → environ **8–9 g en PLA à 20 % de remplissage**
- Fût galbé, 8 cordes de tension, bandes et chevrons décoratifs, peau bombée, cerclage métallique, boucle porte-clés horizontale
- Inscription **MAWONAJ** en relief 1,2 mm épousant la courbure du fût (vérifiée lettre par lettre dans le maillage)
- Maillage **étanche** (watertight, 0 arête ouverte)
- **Aucun support nécessaire** : impression à plat, peau vers le haut

## Régénérer le STL

```bash
python3 gen_tambour.py
```

Pour changer l'inscription, modifier `TEXT = "MAWONAJ"` dans `gen_tambour.py`.

## Impression (Anycubic Kobra 3)

Couches 0,12 mm, 4 parois, gyroid 20 %, aucun support, brim 3–4 mm, PLA 200–210 °C / plateau 60 °C, à plat peau vers le haut. Détails dans `README_impression_Kobra3.md`.
