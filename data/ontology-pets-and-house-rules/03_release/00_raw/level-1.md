# pets-and-house-rules · level 1

**Version:** raw+4eb170a · **Release:** raw · This file holds level 1, the core of the domain.

Explain what it takes to own a dog or a cat in a residential complex, and which house rules apply to pets and their owners.

This is the raw release: it also holds elements that are not approved yet. They are marked
`● proposed` or `◐ waiting for approval`, and drawn dashed in the diagrams.

## Taxonomy

```mermaid
flowchart TB
    classDef draft stroke-dasharray: 5 5
    cn_01M82B3MD8NCJFJC9394MZ8MQV["building complex"]
    cn_01M82AQDR2NPZDR8C737517K86["cat"]
    cn_01M82AQDR2NPZDR8C737517K87["cat owner"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYT["compost"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM["dog"]
    cn_01M82B3MD8NCJFJC9394MZ8MQN["dog owner"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKV["dog registration"]
    cn_01M82AH1GXVV72WP99JQXMH6XS["dog waste"]
    cn_01M82B0RVQB8E3F7FG9YPD26J7["house management"]
    cn_01M82B0RVQB8E3F7FG9YPD26JD["house rule"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW6["leash"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKS["local authority"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKT["microchip"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8["owner"]
    cn_01M82B2PPZPYF6543TD3RQQKNJ["pet"]
    cn_01M82B2PQ0Y5BYDSR06NJ167CE["pet owner"]
    cn_01M82B2PQ0Y5BYDSR06NJ167CG["pet registration"]
    cn_01M82B6NEKKV0CSECXDQRKNHNZ["pet textile"]
    cn_01M82B4TJPFJR5BJ36WDBJT000["pet waste"]
    cn_01M82B0RVQB8E3F7FG9YPD26J6["resident"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYR["residual waste"]
    cn_01M82B4TJPFJR5BJ36WDBJSZZZ["residual waste bin"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYS["toilet"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYQ["used litter"]
    cn_01M82AH1GXVV72WP99JQXMH6XT["waste bin"]
    class cn_01M82B3MD8NCJFJC9394MZ8MQV,cn_01M82AQDR2NPZDR8C737517K86,cn_01M82AQDR2NPZDR8C737517K87,cn_01M82ATVV0G4J5RJ6TZ063RNYT,cn_01M82AC66KMJH32E2MQ3Z7ZBKM,cn_01M82B3MD8NCJFJC9394MZ8MQN,cn_01M82AC66KMJH32E2MQ3Z7ZBKV,cn_01M82AH1GXVV72WP99JQXMH6XS,cn_01M82B0RVQB8E3F7FG9YPD26J7,cn_01M82B0RVQB8E3F7FG9YPD26JD,cn_01M82AFTZDSHCD0SK6T4N2YZW6,cn_01M82AC66KMJH32E2MQ3Z7ZBKS,cn_01M82AC66KMJH32E2MQ3Z7ZBKT,cn_01M82AE56ZYS5Y2Z0C35ECC9Y8,cn_01M82B2PPZPYF6543TD3RQQKNJ,cn_01M82B2PQ0Y5BYDSR06NJ167CE,cn_01M82B2PQ0Y5BYDSR06NJ167CG,cn_01M82B6NEKKV0CSECXDQRKNHNZ,cn_01M82B4TJPFJR5BJ36WDBJT000,cn_01M82B0RVQB8E3F7FG9YPD26J6,cn_01M82ATVV0G4J5RJ6TZ063RNYR,cn_01M82B4TJPFJR5BJ36WDBJSZZZ,cn_01M82ATVV0G4J5RJ6TZ063RNYS,cn_01M82ATVV0G4J5RJ6TZ063RNYQ,cn_01M82AH1GXVV72WP99JQXMH6XT draft
```

