# pets-and-house-rules · level 1

**Version:** raw+80623eb · **Release:** raw · This file holds level 1, the core of the domain.

Explain what it takes to own a dog or a cat in a residential complex, and which house rules apply to pets and their owners.

This is the raw release: it also holds elements that are not approved yet. They are marked
`● proposed` or `◐ waiting for approval`, and drawn dashed in the diagrams.

## Taxonomy

```mermaid
flowchart TB
    classDef draft stroke-dasharray: 5 5
    cn_01M82AQDR2NPZDR8C737517K86["cat"]
    cn_01M82AQDR2NPZDR8C737517K87["cat owner"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYT["compost"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM["dog"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKV["dog registration"]
    cn_01M82AH1GXVV72WP99JQXMH6XS["dog waste"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW6["leash"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKS["local authority"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKT["microchip"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8["owner"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYR["residual waste"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYS["toilet"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYQ["used litter"]
    cn_01M82AH1GXVV72WP99JQXMH6XT["waste bin"]
    class cn_01M82AQDR2NPZDR8C737517K86,cn_01M82AQDR2NPZDR8C737517K87,cn_01M82ATVV0G4J5RJ6TZ063RNYT,cn_01M82AC66KMJH32E2MQ3Z7ZBKM,cn_01M82AC66KMJH32E2MQ3Z7ZBKV,cn_01M82AH1GXVV72WP99JQXMH6XS,cn_01M82AFTZDSHCD0SK6T4N2YZW6,cn_01M82AC66KMJH32E2MQ3Z7ZBKS,cn_01M82AC66KMJH32E2MQ3Z7ZBKT,cn_01M82AE56ZYS5Y2Z0C35ECC9Y8,cn_01M82ATVV0G4J5RJ6TZ063RNYR,cn_01M82ATVV0G4J5RJ6TZ063RNYS,cn_01M82ATVV0G4J5RJ6TZ063RNYQ,cn_01M82AH1GXVV72WP99JQXMH6XT draft
```

