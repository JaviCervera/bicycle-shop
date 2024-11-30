# bicycle-shop

To run the tests, do:

```shell
python -m unittest
```

(In some systems, the executable might be `python3` instead of `python`).

## Data model

```
# 1, Bycicles
product:
- id
- description

# 1, 1, BMX, http://cdn...
product_model:
- id
- product_id
- description
- image url

# 1, 1, Frame type
# 2, 1, Frame finish
# 3, 1, Wheels
# 4, 1, Rim color
# 5, 1, Chain
product_part:
- id
- product_id
- description

# 1, 1, Full-suspension, 130
# 2, 1, Diamond, 100
# 3, 1, Step-through, 90
# 4, 2, Matte, 50
# 5, 2, Shiny, 30
# 6, 3, Road wheels, 80
# 7, 3, Mountain wheels, 90
# 8, 3, Fat bike wheels, 100
# 9, 4, Red, 20
# 10, 4, Black, 25
# 11, 4, Blue, 20
# 12, 5, Single-speed chain, 43
# 13, 5, 8-speed chain, 90
part_option:
- id
- part_id
- description
- price

# 2, 7
# 3, 7
# 8, 9
option_incompatibility:
- option_id
- incompatible_option_id

# 2, 4, 0.7
option_price_modifier:
- option_id
- dependent_option_id
- coef
```
