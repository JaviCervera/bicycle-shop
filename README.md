# bicycle-shop

To run the tests, do:

```shell
python -m unittest
```

(In some systems, the executable might be `python3` instead of `python`).

## Problem description

You're tasked with building a website that allows Marcus, a bicycle shop owner, to sell his bicycles.

Marcus owns a growing business and now wants to sell online. He also tells you that bicycles are his main product, but if the business continues to grow, he will surely start selling other sports-related items such as skis, surfboards, roller skates, etc. It would be a nice bonus if the same website allowed him to sell those things as well [1].

What makes Marcus's business successful is that customers can fully customize their bicycles. They can select many different options for the various parts of the bicycle [2]. Here is an incomplete list of all the parts and their possible choices, to give an example:

* Frame type: Full-suspension, diamond, step-through
* Frame finish: Matte, shiny
* Wheels: Road wheels, mountain wheels, fat bike wheels
* Rim color: Red, black, blue
* Chain: Single-speed chain, 8-speed chain

On top of that, Marcus points out that some combinations are prohibited because they are not possible in reality [3]. For example:

* If you select "mountain wheels," then the only frame available is the full-suspension.
* If you select "fat bike wheels," then the red rim color is unavailable because the manufacturer doesn't provide it.

Additionally, Marcus sometimes doesn't have all possible variations of each part in stock, so he wants to be able to mark them as "temporarily out of stock" to avoid receiving orders he can't fulfill [4].

Finally, Marcus explains how to calculate the price that you should present to the customer after customizing a bicycle. Normally, this price is calculated by adding up the individual prices of each selected part [5]. For example:

* Full suspension = 130 EUR
* Shiny frame = 30 EUR
* Road wheels = 80 EUR
* Rim color blue = 20 EUR
* Chain: Single-speed chain = 43 EUR
* Total price: 130 + 30 + 80 + 20 + 43 = 303 EUR

However, the price of some options might depend on others. For instance, the frame finish is applied over the whole bicycle, so the more area to cover, the more expensive it gets. Because of that, the matte finish over a full-suspension frame costs 50 EUR, while applied over a diamond frame it costs 35 EUR [6].

These kinds of variations can always happen, and they might depend on any of the other choices, so Marcus asks you to consider this, as otherwise, he would be losing money.

## Requirements

1. The store must be able to sell different kinds of products.
2. Each product is divided in different parts that the client can customize by choosing from several options for each part.
3. The option selected for a part might be incompatible with other options of any parts.
4. You can't select options which are out of stock.
5. The price of a product is calculated by adding up the individual prices of each selected part.
6. The price of the options in some parts might depend on which options were selected for other parts.

## Data model

```
# 1, Bycicles
product:
- id
- description

# 1, 1, Frame type
# 2, 1, Frame finish
# 3, 1, Wheels
# 4, 1, Rim color
# 5, 1, Chain
product_part:
- id
- product_id
- description

# 1, 1, Full-suspension, 130, True
# 2, 1, Diamond, 100, True
# 3, 1, Step-through, 90, True
# 4, 2, Matte, 50, True
# 5, 2, Shiny, 30, True
# 6, 3, Road wheels, 80, True
# 7, 3, Mountain wheels, 90, True
# 8, 3, Fat bike wheels, 100, True
# 9, 4, Red, 20, True
# 10, 4, Black, 25, True
# 11, 4, Blue, 20, True
# 12, 5, Single-speed chain, 43, True
# 13, 5, 8-speed chain, 90, False
part_option:
- id
- part_id
- description
- price
- in_stock

# 2, 7
# 3, 7
# 8, 9
option_incompatibility:
- option_id
- incompatible_option_id

# 2, 4, 0.7
# Any items in part_id will get their price modified by coef if
# depending_option_id is selected (which itself might belong to a different
# part_id)
option_price_modifier:
- part_id
- depending_option_id
- coef
```

## Requirements conformance

1. The store must be able to sell different kinds of products.
This requirement is satisfied by providing a `ProductRepository` that can
return an arbitrary number of `Product`s.

2. Each product is divided in different parts that the client can customize by choosing from several options for each part.
`ProductPartRepository` can return the list of parts available for a specific `Product`. `PartOptionRepository` can returns the options available for a given `ProductPart`.

3. The option selected for a part might be incompatible with other options of any parts.
`PartOptionRepository` can provide a list of `PartOption`s which are incompatible with another one.

`PartOptionFilter.compatible` returns the options available for a part based on other options selected.

4. You can't select options which are out of stock.
`PartOption` has an `in_stock` property that indicates this. This is enough as the purchase functionality is not added to this exercise. In that case, the class would instead hold a `units_available` options. An option would be in stock if its value is > 0, and would decrease with each order purchased that contains the option.

`PartOptionFilter.in_stock` returns which of the given options are in stock.

5. The price of a product is calculated by adding up the individual prices of each selected part.

`PriceCalculator` computes the total price from a list of parts.

6. The price of the options in some parts might depend on which options were selected for other parts.

`PriceCalculator` takes into account if a selected option modifies other options in the list.