## Concepts and relations

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AQDR2NPZDR8C737517K86["cat"]
    cn_01M82AQDR2NPZDR8C737517K87["cat owner"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYT["compost"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM["dog"]
    cn_01M82B3MD8NCJFJC9394MZ8MQN["dog owner"]
    cn_01M82AH1GXVV72WP99JQXMH6XS["dog waste"]
    cn_01M82B0RVQB8E3F7FG9YPD26J7["house management"]
    cn_01M82B0RVQB8E3F7FG9YPD26JD["house rule"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW6["leash"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKS["local authority"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKT["microchip"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8["owner"]
    cn_01M82B2PPZPYF6543TD3RQQKNJ["pet"]
    cn_01M82B2PQ0Y5BYDSR06NJ167CE["pet owner"]
    cn_01M82B4TJPFJR5BJ36WDBJT000["pet waste"]
    cn_01M82B0RVQB8E3F7FG9YPD26J6["resident"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYR["residual waste"]
    cn_01M82B4TJPFJR5BJ36WDBJSZZZ["residual waste bin"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYS["toilet"]
    cn_01M82ATVV0G4J5RJ6TZ063RNYQ["used litter"]
    cn_01M82AH1GXVV72WP99JQXMH6XT["waste bin"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "is registered with" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKS
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "carries" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKT
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "is kept on" .-> cn_01M82AFTZDSHCD0SK6T4N2YZW6
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "is kept on" .-> cn_01M82AFTZDSHCD0SK6T4N2YZW6
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8 -. "picks up" .-> cn_01M82AH1GXVV72WP99JQXMH6XS
    cn_01M82AH1GXVV72WP99JQXMH6XS -. "is put in" .-> cn_01M82AH1GXVV72WP99JQXMH6XT
    cn_01M82AQDR2NPZDR8C737517K87 -. "owns" .-> cn_01M82AQDR2NPZDR8C737517K86
    cn_01M82ATVV0G4J5RJ6TZ063RNYQ -. "goes into" .-> cn_01M82ATVV0G4J5RJ6TZ063RNYR
    cn_01M82ATVV0G4J5RJ6TZ063RNYQ -. "never goes into" .-> cn_01M82ATVV0G4J5RJ6TZ063RNYS
    cn_01M82ATVV0G4J5RJ6TZ063RNYQ -. "never goes into" .-> cn_01M82ATVV0G4J5RJ6TZ063RNYT
    cn_01M82ATVV0G4J5RJ6TZ063RNYQ -. "goes into" .-> cn_01M82B4TJPFJR5BJ36WDBJSZZZ
    cn_01M82B0RVQB8E3F7FG9YPD26J6 -. "must follow" .-> cn_01M82B0RVQB8E3F7FG9YPD26JD
    cn_01M82B0RVQB8E3F7FG9YPD26J7 -. "enforces" .-> cn_01M82B0RVQB8E3F7FG9YPD26JD
    cn_01M82B2PPZPYF6543TD3RQQKNJ -. "must not disturb" .-> cn_01M82B0RVQB8E3F7FG9YPD26J6
    cn_01M82B2PPZPYF6543TD3RQQKNJ -. "is registered with" .-> cn_01M82B0RVQB8E3F7FG9YPD26J7
    cn_01M82B2PQ0Y5BYDSR06NJ167CE -. "owns" .-> cn_01M82B2PPZPYF6543TD3RQQKNJ
    cn_01M82B3MD8NCJFJC9394MZ8MQN -. "owns" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKM
    cn_01M82B4TJPFJR5BJ36WDBJT000 -. "goes into" .-> cn_01M82B4TJPFJR5BJ36WDBJSZZZ
    class cn_01M82AQDR2NPZDR8C737517K86,cn_01M82AQDR2NPZDR8C737517K87,cn_01M82ATVV0G4J5RJ6TZ063RNYT,cn_01M82AC66KMJH32E2MQ3Z7ZBKM,cn_01M82B3MD8NCJFJC9394MZ8MQN,cn_01M82AH1GXVV72WP99JQXMH6XS,cn_01M82B0RVQB8E3F7FG9YPD26J7,cn_01M82B0RVQB8E3F7FG9YPD26JD,cn_01M82AFTZDSHCD0SK6T4N2YZW6,cn_01M82AC66KMJH32E2MQ3Z7ZBKS,cn_01M82AC66KMJH32E2MQ3Z7ZBKT,cn_01M82AE56ZYS5Y2Z0C35ECC9Y8,cn_01M82B2PPZPYF6543TD3RQQKNJ,cn_01M82B2PQ0Y5BYDSR06NJ167CE,cn_01M82B4TJPFJR5BJ36WDBJT000,cn_01M82B0RVQB8E3F7FG9YPD26J6,cn_01M82ATVV0G4J5RJ6TZ063RNYR,cn_01M82B4TJPFJR5BJ36WDBJSZZZ,cn_01M82ATVV0G4J5RJ6TZ063RNYS,cn_01M82ATVV0G4J5RJ6TZ063RNYQ,cn_01M82AH1GXVV72WP99JQXMH6XT draft
```

## Concepts

<a id="cn_01M82B3MD8NCJFJC9394MZ8MQV"></a>
### building complex · ● proposed

- **Level:** 1
- **Evidence:** [§18](#su_01M82B00WB34E68SXWEMVZ22ED)

<a id="cn_01M82AQDR2NPZDR8C737517K86"></a>
### cat · ● proposed

- **Level:** 1
- **Evidence:** [§1](#su_01M82APMQ68JDJRTYQDVNXFWWJ), [§6](#su_01M82APMQ68JDJRTYQDVNXFWWM), [§11](#su_01M82APMQ7MGEVFK2CW6002H2P), [§13](#su_01M82APMQ7MGEVFK2CW6002H2R), [§14](#su_01M82APMQ7MGEVFK2CW6002H2T), [§15](#su_01M82APMQ7MGEVFK2CW6002H2W), [§23](#su_01M82APMQ7MGEVFK2CW6002H2Y), [§30](#su_01M82APMQ7MGEVFK2CW6002H30), [§31](#su_01M82APMQ7MGEVFK2CW6002H32), [§36](#su_01M82APMQ7MGEVFK2CW6002H34), [§39](#su_01M82APMQ7MGEVFK2CW6002H36)

<a id="cn_01M82AQDR2NPZDR8C737517K87"></a>
### cat owner · ● proposed

- **Level:** 1
- **Evidence:** [§1](#su_01M82APMQ68JDJRTYQDVNXFWWJ)

<a id="cn_01M82ATVV0G4J5RJ6TZ063RNYT"></a>
### compost · ● proposed

- **Level:** 1
- **Evidence:** [§15](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKM"></a>
### dog · ● proposed

A social animal.

- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB8), [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9), [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH), [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK), [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN), [§22](#su_01M82ABDR28HTPAFF4C44FRBZ9), [§25](#su_01M82ABDR28HTPAFF4C44FRBZE), [§26](#su_01M82ABDR28HTPAFF4C44FRBZG), [§28](#su_01M82ABDR28HTPAFF4C44FRBZJ), [§29](#su_01M82ABDR28HTPAFF4C44FRBZP), [§33](#su_01M82ABDR28HTPAFF4C44FRBZR), [§34](#su_01M82ABDR28HTPAFF4C44FRBZS), [§37](#su_01M82ABDR30PE47ZK8WSGY3HX2), [§38](#su_01M82ABDR30PE47ZK8WSGY3HX3), [§41](#su_01M82ABDR30PE47ZK8WSGY3HX5), [§42](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82B3MD8NCJFJC9394MZ8MQN"></a>
### dog owner · ● proposed

- **Synonyms:** owner
- **Sense:** Person who keeps and is responsible for a dog.
- **Level:** 1
- **Evidence:** [§18](#su_01M82B00WB34E68SXWEMVZ22ED), [§19](#su_01M82B00WB34E68SXWEMVZ22EE), [§20](#su_01M82B00WB34E68SXWEMVZ22EF)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKV"></a>
### dog registration · ● proposed

- **Synonyms:** registered
- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="cn_01M82AH1GXVV72WP99JQXMH6XS"></a>
### dog waste · ● proposed

- **Synonyms:** waste
- **Level:** 1
- **Evidence:** [§26](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="cn_01M82B0RVQB8E3F7FG9YPD26J7"></a>
### house management · ● proposed

Administers the buildings and enforces these rules.

- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN), [§16](#su_01M82B00WB34E68SXWEMVZ22EA), [§20](#su_01M82B00WB34E68SXWEMVZ22EF), [§27](#su_01M82B00WB34E68SXWEMVZ22EK), [§32](#su_01M82B00WB34E68SXWEMVZ22EQ), [§40](#su_01M82B00WCXHEC1FCHYNF4GYBC), [§43](#su_01M82B00WCXHEC1FCHYNF4GYBE)

<a id="cn_01M82B0RVQB8E3F7FG9YPD26JD"></a>
### house rule · ● proposed

- **Synonyms:** rules
- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="cn_01M82AFTZDSHCD0SK6T4N2YZW6"></a>
### leash · ● proposed

- **Synonyms:** lead
- **Level:** 1
- **Evidence:** [§24](#su_01M82ABDR28HTPAFF4C44FRBZC), [§25](#su_01M82ABDR28HTPAFF4C44FRBZE), [§42](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKS"></a>
### local authority · ● proposed

- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9), [§5](#su_01M82ABDR1CAX5PFZ2HWSEQHBF), [§42](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKT"></a>
### microchip · ● proposed

- **Synonyms:** microchipped
- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9), [§41](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="cn_01M82AE56ZYS5Y2Z0C35ECC9Y8"></a>
### owner · ● proposed

- **Synonyms:** dog owner
- **Level:** 1
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK), [§26](#su_01M82ABDR28HTPAFF4C44FRBZG), [§29](#su_01M82ABDR28HTPAFF4C44FRBZP), [§38](#su_01M82ABDR30PE47ZK8WSGY3HX3), [§42](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82B2PPZPYF6543TD3RQQKNJ"></a>
### pet · ● proposed

A dog or a cat.

- **Level:** 1
- **Evidence:** [§16](#su_01M82B00WB34E68SXWEMVZ22EA)

<a id="cn_01M82B2PQ0Y5BYDSR06NJ167CE"></a>
### pet owner · ● proposed

- **Level:** 1
- **Evidence:** [§16](#su_01M82B00WB34E68SXWEMVZ22EA)

<a id="cn_01M82B2PQ0Y5BYDSR06NJ167CG"></a>
### pet registration · ● proposed

- **Synonyms:** registered
- **Level:** 1
- **Evidence:** [§16](#su_01M82B00WB34E68SXWEMVZ22EA)

<a id="cn_01M82B6NEKKV0CSECXDQRKNHNZ"></a>
### pet textile · ● proposed

- **Synonyms:** pet textiles
- **Level:** 1
- **Evidence:** [§35](#su_01M82B00WB34E68SXWEMVZ22ES)

<a id="cn_01M82B4TJPFJR5BJ36WDBJT000"></a>
### pet waste · ● proposed

- **Level:** 1
- **Evidence:** [§27](#su_01M82B00WB34E68SXWEMVZ22EK)

<a id="cn_01M82B0RVQB8E3F7FG9YPD26J6"></a>
### resident · ● proposed

Anyone who lives in one of the buildings: tenants, owners and their household members.

- **Synonyms:** residents
- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN), [§7](#su_01M82B00WAF2BQ321TGZ91X4KQ), [§12](#su_01M82B00WAF2BQ321TGZ91X4KS), [§16](#su_01M82B00WB34E68SXWEMVZ22EA), [§32](#su_01M82B00WB34E68SXWEMVZ22EQ)

<a id="cn_01M82ATVV0G4J5RJ6TZ063RNYR"></a>
### residual waste · ● proposed

- **Level:** 1
- **Evidence:** [§15](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="cn_01M82B4TJPFJR5BJ36WDBJSZZZ"></a>
### residual waste bin · ● proposed

- **Level:** 1
- **Evidence:** [§27](#su_01M82B00WB34E68SXWEMVZ22EK)

<a id="cn_01M82ATVV0G4J5RJ6TZ063RNYS"></a>
### toilet · ● proposed

- **Level:** 1
- **Evidence:** [§15](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="cn_01M82ATVV0G4J5RJ6TZ063RNYQ"></a>
### used litter · ● proposed

- **Synonyms:** used cat litter
- **Is a:** litter
- **Level:** 1
- **Evidence:** [§15](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="cn_01M82AH1GXVV72WP99JQXMH6XT"></a>
### waste bin · ● proposed

- **Level:** 1
- **Evidence:** [§26](#su_01M82ABDR28HTPAFF4C44FRBZG)

## Relations

<a id="rl_01M82B0RVQB8E3F7FG9YPD26JF"></a>
### administers · ● proposed

- [house management](#cn_01M82B0RVQB8E3F7FG9YPD26J7) — administers → building
- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="rl_01M82B0RVQB8E3F7FG9YPD26JJ"></a>
### apply to · ● proposed

- [house rule](#cn_01M82B0RVQB8E3F7FG9YPD26JD) — apply to → building
- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="rl_01M82AC66KMJH32E2MQ3Z7ZBM1"></a>
### carries · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — carries → [microchip](#cn_01M82AC66KMJH32E2MQ3Z7ZBKT)
- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="rl_01M82B0RVQB8E3F7FG9YPD26JG"></a>
### enforces · ● proposed

- [house management](#cn_01M82B0RVQB8E3F7FG9YPD26J7) — enforces → [house rule](#cn_01M82B0RVQB8E3F7FG9YPD26JD)
- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="rl_01M82ATVV0G4J5RJ6TZ063RNYY"></a>
### goes into · ● proposed

- [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ) — goes into → [residual waste](#cn_01M82ATVV0G4J5RJ6TZ063RNYR)
- **Level:** 1
- **Evidence:** [§15](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="rl_01M82B4TJPFJR5BJ36WDBJT006"></a>
### goes into · ● proposed

- [pet waste](#cn_01M82B4TJPFJR5BJ36WDBJT000) — goes into → [residual waste bin](#cn_01M82B4TJPFJR5BJ36WDBJSZZZ)
- **Level:** 1
- **Evidence:** [§27](#su_01M82B00WB34E68SXWEMVZ22EK)

<a id="rl_01M82B4TJPFJR5BJ36WDBJT007"></a>
### goes into · ● proposed

- [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ) — goes into → [residual waste bin](#cn_01M82B4TJPFJR5BJ36WDBJSZZZ)
- **Level:** 1
- **Evidence:** [§27](#su_01M82B00WB34E68SXWEMVZ22EK)

<a id="rl_01M82B441FVKK345F8CJ12SYK8"></a>
### is kept inside · ● proposed

- litter box — is kept inside → flat
- **Level:** 1
- **Evidence:** [§21](#su_01M82B00WB34E68SXWEMVZ22EH)

<a id="rl_01M82AM9P6EWS5D1VJCAH8Z7VM"></a>
### is kept on · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — is kept on → [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6)
- **Level:** 1
- **Evidence:** [§42](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="rl_01M82B3MD8NCJFJC9394MZ8MR3"></a>
### is kept on · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — is kept on → [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6)
- **Level:** 1
- **Evidence:** [§17](#su_01M82B00WB34E68SXWEMVZ22EC)

<a id="rl_01M82AM9P6EWS5D1VJCAH8Z7VH"></a>
### is liable for · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — is liable for → damage
- **Level:** 1
- **Evidence:** [§42](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="rl_01M82AH1GXVV72WP99JQXMH6XY"></a>
### is put in · ● proposed

- [dog waste](#cn_01M82AH1GXVV72WP99JQXMH6XS) — is put in → [waste bin](#cn_01M82AH1GXVV72WP99JQXMH6XT)
- **Level:** 1
- **Evidence:** [§26](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="rl_01M82AC66KMJH32E2MQ3Z7ZBM0"></a>
### is registered with · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — is registered with → [local authority](#cn_01M82AC66KMJH32E2MQ3Z7ZBKS)
- **Level:** 1
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="rl_01M82B2PQ0Y5BYDSR06NJ167CK"></a>
### is registered with · ● proposed

- [pet](#cn_01M82B2PPZPYF6543TD3RQQKNJ) — is registered with → [house management](#cn_01M82B0RVQB8E3F7FG9YPD26J7)
- **Level:** 1
- **Evidence:** [§16](#su_01M82B00WB34E68SXWEMVZ22EA)

<a id="rl_01M82B0RVQB8E3F7FG9YPD26JE"></a>
### lives in · ● proposed

- [resident](#cn_01M82B0RVQB8E3F7FG9YPD26J6) — lives in → building
- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="rl_01M82B441FVKK345F8CJ12SYK6"></a>
### may not be kept in · ● proposed

- [cat](#cn_01M82AQDR2NPZDR8C737517K86) — may not be kept in → stairwell
- **Level:** 1
- **Evidence:** [§21](#su_01M82B00WB34E68SXWEMVZ22EH)

<a id="rl_01M82B441FVKK345F8CJ12SYK7"></a>
### may not be kept in · ● proposed

- [cat](#cn_01M82AQDR2NPZDR8C737517K86) — may not be kept in → cellar
- **Level:** 1
- **Evidence:** [§21](#su_01M82B00WB34E68SXWEMVZ22EH)

<a id="rl_01M82B1AN7D1ZA7ABBS5RZ4XKC"></a>
### must avoid during quiet hours · ● proposed

- [resident](#cn_01M82B0RVQB8E3F7FG9YPD26J6) — must avoid during quiet hours → noise
- **Level:** 1
- **Evidence:** [§7](#su_01M82B00WAF2BQ321TGZ91X4KQ)

<a id="rl_01M82B0RVQB8E3F7FG9YPD26JH"></a>
### must follow · ● proposed

- [resident](#cn_01M82B0RVQB8E3F7FG9YPD26J6) — must follow → [house rule](#cn_01M82B0RVQB8E3F7FG9YPD26JD)
- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="rl_01M82B2PQ0Y5BYDSR06NJ167CN"></a>
### must not disturb · ● proposed

- [pet](#cn_01M82B2PPZPYF6543TD3RQQKNJ) — must not disturb → [resident](#cn_01M82B0RVQB8E3F7FG9YPD26J6)
- **Level:** 1
- **Evidence:** [§16](#su_01M82B00WB34E68SXWEMVZ22EA)

<a id="rl_01M82ATVV0G4J5RJ6TZ063RNYZ"></a>
### never goes into · ● proposed

- [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ) — never goes into → [toilet](#cn_01M82ATVV0G4J5RJ6TZ063RNYS)
- **Level:** 1
- **Evidence:** [§15](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="rl_01M82ATVV0G4J5RJ6TZ063RNZ0"></a>
### never goes into · ● proposed

- [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ) — never goes into → [compost](#cn_01M82ATVV0G4J5RJ6TZ063RNYT)
- **Level:** 1
- **Evidence:** [§15](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="rl_01M82AQDR2NPZDR8C737517K8D"></a>
### owns · ● proposed

- [cat owner](#cn_01M82AQDR2NPZDR8C737517K87) — owns → [cat](#cn_01M82AQDR2NPZDR8C737517K86)
- **Level:** 1
- **Evidence:** [§1](#su_01M82APMQ68JDJRTYQDVNXFWWJ)

<a id="rl_01M82B2PQ0Y5BYDSR06NJ167CM"></a>
### owns · ● proposed

- [pet owner](#cn_01M82B2PQ0Y5BYDSR06NJ167CE) — owns → [pet](#cn_01M82B2PPZPYF6543TD3RQQKNJ)
- **Level:** 1
- **Evidence:** [§16](#su_01M82B00WB34E68SXWEMVZ22EA)

<a id="rl_01M82B3MD8NCJFJC9394MZ8MR4"></a>
### owns · ● proposed

- [dog owner](#cn_01M82B3MD8NCJFJC9394MZ8MQN) — owns → [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM)
- **Level:** 1
- **Evidence:** [§18](#su_01M82B00WB34E68SXWEMVZ22ED), [§19](#su_01M82B00WB34E68SXWEMVZ22EE)

<a id="rl_01M82AH1GXVV72WP99JQXMH6XX"></a>
### picks up · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — picks up → [dog waste](#cn_01M82AH1GXVV72WP99JQXMH6XS)
- **Level:** 1
- **Evidence:** [§26](#su_01M82ABDR28HTPAFF4C44FRBZG)

## Rules

<a id="ru_01M82AH1GXVV72WP99JQXMH6Y3"></a>
### Always pick up dog waste and put it in a waste bin · ● proposed

owner **must** always pick up the dog's waste and put it in a waste bin

- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [dog waste](#cn_01M82AH1GXVV72WP99JQXMH6XS), [waste bin](#cn_01M82AH1GXVV72WP99JQXMH6XT), [picks up](#rl_01M82AH1GXVV72WP99JQXMH6XX), [is put in](#rl_01M82AH1GXVV72WP99JQXMH6XY)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§26](#su_01M82ABDR28HTPAFF4C44FRBZG)

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

<a id="ru_01M82B3MD8NCJFJC9394MZ8MRB"></a>
### Dogs on lead in shared areas · ● proposed

dog owner **must** keep the dog on a lead at all times in the inner yard, the stairwells and the lifts

- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6), inner yard, stairwell, lift, [is kept on](#rl_01M82B3MD8NCJFJC9394MZ8MR3)
- **Applies to:** co_01M82B00W91390459HX0FJMY3T
- **Level:** 1
- **Evidence:** [§17](#su_01M82B00WB34E68SXWEMVZ22EC)

<a id="ru_01M82B0RVQB8E3F7FG9YPD26JN"></a>
### House management enforces the house rules · ● proposed

house management **must** enforce the house rules

- **Refers to:** [house management](#cn_01M82B0RVQB8E3F7FG9YPD26J7), [house rule](#cn_01M82B0RVQB8E3F7FG9YPD26JD), [enforces](#rl_01M82B0RVQB8E3F7FG9YPD26JG)
- **Applies to:** co_01M82B00W91390459HX0FJMY3T
- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="ru_01M82AM9P6EWS5D1VJCAH8Z7VT"></a>
### Leash in public places · ● proposed

dog owner **must** keep the dog on a leash in public places

- **When:** unless a sign allows free running
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6), public place, free-running sign, [is kept on](#rl_01M82AM9P6EWS5D1VJCAH8Z7VM), is located in
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§42](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="ru_01M82B3MD8NCJFJC9394MZ8MRC"></a>
### Maximum lead length · ● proposed

dog owner **must not** use a lead longer than 2 metres

- **Limit:** ≤ 2 m
- **Refers to:** [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6), [is kept on](#rl_01M82B3MD8NCJFJC9394MZ8MR3)
- **Applies to:** co_01M82B00W91390459HX0FJMY3T
- **Level:** 1
- **Evidence:** [§17](#su_01M82B00WB34E68SXWEMVZ22EC)

<a id="ru_01M82B6NEKKV0CSECXDQRKNHPD"></a>
### No pet textiles in shared washing machines · ● proposed

pet owner **must not** wash pet blankets, pet beds or other pet textiles in the shared washing machines

- **Refers to:** [pet textile](#cn_01M82B6NEKKV0CSECXDQRKNHNZ), pet blanket, pet bed, shared washing machine
- **Applies to:** co_01M82B00W91390459HX0FJMY3T
- **Level:** 1
- **Evidence:** [§35](#su_01M82B00WB34E68SXWEMVZ22ES)

<a id="ru_01M82B3MD8NCJFJC9394MZ8MRD"></a>
### No relieving in yard or flower beds · ● proposed

dog owner **must not** let the dog relieve itself in the inner yard or the flower beds

- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), inner yard, flower bed
- **Applies to:** co_01M82B00W91390459HX0FJMY3T
- **Level:** 1
- **Evidence:** [§18](#su_01M82B00WB34E68SXWEMVZ22ED)

<a id="ru_01M82ATVV0G4J5RJ6TZ063RNZ6"></a>
### No used litter in the compost · ● proposed

cat owner **must not** put used litter into the compost

- **Refers to:** [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ), [compost](#cn_01M82ATVV0G4J5RJ6TZ063RNYT), [never goes into](#rl_01M82ATVV0G4J5RJ6TZ063RNZ0)
- **Applies to:** co_01M82APMQ5V0PTBT5SDYAF1JAP
- **Level:** 1
- **Evidence:** [§15](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="ru_01M82ATVV0G4J5RJ6TZ063RNZ5"></a>
### No used litter in the toilet · ● proposed

cat owner **must not** put used litter into the toilet

- **Refers to:** [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ), [toilet](#cn_01M82ATVV0G4J5RJ6TZ063RNYS), [never goes into](#rl_01M82ATVV0G4J5RJ6TZ063RNYZ)
- **Applies to:** co_01M82APMQ5V0PTBT5SDYAF1JAP
- **Level:** 1
- **Evidence:** [§15](#su_01M82APMQ7MGEVFK2CW6002H2W)

<a id="ru_01M82AM9P6EWS5D1VJCAH8Z7VQ"></a>
### Owner is liable for dog damage · ● proposed

dog owner **must** be liable for any damage the dog causes

- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), damage, [is liable for](#rl_01M82AM9P6EWS5D1VJCAH8Z7VH), causes
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§42](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="ru_01M82B2PQ0Y5BYDSR06NJ167CQ"></a>
### Pet must not disturb residents · ● proposed

pet owner **must** make sure that their pet does not disturb other residents

- **Refers to:** [resident](#cn_01M82B0RVQB8E3F7FG9YPD26J6), [pet](#cn_01M82B2PPZPYF6543TD3RQQKNJ), [pet owner](#cn_01M82B2PQ0Y5BYDSR06NJ167CE), [must not disturb](#rl_01M82B2PQ0Y5BYDSR06NJ167CN)
- **Applies to:** co_01M82B00W91390459HX0FJMY3T
- **Level:** 1
- **Evidence:** [§16](#su_01M82B00WB34E68SXWEMVZ22EA)

<a id="ru_01M82B4TJPFJR5BJ36WDBJT009"></a>
### Pet waste only into residual waste bin · ● proposed

pet owner **must** put pet waste into the residual waste bin only

- **Refers to:** [residual waste bin](#cn_01M82B4TJPFJR5BJ36WDBJSZZZ), [pet waste](#cn_01M82B4TJPFJR5BJ36WDBJT000), [goes into](#rl_01M82B4TJPFJR5BJ36WDBJT006)
- **Applies to:** co_01M82B00W91390459HX0FJMY3T
- **Level:** 1
- **Evidence:** [§27](#su_01M82B00WB34E68SXWEMVZ22EK)

<a id="ru_01M82B2PQ0Y5BYDSR06NJ167CP"></a>
### Register pet within 14 days · ● proposed

pet owner **must** register the pet (dog or cat) with the house management

- **When:** within 14 days of moving in or acquiring the pet
- **Limit:** ≤ 14 days
- **Refers to:** [house management](#cn_01M82B0RVQB8E3F7FG9YPD26J7), [pet](#cn_01M82B2PPZPYF6543TD3RQQKNJ), [pet owner](#cn_01M82B2PQ0Y5BYDSR06NJ167CE), [pet registration](#cn_01M82B2PQ0Y5BYDSR06NJ167CG), moving in, acquiring a pet, [is registered with](#rl_01M82B2PQ0Y5BYDSR06NJ167CK)
- **Applies to:** co_01M82B00W91390459HX0FJMY3T
- **Level:** 1
- **Evidence:** [§16](#su_01M82B00WB34E68SXWEMVZ22EA)

<a id="ru_01M82B0RVQB8E3F7FG9YPD26JM"></a>
### Residents must follow the house rules · ● proposed

resident **must** follow the house rules

- **Refers to:** [resident](#cn_01M82B0RVQB8E3F7FG9YPD26J6), [house rule](#cn_01M82B0RVQB8E3F7FG9YPD26JD), [must follow](#rl_01M82B0RVQB8E3F7FG9YPD26JH)
- **Applies to:** co_01M82B00W91390459HX0FJMY3T
- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="ru_01M82B3MD8NCJFJC9394MZ8MRE"></a>
### Take dog outside complex to relieve · ● proposed

dog owner **must** take the dog outside the building complex to relieve itself

- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [building complex](#cn_01M82B3MD8NCJFJC9394MZ8MQV)
- **Applies to:** co_01M82B00W91390459HX0FJMY3T
- **Level:** 1
- **Evidence:** [§18](#su_01M82B00WB34E68SXWEMVZ22ED)

<a id="ru_01M82B4TJQ99E974JCJPXB3VN6"></a>
### Used cat litter only into residual waste bin · ● proposed

pet owner **must** put used cat litter into the residual waste bin only

- **Refers to:** [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ), [residual waste bin](#cn_01M82B4TJPFJR5BJ36WDBJSZZZ), [goes into](#rl_01M82B4TJPFJR5BJ36WDBJT007)
- **Applies to:** co_01M82B00W91390459HX0FJMY3T
- **Level:** 1
- **Evidence:** [§27](#su_01M82B00WB34E68SXWEMVZ22EK)

<a id="ru_01M82ATVV0G4J5RJ6TZ063RNZ4"></a>
### Used litter into residual waste · ● proposed

cat owner **must** put used litter into the residual waste

- **Refers to:** [used litter](#cn_01M82ATVV0G4J5RJ6TZ063RNYQ), [residual waste](#cn_01M82ATVV0G4J5RJ6TZ063RNYR), [goes into](#rl_01M82ATVV0G4J5RJ6TZ063RNYY)
- **Applies to:** co_01M82APMQ5V0PTBT5SDYAF1JAP
- **Level:** 1
- **Evidence:** [§15](#su_01M82APMQ7MGEVFK2CW6002H2W)

## Properties

<a id="pr_01M82B0RVQB8E3F7FG9YPD26JP"></a>
### Buildings covered by the rules · ● proposed

- **Of:** [house rule](#cn_01M82B0RVQB8E3F7FG9YPD26JD)
- **applies to buildings:** A, B and C
- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="pr_01M82AQDR2NPZDR8C737517K8P"></a>
### Cat lifespan · ● proposed

- **Of:** [cat](#cn_01M82AQDR2NPZDR8C737517K86)
- **lifespan:** 12 to 18 years
- **Level:** 1
- **Evidence:** [§1](#su_01M82APMQ68JDJRTYQDVNXFWWJ)

<a id="pr_01M82B2PQ0Y5BYDSR06NJ167CR"></a>
### Registration deadline · ● proposed

- **Of:** [pet registration](#cn_01M82B2PQ0Y5BYDSR06NJ167CG)
- **deadline:** 14 days after moving in or acquiring the pet
- **Level:** 1
- **Evidence:** [§16](#su_01M82B00WB34E68SXWEMVZ22EA)

## Statements

<a id="st_01M82AQDR2NPZDR8C737517K7T"></a>
### Cat lifespan · ● proposed

A cat lives 12 to 18 years.

- **Level:** 1
- **Evidence:** [§1](#su_01M82APMQ68JDJRTYQDVNXFWWJ)

<a id="st_01M82B441E6BBHH3GXQY9DWSBT"></a>
### Cats not kept in stairwells or cellar · ● proposed

Cats may not be kept in the stairwells or the cellar.

- **Level:** 1
- **Evidence:** [§21](#su_01M82B00WB34E68SXWEMVZ22EH)

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

<a id="st_01M82B0RVQB8E3F7FG9YPD26HV"></a>
### House management administers buildings · ● proposed

The house management administers the buildings.

- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="st_01M82B0RVQB8E3F7FG9YPD26HW"></a>
### House management enforces rules · ● proposed

The house management enforces these rules.

- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="st_01M82B3MD77GTCF7Q7S02RS3Q4"></a>
### Lead required in shared areas · ● proposed

Dogs must be kept on a lead at all times in the inner yard, the stairwells and the lifts.

- **Level:** 1
- **Evidence:** [§17](#su_01M82B00WB34E68SXWEMVZ22EC)

<a id="st_01M82AM9P6EWS5D1VJCAH8Z7TY"></a>
### Leash in public places · ● proposed

In public places, a dog must be kept on a leash unless a sign allows free running.

- **Level:** 1
- **Evidence:** [§42](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="st_01M82AC66KMJH32E2MQ3Z7ZBK8"></a>
### Lifelong needs of a dog · ● proposed

A dog needs daily exercise, company, training and veterinary care for its whole life.

- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="st_01M82B441E6BBHH3GXQY9DWSBV"></a>
### Litter boxes inside the flat · ● proposed

Litter boxes must be kept inside the flat.

- **Level:** 1
- **Evidence:** [§21](#su_01M82B00WB34E68SXWEMVZ22EH)

<a id="st_01M82B3MD8NCJFJC9394MZ8MPZ"></a>
### Maximum lead length · ● proposed

The lead may not be longer than 2 metres.

- **Level:** 1
- **Evidence:** [§17](#su_01M82B00WB34E68SXWEMVZ22EC)

<a id="st_01M82B2PPZPYF6543TD3RQQKNA"></a>
### No disturbance of residents · ● proposed

A pet owner must make sure that their pet does not disturb other residents.

- **Level:** 1
- **Evidence:** [§16](#su_01M82B00WB34E68SXWEMVZ22EA)

<a id="st_01M82B6NEKKV0CSECXDQRKNHNB"></a>
### No pet textiles in shared machines · ● proposed

Pet blankets, pet beds and other pet textiles may not be washed in the shared washing machines.

- **Level:** 1
- **Evidence:** [§35](#su_01M82B00WB34E68SXWEMVZ22ES)

<a id="st_01M82B3MD8NCJFJC9394MZ8MQ0"></a>
### No relieving in yard or flower beds · ● proposed

Dogs may not relieve themselves in the inner yard or the flower beds.

- **Level:** 1
- **Evidence:** [§18](#su_01M82B00WB34E68SXWEMVZ22ED)

<a id="st_01M82AM9P5HMXJKJ1997DWSW20"></a>
### Owner liable for dog damage · ● proposed

The dog owner is liable for any damage the dog causes.

- **Level:** 1
- **Evidence:** [§42](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="st_01M82B1AN7D1ZA7ABBS5RZ4XJX"></a>
### Persistent barking counts as noise · ● proposed

Noise to be avoided during quiet hours includes music, drilling and persistent barking.

- **Level:** 1
- **Evidence:** [§7](#su_01M82B00WAF2BQ321TGZ91X4KQ)

<a id="st_01M82B2PPZPYF6543TD3RQQKN8"></a>
### Pet registration · ● proposed

Every pet (dog or cat) must be registered with the house management.

- **Level:** 1
- **Evidence:** [§16](#su_01M82B00WB34E68SXWEMVZ22EA)

<a id="st_01M82B4TJPFJR5BJ36WDBJSZZF"></a>
### Pet waste goes into residual waste · ● proposed

Pet waste and used cat litter go into the residual waste bin only.

- **Level:** 1
- **Evidence:** [§27](#su_01M82B00WB34E68SXWEMVZ22EK)

<a id="st_01M82AH1GXVV72WP99JQXMH6X9"></a>
### Pick up dog waste · ● proposed

The owner must always pick up the dog's waste and put it in a waste bin.

- **Level:** 1
- **Evidence:** [§26](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="st_01M82B2PPZPYF6543TD3RQQKN9"></a>
### Registration deadline · ● proposed

A pet must be registered within 14 days of moving in or acquiring the pet.

- **Level:** 1
- **Evidence:** [§16](#su_01M82B00WB34E68SXWEMVZ22EA)

<a id="st_01M82B3MD8NCJFJC9394MZ8MQ1"></a>
### Relieving outside the complex · ● proposed

Dog owners take their dogs outside the building complex to relieve themselves.

- **Level:** 1
- **Evidence:** [§18](#su_01M82B00WB34E68SXWEMVZ22ED)

<a id="st_01M82B0RVQB8E3F7FG9YPD26HT"></a>
### Resident definition · ● proposed

A resident is anyone who lives in one of the buildings: tenants, owners and their household members.

- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="st_01M82B1AN7D1ZA7ABBS5RZ4XJW"></a>
### Residents avoid audible noise during quiet hours · ● proposed

During quiet hours, residents must avoid noise that can be heard in other flats or in the inner yard.

- **Level:** 1
- **Evidence:** [§7](#su_01M82B00WAF2BQ321TGZ91X4KQ)

<a id="st_01M82B0RVQB8E3F7FG9YPD26HX"></a>
### Residents must follow the rules · ● proposed

Every resident must follow these rules.

- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="st_01M82B0RVQB8E3F7FG9YPD26HS"></a>
### Scope of the rules · ● proposed

These rules apply to buildings A, B and C around the shared inner yard.

- **Level:** 1
- **Evidence:** [§4](#su_01M82B00WAF2BQ321TGZ91X4KN)

<a id="st_01M82ATVV0G4J5RJ6TZ063RNYA"></a>
### Used litter disposal · ● proposed

Used litter goes into the residual waste, never into the toilet or the compost.

- **Level:** 1
- **Evidence:** [§15](#su_01M82APMQ7MGEVFK2CW6002H2W)

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

<a id="su_01M82B00WAF2BQ321TGZ91X4KN"></a>
**§4** · 01-scope-and-definitions.md › 1. Scope and Definitions

> These rules apply to buildings A, B and C around the shared inner yard. A **resident** is anyone who lives in one of the buildings: tenants, owners and their household members. The **house management** administers the buildings and enforces these rules. Every resident must follow them.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBF"></a>
**§5** · 02-choosing-a-breed.md › 2. Choosing a Breed

> Some breeds are classified as dangerous by the local authority. Check the local list before you choose a breed.

<a id="su_01M82APMQ68JDJRTYQDVNXFWWM"></a>
**§6** · 02-indoor-or-outdoor-cat.md › 2. Indoor or Outdoor Cat

> Decide early whether your cat will be an indoor cat or an outdoor cat.

<a id="su_01M82B00WAF2BQ321TGZ91X4KQ"></a>
**§7** · 02-quiet-hours.md › 2. Quiet Hours

> Quiet hours are from 22:00 to 07:00 on weekdays and from 22:00 to 09:00 on weekends and public holidays. During quiet hours, residents must avoid noise that can be heard in other flats or in the inner yard, including music, drilling and persistent barking.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBH"></a>
**§8** · 03-health-and-care/01-feeding.md › 3. Health and Care — 3.1 Feeding

> Feed an adult dog twice a day and a puppy three to four times a day. Fresh water must always be available. Chocolate, grapes, onions and xylitol are poisonous to dogs.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBK"></a>
**§9** · 03-health-and-care/02-vaccination-and-the-veterinarian.md › 3. Health and Care — 3.2 Vaccination and the Veterinarian

> A puppy receives its first vaccinations at 8 weeks of age. The rabies vaccination is mandatory and must be renewed every year. Take your dog to the veterinarian for a check-up at least once a year.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBN"></a>
**§10** · 03-health-and-care/03-grooming-and-hygiene.md › 3. Health and Care — 3.3 Grooming and Hygiene

> Brush your dog at least once a week; long-haired breeds need brushing every day. Trim the claws when you can hear them clicking on the floor. Wash your dog's bed and blankets once a week at 60 °C.

<a id="su_01M82APMQ7MGEVFK2CW6002H2P"></a>
**§11** · 03-home-and-equipment.md › 3. Home and Equipment

> Every cat needs a litter box, a scratching post, food and water bowls placed away from the litter box, and a quiet place to sleep. Secure windows and balconies with a net, because cats can fall from height.

<a id="su_01M82B00WAF2BQ321TGZ91X4KS"></a>
**§12** · 03-the-shared-inner-yard.md › 3. The Shared Inner Yard

> The inner yard is shared by all residents. Children may play there between 08:00 and 20:00. Bicycles must be parked in the bicycle racks only. Barbecues are allowed only in the marked barbecue area and never during quiet hours.

<a id="su_01M82APMQ7MGEVFK2CW6002H2R"></a>
**§13** · 04-health-and-care/01-feeding.md › 4. Health and Care — 4.1 Feeding

> Feed an adult cat two to three small meals a day; kittens need four meals a day. Cats need meat-based food. Lilies, onions, chocolate and dog food are not suitable for cats; lilies are highly poisonous.

<a id="su_01M82APMQ7MGEVFK2CW6002H2T"></a>
**§14** · 04-health-and-care/02-vaccination-and-the-veterinarian.md › 4. Health and Care — 4.2 Vaccination and the Veterinarian

> A kitten receives its first vaccinations at 8 weeks of age. A cat that goes outdoors must also be vaccinated against rabies, renewed every year. Neuter your cat at about 5 to 6 months of age. Visit the veterinarian at least once a year.

<a id="su_01M82APMQ7MGEVFK2CW6002H2W"></a>
**§15** · 04-health-and-care/03-litter-box-hygiene.md › 4. Health and Care — 4.3 Litter Box Hygiene

> Provide one litter box per cat plus one extra. Remove clumps every day and replace all litter once a week. Used litter goes into the residual waste, never into the toilet or the compost.

<a id="su_01M82B00WB34E68SXWEMVZ22EA"></a>
**§16** · 04-pets/01-registering-pets.md › 4. Pets — 4.1 Registering Pets

> Every pet (dog or cat) must be registered with the house management within 14 days of moving in or acquiring the pet. A pet owner must make sure that their pet does not disturb other residents.

<a id="su_01M82B00WB34E68SXWEMVZ22EC"></a>
**§17** · 04-pets/02-dogs.md › 4. Pets — 4.2 Dogs

> Dogs must be kept on a lead at all times in the inner yard, the stairwells and the lifts. The lead may not be longer than 2 metres.

<a id="su_01M82B00WB34E68SXWEMVZ22ED"></a>
**§18** · 04-pets/02-dogs.md › 4. Pets — 4.2 Dogs

> Dogs may not relieve themselves in the inner yard or the flower beds. Dog owners take their dogs outside the building complex for this.

<a id="su_01M82B00WB34E68SXWEMVZ22EE"></a>
**§19** · 04-pets/02-dogs.md › 4. Pets — 4.2 Dogs

> The maximum time a dog may be left alone in a flat depends on the dog's education (training) and its specific breed. Owners are responsible for knowing the limit that applies to their dog.

<a id="su_01M82B00WB34E68SXWEMVZ22EF"></a>
**§20** · 04-pets/02-dogs.md › 4. Pets — 4.2 Dogs

> If a dog barks persistently while left alone, the house management may require the owner to arrange care.

<a id="su_01M82B00WB34E68SXWEMVZ22EH"></a>
**§21** · 04-pets/03-cats.md › 4. Pets — 4.3 Cats

> Cats may move freely in the inner yard. Cats may not be kept in the stairwells or the cellar. Litter boxes must be kept inside the flat.

<a id="su_01M82ABDR28HTPAFF4C44FRBZ9"></a>
**§22** · 04-puppy-basics.md › 4. Puppy Basics

> A puppy is a dog younger than 6 months. Puppies should not leave their mother before 8 weeks of age.

<a id="su_01M82APMQ7MGEVFK2CW6002H2Y"></a>
**§23** · 05-kittens.md › 5. Kittens

> A kitten is a cat younger than 6 months. Kittens should not leave their mother before 12 weeks of age. Let a new kitten explore one room first, then the rest of the flat. Kittens learn to use the litter box quickly if it is easy to reach.

<a id="su_01M82ABDR28HTPAFF4C44FRBZC"></a>
**§24** · 05-walking-and-the-leash/01-choosing-a-leash.md › 5. Walking and the Leash — 5.1 Choosing a Leash

> Use a leash of 1.5 to 2 metres for everyday walks. A retractable leash is not suitable in busy streets. Attach the leash to a well-fitting collar or harness: you should be able to slide two fingers under the collar.

<a id="su_01M82ABDR28HTPAFF4C44FRBZE"></a>
**§25** · 05-walking-and-the-leash/02-leash-training.md › 5. Walking and the Leash — 5.2 Leash Training

> Start leash training when the puppy is 8 to 10 weeks old. Reward the dog when the leash is loose, and stop walking when the dog pulls. Never jerk the leash.

<a id="su_01M82ABDR28HTPAFF4C44FRBZG"></a>
**§26** · 05-walking-and-the-leash/03-daily-walks.md › 5. Walking and the Leash — 5.3 Daily Walks

> An adult dog needs at least two walks a day: 30 to 60 minutes in total for small breeds and up to 2 hours for large and working breeds. A puppy must be taken outside to relieve itself every 2 to 3 hours. Always pick up your dog's waste and put it in a waste bin.

<a id="su_01M82B00WB34E68SXWEMVZ22EK"></a>
**§27** · 05-waste-and-recycling.md › 5. Waste and Recycling

> Waste is sorted in the bin room of building B: paper, plastic, glass, organic waste and residual waste. Pet waste and used cat litter go into the residual waste bin only. Bulky items must be booked for collection with the house management.

<a id="su_01M82ABDR28HTPAFF4C44FRBZJ"></a>
**§28** · 06-being-a-good-lead-for-your-dog.md › 6. Being a Good Lead for Your Dog

> Your dog looks to you for direction. Be its lead: a calm, consistent and confident leader whose signals it can trust.

<a id="su_01M82ABDR28HTPAFF4C44FRBZP"></a>
**§29** · 06-being-a-good-lead-for-your-dog.md › 6. Being a Good Lead for Your Dog

> A dog that does not see its owner as a reliable lead may become anxious or try to take control.

<a id="su_01M82APMQ7MGEVFK2CW6002H30"></a>
**§30** · 06-play-and-behaviour.md › 6. Play and Behaviour

> Play with your cat for at least 15 minutes twice a day. A cat that scratches furniture usually needs a better scratching post, not punishment. Never punish a cat physically. A cat that suddenly stops using its litter box may be ill and should see a veterinarian.

<a id="su_01M82APMQ7MGEVFK2CW6002H32"></a>
**§31** · 07-grooming.md › 7. Grooming

> Short-haired cats groom themselves; brush them once a week to reduce hair in the flat. Long-haired cats need brushing every day to prevent matting. Do not bathe a cat unless the veterinarian advises it.

<a id="su_01M82B00WB34E68SXWEMVZ22EQ"></a>
**§32** · 07-security-and-access.md › 7. Security and Access

> The main doors of each building stay closed and locked from 22:00 to 06:00; residents open them with their own key. Do not let strangers into the building. Lost keys must be reported to the house management at once.

<a id="su_01M82ABDR28HTPAFF4C44FRBZR"></a>
**§33** · 07-training-and-commands.md › 7. Training and Commands

> Every dog should learn five basic commands: *sit*, *down*, *stay*, *come* and *leave it*. Train in short sessions of 5 to 10 minutes, several times a day, and always end with a success.

<a id="su_01M82ABDR28HTPAFF4C44FRBZS"></a>
**§34** · 07-training-and-commands.md › 7. Training and Commands

> A dog training course with a certified trainer is recommended in the first year. Dogs of breeds classified as dangerous must pass an obedience test.

<a id="su_01M82B00WB34E68SXWEMVZ22ES"></a>
**§35** · 08-laundry-and-cellar.md › 8. Laundry and Cellar

> The shared laundry room is in the cellar of building A and may be used from 07:00 to 21:00. Book a slot on the list at the door. Pet blankets, pet beds and other pet textiles may not be washed in the shared washing machines. Each flat has one cellar compartment; flammable liquids may not be stored there.

<a id="su_01M82APMQ7MGEVFK2CW6002H34"></a>
**§36** · 08-leaving-your-cat-alone.md › 8. Leaving Your Cat Alone

> An adult cat can stay alone for up to 24 hours if it has enough food, fresh water and a clean litter box. For longer absences, arrange for someone to visit the cat at least once a day.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX2"></a>
**§37** · 08-leaving-your-dog-alone.md › 8. Leaving Your Dog Alone

> Dogs are social animals. **Never leave an adult dog alone at home for more than 6 hours.** Puppies should not be left alone for more than 2 hours.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX3"></a>
**§38** · 08-leaving-your-dog-alone.md › 8. Leaving Your Dog Alone

> Before you leave, walk the dog, leave water and a safe chew toy, and keep your departure low-key. If your dog barks or howls while you are away, train it to be alone step by step, starting with a few minutes.

<a id="su_01M82APMQ7MGEVFK2CW6002H36"></a>
**§39** · 09-moving-house-with-a-cat.md › 9. Moving House with a Cat

> Cats are attached to their territory. On moving day, keep the cat in a closed room with its litter box. After the move, keep an outdoor cat indoors for at least 2 weeks before you let it outside, so that it learns its new home.

<a id="su_01M82B00WCXHEC1FCHYNF4GYBC"></a>
**§40** · 09-renovation-and-moving.md › 9. Renovation and Moving

> Noisy work such as drilling is allowed on weekdays from 08:00 to 12:00 and from 14:00 to 18:00, and on Saturdays from 09:00 to 12:00. Announce a move to the house management at least 7 days in advance, and protect the lift with the covers provided.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX5"></a>
**§41** · 09-travelling-with-your-dog.md › 9. Travelling with Your Dog

> In a car, a dog must travel in a crate or wear a safety harness attached to the seat belt. Never leave a dog in a parked car in warm weather. For travel abroad, your dog needs a pet passport, a microchip and a valid rabies vaccination.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX7"></a>
**§42** · 10-legal-obligations-and-responsibility.md › 10. Legal Obligations and Responsibility

> You are liable for any damage your dog causes. Third-party liability insurance for dog owners is strongly recommended, and it is mandatory for breeds classified as dangerous by the local authority. In public places, your dog must be kept on a leash unless a sign allows free running.

<a id="su_01M82B00WCXHEC1FCHYNF4GYBE"></a>
**§43** · 10-reporting-and-enforcement.md › 10. Reporting and Enforcement

> Report damage, noise complaints and rule violations to the house management in writing. Repeated violations after a written warning may lead to termination of the tenancy.
