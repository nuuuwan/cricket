from cricket.core import ODI

odis = ODI.load_list()
country_to_n = {}
country_to_neutral_n = {}
for odi in odis:
    country = odi.country
    if country is None:
        continue
    country_to_n[country] = country_to_n.get(country, 0) + 1

    if odi.is_neutral:
        country_to_neutral_n[country] = (
            country_to_neutral_n.get(country, 0) + 1
        )

        if country == 'India':
            print(odi)

for country, n in sorted(country_to_n.items(), key=lambda x: x[1]):
    n_neutral = country_to_neutral_n.get(country, 0)
    print(f"{n} {n_neutral} {country}")