## Concepts and relations

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AQDR2NPZDR8C737517K86["cat"]
    cn_01M82AQDR2NPZDR8C737517K87["cat owner"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYT["compost"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM["dog"]
    cn_01M82AH1GXVV72WP99JQXMH6XS["dog waste"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW6["leash"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKS["local authority"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKT["microchip"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8["owner"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYR["residual waste"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYS["toilet"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYQ["used litter"]
    cn_01M82AH1GXVV72WP99JQXMH6XT["waste bin"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "is registered with" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKS
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "carries" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKT
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "is kept on" .-> cn_01M82AFTZDSHCD0SK6T4N2YZW6
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8 -. "picks up" .-> cn_01M82AH1GXVV72WP99JQXMH6XS
    cn_01M82AH1GXVV72WP99JQXMH6XS -. "is put in" .-> cn_01M82AH1GXVV72WP99JQXMH6XT
    cn_01M82AQDR2NPZDR8C737517K87 -. "owns" .-> cn_01M82AQDR2NPZDR8C737517K86
    cn_01M82ATVV0G4J5RJ6TZ063RNYQ -. "goes into" .-> cn_01M82ATVV0G4J5RJ6TZ063RNYR
    cn_01M82ATVV0G4J5RJ6TZ063RNYQ -. "never goes into" .-> cn_01M82ATVV0G4J5RJ6TZ063RNYS
    cn_01M82ATVV0G4J5RJ6TZ063RNYQ -. "never goes into" .-> cn_01M82ATVV0G4J5RJ6TZ063RNYT
    class cn_01M82AQDR2NPZDR8C737517K86,cn_01M82AQDR2NPZDR8C737517K87,cn_01M82ATVV0G4J5RJ6TZ063RNYT,cn_01M82AC66KMJH32E2MQ3Z7ZBKM,cn_01M82AH1GXVV72WP99JQXMH6XS,cn_01M82AFTZDSHCD0SK6T4N2YZW6,cn_01M82AC66KMJH32E2MQ3Z7ZBKS,cn_01M82AC66KMJH32E2MQ3Z7ZBKT,cn_01M82AE56ZYS5Y2Z0C35ECC9Y8,cn_01M82ATVV0G4J5RJ6TZ063RNYR,cn_01M82ATVV0G4J5RJ6TZ063RNYS,cn_01M82ATVV0G4J5RJ6TZ063RNYQ,cn_01M82AH1GXVV72WP99JQXMH6XT draft
```

## Concepts

<a id="cn_01M82AQDR2NPZDR8C737517K86"></a>
### cat · ● proposed

- **Level:** 1
- **Evidence:** [§1](#su_01M82APMQ68JDJRTYQDVNXFWWJ), [§5](#su_01M82APMQ68JDJRTYQDVNXFWWM), [§9](#su_01M82APMQ7MGEVFK2CW6002H2P), [§10](#su_01M82APMQ7MGEVFK2CW6002H2R), [§11](#su_01M82APMQ7MGEVFK2CW6002H2T), [§12](#su_01M82APMQ7MGEVFK2CW6002H2W), [§14](#su_01M82APMQ7MGEVFK2CW6002H2Y), [§20](#su_01M82APMQ7MGEVFK2CW6002H30), [§21](#su_01M82APMQ7MGEVFK2CW6002H32), [§24](#su_01M82APMQ7MGEVFK2CW6002H34), [§27](#su_01M82APMQ7MGEVFK2CW6002H36)

<a id="cn_01M82AQDR2NPZDR8C737517K87"></a>
### cat owner · ● proposed

- **Level:** 1
- **Evidence:** [§1](#su_01M82APMQ68JDJRTYQDVNXFWWJ)

<a id="cn_01M82ATVV0G4J5RJ6TZ063RNYT"></a>
### compost · ● proposed

- **Level:** 1
- **Evidence:** [§12](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKM"></a>
### dog · ● proposed

A social animal.

- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB8), [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9), [§6](#su_01M82ABDR1CAX5PFZ2HWSEQHBH), [§7](#su_01M82ABDR1CAX5PFZ2HWSEQHBK), [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBN), [§13](#su_01M82ABDR28HTPAFF4C44FRBZ9), [§16](#su_01M82ABDR28HTPAFF4C44FRBZE), [§17](#su_01M82ABDR28HTPAFF4C44FRBZG), [§18](#su_01M82ABDR28HTPAFF4C44FRBZJ), [§19](#su_01M82ABDR28HTPAFF4C44FRBZP), [§22](#su_01M82ABDR28HTPAFF4C44FRBZR), [§23](#su_01M82ABDR28HTPAFF4C44FRBZS), [§25](#su_01M82ABDR30PE47ZK8WSGY3HX2), [§26](#su_01M82ABDR30PE47ZK8WSGY3HX3), [§28](#su_01M82ABDR30PE47ZK8WSGY3HX5), [§29](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKV"></a>
### dog registration · ● proposed

- **Synonyms:** registered
- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="cn_01M82AH1GXVV72WP99JQXMH6XS"></a>
### dog waste · ● proposed

- **Synonyms:** waste
- **Level:** 1
- **Evidence:** [§17](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="cn_01M82AFTZDSHCD0SK6T4N2YZW6"></a>
### leash · ● proposed

- **Level:** 1
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZC), [§16](#su_01M82ABDR28HTPAFF4C44FRBZE), [§29](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKS"></a>
### local authority · ● proposed

- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9), [§4](#su_01M82ABDR1CAX5PFZ2HWSEQHBF), [§29](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKT"></a>
### microchip · ● proposed

- **Synonyms:** microchipped
- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9), [§28](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="cn_01M82AE56ZYS5Y2Z0C35ECC9Y8"></a>
### owner · ● proposed

- **Synonyms:** dog owner
- **Level:** 1
- **Evidence:** [§7](#su_01M82ABDR1CAX5PFZ2HWSEQHBK), [§17](#su_01M82ABDR28HTPAFF4C44FRBZG), [§19](#su_01M82ABDR28HTPAFF4C44FRBZP), [§26](#su_01M82ABDR30PE47ZK8WSGY3HX3), [§29](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82ATVV0G4J5RJ6TZ063RNYR"></a>
### residual waste · ● proposed

- **Level:** 1
- **Evidence:** [§12](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="cn_01M82ATVV0G4J5RJ6TZ063RNYS"></a>
### toilet · ● proposed

- **Level:** 1
- **Evidence:** [§12](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="cn_01M82ATVV0G4J5RJ6TZ063RNYQ"></a>
### used litter · ● proposed

- **Is a:** litter
- **Level:** 1
- **Evidence:** [§12](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="cn_01M82AH1GXVV72WP99JQXMH6XT"></a>
### waste bin · ● proposed

- **Level:** 1
- **Evidence:** [§17](#su_01M82ABDR28HTPAFF4C44FRBZG)

## Relations

<a id="rl_01M82AC66KMJH32E2MQ3Z7ZBM1"></a>
### carries · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — carries → [microchip](#cn_01M82AC66KMJH32E2MQ3Z7ZBKT)
- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="rl_01M82ATVV0G4J5RJ6TZ063RNYY"></a>
### goes into · ● proposed

- [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ) — goes into → [residual waste](#cn_01M82ATVV0G4J5RJ6TZ063RNYR)
- **Level:** 1
- **Evidence:** [§12](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="rl_01M82AM9P6EWS5D1VJCAH8Z7VM"></a>
### is kept on · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — is kept on → [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6)
- **Level:** 1
- **Evidence:** [§29](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="rl_01M82AM9P6EWS5D1VJCAH8Z7VH"></a>
### is liable for · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — is liable for → damage
- **Level:** 1
- **Evidence:** [§29](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="rl_01M82AH1GXVV72WP99JQXMH6XY"></a>
### is put in · ● proposed

- [dog waste](#cn_01M82AH1GXVV72WP99JQXMH6XS) — is put in → [waste bin](#cn_01M82AH1GXVV72WP99JQXMH6XT)
- **Level:** 1
- **Evidence:** [§17](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="rl_01M82AC66KMJH32E2MQ3Z7ZBM0"></a>
### is registered with · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — is registered with → [local authority](#cn_01M82AC66KMJH32E2MQ3Z7ZBKS)
- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="rl_01M82ATVV0G4J5RJ6TZ063RNYZ"></a>
### never goes into · ● proposed

- [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ) — never goes into → [toilet](#cn_01M82ATVV0G4J5RJ6TZ063RNYS)
- **Level:** 1
- **Evidence:** [§12](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="rl_01M82ATVV0G4J5RJ6TZ063RNZ0"></a>
### never goes into · ● proposed

- [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ) — never goes into → [compost](#cn_01M82ATVV0G4J5RJ6TZ063RNYT)
- **Level:** 1
- **Evidence:** [§12](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="rl_01M82AQDR2NPZDR8C737517K8D"></a>
### owns · ● proposed

- [cat owner](#cn_01M82AQDR2NPZDR8C737517K87) — owns → [cat](#cn_01M82AQDR2NPZDR8C737517K86)
- **Level:** 1
- **Evidence:** [§1](#su_01M82APMQ68JDJRTYQDVNXFWWJ)

<a id="rl_01M82AH1GXVV72WP99JQXMH6XX"></a>
### picks up · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — picks up → [dog waste](#cn_01M82AH1GXVV72WP99JQXMH6XS)
- **Level:** 1
- **Evidence:** [§17](#su_01M82ABDR28HTPAFF4C44FRBZG)

## Rules

<a id="ru_01M82AH1GXVV72WP99JQXMH6Y3"></a>
### Always pick up dog waste and put it in a waste bin · ● proposed

owner **must** always pick up the dog's waste and put it in a waste bin

- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [dog waste](#cn_01M82AH1GXVV72WP99JQXMH6XS), [waste bin](#cn_01M82AH1GXVV72WP99JQXMH6XT), [picks up](#rl_01M82AH1GXVV72WP99JQXMH6XX), [is put in](#rl_01M82AH1GXVV72WP99JQXMH6XY)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§17](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="ru_01M82AC66KMJH32E2MQ3Z7ZBM4"></a>
### Dog microchip · ● proposed

dog owner **must** ensure the dog carries a microchip

- **When:** the dog is older than 4 months
- **Limit:** &gt; 4 months
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [microchip](#cn_01M82AC66KMJH32E2MQ3Z7ZBKT), [carries](#rl_01M82AC66KMJH32E2MQ3Z7ZBM1)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="ru_01M82AC66KMJH32E2MQ3Z7ZBM3"></a>
### Dog registration · ● proposed

dog owner **must** register the dog with the local authority

- **When:** the dog is older than 4 months
- **Limit:** &gt; 4 months
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [local authority](#cn_01M82AC66KMJH32E2MQ3Z7ZBKS), [dog registration](#cn_01M82AC66KMJH32E2MQ3Z7ZBKV), [is registered with](#rl_01M82AC66KMJH32E2MQ3Z7ZBM0)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="ru_01M82AM9P6EWS5D1VJCAH8Z7VT"></a>
### Leash in public places · ● proposed

dog owner **must** keep the dog on a leash in public places

- **When:** unless a sign allows free running
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6), public place, free-running sign, [is kept on](#rl_01M82AM9P6EWS5D1VJCAH8Z7VM), is located in
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§29](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="ru_01M82ATVV0G4J5RJ6TZ063RNZ6"></a>
### No used litter in the compost · ● proposed

cat owner **must not** put used litter into the compost

- **Refers to:** [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ), [compost](#cn_01M82ATVV0G4J5RJ6TZ063RNYT), [never goes into](#rl_01M82ATVV0G4J5RJ6TZ063RNZ0)
- **Applies to:** co_01M82APMQ5V0PTBT5SDYAF1JAP
- **Level:** 1
- **Evidence:** [§12](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="ru_01M82ATVV0G4J5RJ6TZ063RNZ5"></a>
### No used litter in the toilet · ● proposed

cat owner **must not** put used litter into the toilet

- **Refers to:** [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ), [toilet](#cn_01M82ATVV0G4J5RJ6TZ063RNYS), [never goes into](#rl_01M82ATVV0G4J5RJ6TZ063RNYZ)
- **Applies to:** co_01M82APMQ5V0PTBT5SDYAF1JAP
- **Level:** 1
- **Evidence:** [§12](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="ru_01M82AM9P6EWS5D1VJCAH8Z7VQ"></a>
### Owner is liable for dog damage · ● proposed

dog owner **must** be liable for any damage the dog causes

- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), damage, [is liable for](#rl_01M82AM9P6EWS5D1VJCAH8Z7VH), causes
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§29](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="ru_01M82ATVV0G4J5RJ6TZ063RNZ4"></a>
### Used litter into residual waste · ● proposed

cat owner **must** put used litter into the residual waste

- **Refers to:** [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ), [residual waste](#cn_01M82ATVV0G4J5RJ6TZ063RNYR), [goes into](#rl_01M82ATVV0G4J5RJ6TZ063RNYY)
- **Applies to:** co_01M82APMQ5V0PTBT5SDYAF1JAP
- **Level:** 1
- **Evidence:** [§12](#su_01M82APMQ7MGEVFK2CW6002H2W)

## Properties

<a id="pr_01M82AQDR2NPZDR8C737517K8P"></a>
### Cat lifespan · ● proposed

- **Of:** [cat](#cn_01M82AQDR2NPZDR8C737517K86)
- **lifespan:** 12 to 18 years
- **Level:** 1
- **Evidence:** [§1](#su_01M82APMQ68JDJRTYQDVNXFWWJ)

## Statements

<a id="st_01M82AQDR2NPZDR8C737517K7T"></a>
### Cat lifespan · ● proposed

A cat lives 12 to 18 years.

- **Level:** 1
- **Evidence:** [§1](#su_01M82APMQ68JDJRTYQDVNXFWWJ)

<a id="st_01M82AC66KMJH32E2MQ3Z7ZBK7"></a>
### Dog lifespan · ● proposed

A dog lives 10 to 15 years.

- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="st_01M82AC66KMJH32E2MQ3Z7ZBKB"></a>
### Dog microchip · ● proposed

A dog older than 4 months must carry a microchip.

- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="st_01M82AC66KMJH32E2MQ3Z7ZBKA"></a>
### Dog registration · ● proposed

A dog older than 4 months must be registered with the local authority.

- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="st_01M82AM9P6EWS5D1VJCAH8Z7TY"></a>
### Leash in public places · ● proposed

In public places, a dog must be kept on a leash unless a sign allows free running.

- **Level:** 1
- **Evidence:** [§29](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="st_01M82AC66KMJH32E2MQ3Z7ZBK8"></a>
### Lifelong needs of a dog · ● proposed

A dog needs daily exercise, company, training and veterinary care for its whole life.

- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="st_01M82AM9P5HMXJKJ1997DWSW20"></a>
### Owner liable for dog damage · ● proposed

The dog owner is liable for any damage the dog causes.

- **Level:** 1
- **Evidence:** [§29](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="st_01M82AH1GXVV72WP99JQXMH6X9"></a>
### Pick up dog waste · ● proposed

The owner must always pick up the dog's waste and put it in a waste bin.

- **Level:** 1
- **Evidence:** [§17](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="st_01M82ATVV0G4J5RJ6TZ063RNYA"></a>
### Used litter disposal · ● proposed

Used litter goes into the residual waste, never into the toilet or the compost.

- **Level:** 1
- **Evidence:** [§12](#su_01M82APMQ7MGEVFK2CW6002H2W)

## Evidence

<a id="su_01M82APMQ68JDJRTYQDVNXFWWJ"></a>
**§1** · 01-before-you-get-a-cat.md › 1. Before You Get a Cat

> A cat lives 12 to 18 years. Cats are independent, but they still need daily attention, play and a clean environment. Plan for food, litter, yearly veterinary visits and someone to look after the cat when you travel.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHB8"></a>
**§2** · 01-before-you-get-a-dog.md › 1. Before You Get a Dog

> A dog lives 10 to 15 years. It needs daily exercise, company, training and veterinary care for its whole life. Before you get a dog, check that your home, your working hours and your budget fit the dog you want.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHB9"></a>
**§3** · 01-before-you-get-a-dog.md › 1. Before You Get a Dog

> A dog older than 4 months must be registered with the local authority and must carry a microchip.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBF"></a>
**§4** · 02-choosing-a-breed.md › 2. Choosing a Breed

> Some breeds are classified as dangerous by the local authority. Check the local list before you choose a breed.

<a id="su_01M82APMQ68JDJRTYQDVNXFWWM"></a>
**§5** · 02-indoor-or-outdoor-cat.md › 2. Indoor or Outdoor Cat

> Decide early whether your cat will be an indoor cat or an outdoor cat.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBH"></a>
**§6** · 03-health-and-care/01-feeding.md › 3. Health and Care — 3.1 Feeding

> Feed an adult dog twice a day and a puppy three to four times a day. Fresh water must always be available. Chocolate, grapes, onions and xylitol are poisonous to dogs.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBK"></a>
**§7** · 03-health-and-care/02-vaccination-and-the-veterinarian.md › 3. Health and Care — 3.2 Vaccination and the Veterinarian

> A puppy receives its first vaccinations at 8 weeks of age. The rabies vaccination is mandatory and must be renewed every year. Take your dog to the veterinarian for a check-up at least once a year.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBN"></a>
**§8** · 03-health-and-care/03-grooming-and-hygiene.md › 3. Health and Care — 3.3 Grooming and Hygiene

> Brush your dog at least once a week; long-haired breeds need brushing every day. Trim the claws when you can hear them clicking on the floor. Wash your dog's bed and blankets once a week at 60 °C.

<a id="su_01M82APMQ7MGEVFK2CW6002H2P"></a>
**§9** · 03-home-and-equipment.md › 3. Home and Equipment

> Every cat needs a litter box, a scratching post, food and water bowls placed away from the litter box, and a quiet place to sleep. Secure windows and balconies with a net, because cats can fall from height.

<a id="su_01M82APMQ7MGEVFK2CW6002H2R"></a>
**§10** · 04-health-and-care/01-feeding.md › 4. Health and Care — 4.1 Feeding

> Feed an adult cat two to three small meals a day; kittens need four meals a day. Cats need meat-based food. Lilies, onions, chocolate and dog food are not suitable for cats; lilies are highly poisonous.

<a id="su_01M82APMQ7MGEVFK2CW6002H2T"></a>
**§11** · 04-health-and-care/02-vaccination-and-the-veterinarian.md › 4. Health and Care — 4.2 Vaccination and the Veterinarian

> A kitten receives its first vaccinations at 8 weeks of age. A cat that goes outdoors must also be vaccinated against rabies, renewed every year. Neuter your cat at about 5 to 6 months of age. Visit the veterinarian at least once a year.

<a id="su_01M82APMQ7MGEVFK2CW6002H2W"></a>
**§12** · 04-health-and-care/03-litter-box-hygiene.md › 4. Health and Care — 4.3 Litter Box Hygiene

> Provide one litter box per cat plus one extra. Remove clumps every day and replace all litter once a week. Used litter goes into the residual waste, never into the toilet or the compost.

<a id="su_01M82ABDR28HTPAFF4C44FRBZ9"></a>
**§13** · 04-puppy-basics.md › 4. Puppy Basics

> A puppy is a dog younger than 6 months. Puppies should not leave their mother before 8 weeks of age.

<a id="su_01M82APMQ7MGEVFK2CW6002H2Y"></a>
**§14** · 05-kittens.md › 5. Kittens

> A kitten is a cat younger than 6 months. Kittens should not leave their mother before 12 weeks of age. Let a new kitten explore one room first, then the rest of the flat. Kittens learn to use the litter box quickly if it is easy to reach.

<a id="su_01M82ABDR28HTPAFF4C44FRBZC"></a>
**§15** · 05-walking-and-the-leash/01-choosing-a-leash.md › 5. Walking and the Leash — 5.1 Choosing a Leash

> Use a leash of 1.5 to 2 metres for everyday walks. A retractable leash is not suitable in busy streets. Attach the leash to a well-fitting collar or harness: you should be able to slide two fingers under the collar.

<a id="su_01M82ABDR28HTPAFF4C44FRBZE"></a>
**§16** · 05-walking-and-the-leash/02-leash-training.md › 5. Walking and the Leash — 5.2 Leash Training

> Start leash training when the puppy is 8 to 10 weeks old. Reward the dog when the leash is loose, and stop walking when the dog pulls. Never jerk the leash.

<a id="su_01M82ABDR28HTPAFF4C44FRBZG"></a>
**§17** · 05-walking-and-the-leash/03-daily-walks.md › 5. Walking and the Leash — 5.3 Daily Walks

> An adult dog needs at least two walks a day: 30 to 60 minutes in total for small breeds and up to 2 hours for large and working breeds. A puppy must be taken outside to relieve itself every 2 to 3 hours. Always pick up your dog's waste and put it in a waste bin.

<a id="su_01M82ABDR28HTPAFF4C44FRBZJ"></a>
**§18** · 06-being-a-good-lead-for-your-dog.md › 6. Being a Good Lead for Your Dog

> Your dog looks to you for direction. Be its lead: a calm, consistent and confident leader whose signals it can trust.

<a id="su_01M82ABDR28HTPAFF4C44FRBZP"></a>
**§19** · 06-being-a-good-lead-for-your-dog.md › 6. Being a Good Lead for Your Dog

> A dog that does not see its owner as a reliable lead may become anxious or try to take control.

<a id="su_01M82APMQ7MGEVFK2CW6002H30"></a>
**§20** · 06-play-and-behaviour.md › 6. Play and Behaviour

> Play with your cat for at least 15 minutes twice a day. A cat that scratches furniture usually needs a better scratching post, not punishment. Never punish a cat physically. A cat that suddenly stops using its litter box may be ill and should see a veterinarian.

<a id="su_01M82APMQ7MGEVFK2CW6002H32"></a>
**§21** · 07-grooming.md › 7. Grooming

> Short-haired cats groom themselves; brush them once a week to reduce hair in the flat. Long-haired cats need brushing every day to prevent matting. Do not bathe a cat unless the veterinarian advises it.

<a id="su_01M82ABDR28HTPAFF4C44FRBZR"></a>
**§22** · 07-training-and-commands.md › 7. Training and Commands

> Every dog should learn five basic commands: *sit*, *down*, *stay*, *come* and *leave it*. Train in short sessions of 5 to 10 minutes, several times a day, and always end with a success.

<a id="su_01M82ABDR28HTPAFF4C44FRBZS"></a>
**§23** · 07-training-and-commands.md › 7. Training and Commands

> A dog training course with a certified trainer is recommended in the first year. Dogs of breeds classified as dangerous must pass an obedience test.

<a id="su_01M82APMQ7MGEVFK2CW6002H34"></a>
**§24** · 08-leaving-your-cat-alone.md › 8. Leaving Your Cat Alone

> An adult cat can stay alone for up to 24 hours if it has enough food, fresh water and a clean litter box. For longer absences, arrange for someone to visit the cat at least once a day.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX2"></a>
**§25** · 08-leaving-your-dog-alone.md › 8. Leaving Your Dog Alone

> Dogs are social animals. **Never leave an adult dog alone at home for more than 6 hours.** Puppies should not be left alone for more than 2 hours.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX3"></a>
**§26** · 08-leaving-your-dog-alone.md › 8. Leaving Your Dog Alone

> Before you leave, walk the dog, leave water and a safe chew toy, and keep your departure low-key. If your dog barks or howls while you are away, train it to be alone step by step, starting with a few minutes.

<a id="su_01M82APMQ7MGEVFK2CW6002H36"></a>
**§27** · 09-moving-house-with-a-cat.md › 9. Moving House with a Cat

> Cats are attached to their territory. On moving day, keep the cat in a closed room with its litter box. After the move, keep an outdoor cat indoors for at least 2 weeks before you let it outside, so that it learns its new home.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX5"></a>
**§28** · 09-travelling-with-your-dog.md › 9. Travelling with Your Dog

> In a car, a dog must travel in a crate or wear a safety harness attached to the seat belt. Never leave a dog in a parked car in warm weather. For travel abroad, your dog needs a pet passport, a microchip and a valid rabies vaccination.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX7"></a>
**§29** · 10-legal-obligations-and-responsibility.md › 10. Legal Obligations and Responsibility

> You are liable for any damage your dog causes. Third-party liability insurance for dog owners is strongly recommended, and it is mandatory for breeds classified as dangerous by the local authority. In public places, your dog must be kept on a leash unless a sign allows free running.
