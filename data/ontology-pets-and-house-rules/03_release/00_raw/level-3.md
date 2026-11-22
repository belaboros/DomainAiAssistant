# pets-and-house-rules · level 3

**Version:** raw+759da11 · **Release:** raw · This file holds levels 1 to 3; levels are cumulative.

Explain what it takes to own a dog or a cat in a residential complex, and which house rules apply to pets and their owners.

This is the raw release: it also holds elements that are not approved yet. They are marked
`● proposed` or `◐ waiting for approval`, and drawn dashed in the diagrams.

## Taxonomy

### Taxonomy of breed

```mermaid
flowchart TB
    classDef draft stroke-dasharray: 5 5
    cn_01M82ACZDNRYXG7FZCA8KC7FCX["breed"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD2["dangerous breed"]
    cn_01M82ACZDNRYXG7FZCA8KC7FCZ["large and working breed"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD0["long-haired breed"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD1["short-haired breed"]
    cn_01M82ACZDNRYXG7FZCA8KC7FCY["small companion breed"]
    cn_01M82ACZDNRYXG7FZCA8KC7FCX --> cn_01M82ACZDNRYXG7FZCA8KC7FD2
    cn_01M82ACZDNRYXG7FZCA8KC7FCX --> cn_01M82ACZDNRYXG7FZCA8KC7FCZ
    cn_01M82ACZDNRYXG7FZCA8KC7FCX --> cn_01M82ACZDNRYXG7FZCA8KC7FD0
    cn_01M82ACZDNRYXG7FZCA8KC7FCX --> cn_01M82ACZDNRYXG7FZCA8KC7FD1
    cn_01M82ACZDNRYXG7FZCA8KC7FCX --> cn_01M82ACZDNRYXG7FZCA8KC7FCY
    class cn_01M82ACZDNRYXG7FZCA8KC7FCX,cn_01M82ACZDNRYXG7FZCA8KC7FD2,cn_01M82ACZDNRYXG7FZCA8KC7FCZ,cn_01M82ACZDNRYXG7FZCA8KC7FD0,cn_01M82ACZDNRYXG7FZCA8KC7FD1,cn_01M82ACZDNRYXG7FZCA8KC7FCY draft
```

### Taxonomy of dog

```mermaid
flowchart TB
    classDef draft stroke-dasharray: 5 5
    cn_01M82ADJQKNCFSCKCDMA3H0R86["adult dog"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM["dog"]
    cn_01M82AJ8HWH90DHFSC2JB20DG1["dog of a dangerous breed"]
    cn_01M82AF7YTEGBGGS9B245D10JK["mother"]
    cn_01M82AF7YTEGBGGS9B245D10JJ["puppy"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM --> cn_01M82ADJQKNCFSCKCDMA3H0R86
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM --> cn_01M82AJ8HWH90DHFSC2JB20DG1
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM --> cn_01M82AF7YTEGBGGS9B245D10JK
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM --> cn_01M82AF7YTEGBGGS9B245D10JJ
    class cn_01M82ADJQKNCFSCKCDMA3H0R86,cn_01M82AC66KMJH32E2MQ3Z7ZBKM,cn_01M82AJ8HWH90DHFSC2JB20DG1,cn_01M82AF7YTEGBGGS9B245D10JK,cn_01M82AF7YTEGBGGS9B245D10JJ draft
```

### Taxonomy of food poisonous to dogs

```mermaid
flowchart TB
    classDef draft stroke-dasharray: 5 5
    cn_01M82ADJQKNCFSCKCDMA3H0R8B["chocolate"]
    cn_01M82ADJQKNCFSCKCDMA3H0R8A["food poisonous to dogs"]
    cn_01M82ADJQKNCFSCKCDMA3H0R8C["grape"]
    cn_01M82ADJQKNCFSCKCDMA3H0R8D["onion"]
    cn_01M82ADJQKNCFSCKCDMA3H0R8E["xylitol"]
    cn_01M82ADJQKNCFSCKCDMA3H0R8A --> cn_01M82ADJQKNCFSCKCDMA3H0R8B
    cn_01M82ADJQKNCFSCKCDMA3H0R8A --> cn_01M82ADJQKNCFSCKCDMA3H0R8C
    cn_01M82ADJQKNCFSCKCDMA3H0R8A --> cn_01M82ADJQKNCFSCKCDMA3H0R8D
    cn_01M82ADJQKNCFSCKCDMA3H0R8A --> cn_01M82ADJQKNCFSCKCDMA3H0R8E
    class cn_01M82ADJQKNCFSCKCDMA3H0R8B,cn_01M82ADJQKNCFSCKCDMA3H0R8A,cn_01M82ADJQKNCFSCKCDMA3H0R8C,cn_01M82ADJQKNCFSCKCDMA3H0R8D,cn_01M82ADJQKNCFSCKCDMA3H0R8E draft
```

### Taxonomy of grooming

```mermaid
flowchart TB
    classDef draft stroke-dasharray: 5 5
    cn_01M82AEQW4JVCNX0WEDNNR61W1["brushing"]
    cn_01M82AEQW4JVCNX0WEDNNR61W2["claw trimming"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD6["grooming"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD6 --> cn_01M82AEQW4JVCNX0WEDNNR61W1
    cn_01M82ACZDNRYXG7FZCA8KC7FD6 --> cn_01M82AEQW4JVCNX0WEDNNR61W2
    class cn_01M82AEQW4JVCNX0WEDNNR61W1,cn_01M82AEQW4JVCNX0WEDNNR61W2,cn_01M82ACZDNRYXG7FZCA8KC7FD6 draft
```

### Taxonomy of leash

```mermaid
flowchart TB
    classDef draft stroke-dasharray: 5 5
    cn_01M82AFTZDSHCD0SK6T4N2YZW6["leash"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW7["retractable leash"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW6 --> cn_01M82AFTZDSHCD0SK6T4N2YZW7
    class cn_01M82AFTZDSHCD0SK6T4N2YZW6,cn_01M82AFTZDSHCD0SK6T4N2YZW7 draft
```

### Taxonomy of vaccination

```mermaid
flowchart TB
    classDef draft stroke-dasharray: 5 5
    cn_01M82AE56ZYS5Y2Z0C35ECC9YA["rabies vaccination"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y9["vaccination"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y9 --> cn_01M82AE56ZYS5Y2Z0C35ECC9YA
    class cn_01M82AE56ZYS5Y2Z0C35ECC9YA,cn_01M82AE56ZYS5Y2Z0C35ECC9Y9 draft
```

### Other concepts

```mermaid
flowchart TB
    classDef draft stroke-dasharray: 5 5
    cn_01M82AK1Z9HNB4ZNT1JN5CCR6S["barking or howling"]
    cn_01M82AJ8HWH90DHFSC2JB20DFW["basic command"]
    cn_01M82AEQW4JVCNX0WEDNNR61W6["blanket"]
    cn_01M82AFTZDSHCD0SK6T4N2YZWB["busy street"]
    cn_01M82AKNKGVB3WQ6AJ3QXNT524["car"]
    cn_01M82AJ8HWH90DHFSC2JB20DFZ["certified trainer"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9YC["check-up"]
    cn_01M82AEQW4JVCNX0WEDNNR61W4["claw"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW8["collar"]
    cn_01M82AHPS6SQKW9E9EPJYC3KMN["command word"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKP["company"]
    cn_01M82AKNKGVB3WQ6AJ3QXNT525["crate"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKN["daily exercise"]
    cn_01M82AM9P6EWS5D1VJCAH8Z7VF["damage"]
    cn_01M82AEQW4JVCNX0WEDNNR61W5["dog bed"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKV["dog registration"]
    cn_01M82AJ8HWH90DHFSC2JB20DFY["dog training course"]
    cn_01M82AH1GXVV72WP99JQXMH6XS["dog waste"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD7["exercise"]
    cn_01M82AHPS6SQKW9E9EPJYC3KMP["family"]
    cn_01M82ADJQKNCFSCKCDMA3H0R88["feeding"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD5["flat"]
    cn_01M82AM9P6EWS5D1VJCAH8Z7VG["free-running sign"]
    cn_01M82ADJQKNCFSCKCDMA3H0R89["fresh water"]
    cn_01M82AHPS6SQKW9E9EPJYC3KMR["good behaviour"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW9["harness"]
    cn_01M82AF7YTEGBGGS9B245D10JM["house training"]
    cn_01M82AHPS6SQKW9E9EPJYC3KMQ["household rule for the dog"]
    cn_01M82AH1GXVV72WP99JQXMH6XQ["large breed"]
    cn_01M82AHPS6SQKW9E9EPJYC3KMM["lead (leader)"]
    cn_01M82AG9DZ4Q7M3Z8RX016AKWJ["leash training"]
    cn_01M82AK1Z8YRQBGAGXAECRMD6W["leaving the dog alone"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKS["local authority"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD4["local list of dangerous breeds"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKT["microchip"]
    cn_01M82AJ8HWH90DHFSC2JB20DG2["obedience test"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8["owner"]
    cn_01M82AKNKGVB3WQ6AJ3QXNT528["pet passport"]
    cn_01M82AM9P6EWS5D1VJCAH8Z7VE["public place"]
    cn_01M82AHPS6SQKW9E9EPJYC3KMT["reward"]
    class cn_01M82AK1Z9HNB4ZNT1JN5CCR6S,cn_01M82AJ8HWH90DHFSC2JB20DFW,cn_01M82AEQW4JVCNX0WEDNNR61W6,cn_01M82AFTZDSHCD0SK6T4N2YZWB,cn_01M82AKNKGVB3WQ6AJ3QXNT524,cn_01M82AJ8HWH90DHFSC2JB20DFZ,cn_01M82AE56ZYS5Y2Z0C35ECC9YC,cn_01M82AEQW4JVCNX0WEDNNR61W4,cn_01M82AFTZDSHCD0SK6T4N2YZW8,cn_01M82AHPS6SQKW9E9EPJYC3KMN,cn_01M82AC66KMJH32E2MQ3Z7ZBKP,cn_01M82AKNKGVB3WQ6AJ3QXNT525,cn_01M82AC66KMJH32E2MQ3Z7ZBKN,cn_01M82AM9P6EWS5D1VJCAH8Z7VF,cn_01M82AEQW4JVCNX0WEDNNR61W5,cn_01M82AC66KMJH32E2MQ3Z7ZBKV,cn_01M82AJ8HWH90DHFSC2JB20DFY,cn_01M82AH1GXVV72WP99JQXMH6XS,cn_01M82ACZDNRYXG7FZCA8KC7FD7,cn_01M82AHPS6SQKW9E9EPJYC3KMP,cn_01M82ADJQKNCFSCKCDMA3H0R88,cn_01M82ACZDNRYXG7FZCA8KC7FD5,cn_01M82AM9P6EWS5D1VJCAH8Z7VG,cn_01M82ADJQKNCFSCKCDMA3H0R89,cn_01M82AHPS6SQKW9E9EPJYC3KMR,cn_01M82AFTZDSHCD0SK6T4N2YZW9,cn_01M82AF7YTEGBGGS9B245D10JM,cn_01M82AHPS6SQKW9E9EPJYC3KMQ,cn_01M82AH1GXVV72WP99JQXMH6XQ,cn_01M82AHPS6SQKW9E9EPJYC3KMM,cn_01M82AG9DZ4Q7M3Z8RX016AKWJ,cn_01M82AK1Z8YRQBGAGXAECRMD6W,cn_01M82AC66KMJH32E2MQ3Z7ZBKS,cn_01M82ACZDNRYXG7FZCA8KC7FD4,cn_01M82AC66KMJH32E2MQ3Z7ZBKT,cn_01M82AJ8HWH90DHFSC2JB20DG2,cn_01M82AE56ZYS5Y2Z0C35ECC9Y8,cn_01M82AKNKGVB3WQ6AJ3QXNT528,cn_01M82AM9P6EWS5D1VJCAH8Z7VE,cn_01M82AHPS6SQKW9E9EPJYC3KMT draft
```

### Other concepts

```mermaid
flowchart TB
    classDef draft stroke-dasharray: 5 5
    cn_01M82AK1Z9HNB4ZNT1JN5CCR6R["safe chew toy"]
    cn_01M82AKNKGVB3WQ6AJ3QXNT526["safety harness"]
    cn_01M82AKNKGVB3WQ6AJ3QXNT527["seat belt"]
    cn_01M82AH1GXVV72WP99JQXMH6XP["small breed"]
    cn_01M82AK1Z9HNB4ZNT1JN5CCR6T["step-by-step alone training"]
    cn_01M82AM9P6EWS5D1VJCAH8Z7VA["third-party liability insurance"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKQ["training"]
    cn_01M82AJ8HWH90DHFSC2JB20DFX["training session"]
    cn_01M82AKNKGVB3WQ6AJ3QXNT52B["travel abroad"]
    cn_01M82AHPS6SQKW9E9EPJYC3KMS["unwanted behaviour"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9YB["veterinarian"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKR["veterinary care"]
    cn_01M82AFTZDSHCD0SK6T4N2YZWA["walk"]
    cn_01M82AH1GXVV72WP99JQXMH6XT["waste bin"]
    cn_01M82AH1GXVV72WP99JQXMH6XR["working breed"]
    class cn_01M82AK1Z9HNB4ZNT1JN5CCR6R,cn_01M82AKNKGVB3WQ6AJ3QXNT526,cn_01M82AKNKGVB3WQ6AJ3QXNT527,cn_01M82AH1GXVV72WP99JQXMH6XP,cn_01M82AK1Z9HNB4ZNT1JN5CCR6T,cn_01M82AM9P6EWS5D1VJCAH8Z7VA,cn_01M82AC66KMJH32E2MQ3Z7ZBKQ,cn_01M82AJ8HWH90DHFSC2JB20DFX,cn_01M82AKNKGVB3WQ6AJ3QXNT52B,cn_01M82AHPS6SQKW9E9EPJYC3KMS,cn_01M82AE56ZYS5Y2Z0C35ECC9YB,cn_01M82AC66KMJH32E2MQ3Z7ZBKR,cn_01M82AFTZDSHCD0SK6T4N2YZWA,cn_01M82AH1GXVV72WP99JQXMH6XT,cn_01M82AH1GXVV72WP99JQXMH6XR draft
```

## Concepts and relations

### Relations under barking or howling

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AK1Z9HNB4ZNT1JN5CCR6S["barking or howling"]
    cn_01M82AK1Z9HNB4ZNT1JN5CCR6T["step-by-step alone training"]
    cn_01M82AK1Z9HNB4ZNT1JN5CCR6S -. "is addressed by" .-> cn_01M82AK1Z9HNB4ZNT1JN5CCR6T
    class cn_01M82AK1Z9HNB4ZNT1JN5CCR6S,cn_01M82AK1Z9HNB4ZNT1JN5CCR6T draft
```

### Relations under breed

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82ACZDNRYXG7FZCA8KC7FD7["exercise"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD5["flat"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD6["grooming"]
    cn_01M82ACZDNRYXG7FZCA8KC7FCZ["large and working breed"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD0["long-haired breed"]
    cn_01M82ACZDNRYXG7FZCA8KC7FCY["small companion breed"]
    cn_01M82ACZDNRYXG7FZCA8KC7FCY -. "adapts well to" .-> cn_01M82ACZDNRYXG7FZCA8KC7FD5
    cn_01M82ACZDNRYXG7FZCA8KC7FCY -. "needs less" .-> cn_01M82ACZDNRYXG7FZCA8KC7FD7
    cn_01M82ACZDNRYXG7FZCA8KC7FCZ -. "needs more" .-> cn_01M82ACZDNRYXG7FZCA8KC7FD7
    cn_01M82ACZDNRYXG7FZCA8KC7FD0 -. "needs more" .-> cn_01M82ACZDNRYXG7FZCA8KC7FD6
    class cn_01M82ACZDNRYXG7FZCA8KC7FD7,cn_01M82ACZDNRYXG7FZCA8KC7FD5,cn_01M82ACZDNRYXG7FZCA8KC7FD6,cn_01M82ACZDNRYXG7FZCA8KC7FCZ,cn_01M82ACZDNRYXG7FZCA8KC7FD0,cn_01M82ACZDNRYXG7FZCA8KC7FCY draft
```

### Relations under dog

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82ADJQKNCFSCKCDMA3H0R86["adult dog"]
    cn_01M82AJ8HWH90DHFSC2JB20DFW["basic command"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9YC["check-up"]
    cn_01M82AEQW4JVCNX0WEDNNR61W4["claw"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKP["company"]
    cn_01M82AKNKGVB3WQ6AJ3QXNT525["crate"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKN["daily exercise"]
    cn_01M82AM9P6EWS5D1VJCAH8Z7VF["damage"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD2["dangerous breed"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM["dog"]
    cn_01M82AEQW4JVCNX0WEDNNR61W5["dog bed"]
    cn_01M82AJ8HWH90DHFSC2JB20DG1["dog of a dangerous breed"]
    cn_01M82ADJQKNCFSCKCDMA3H0R88["feeding"]
    cn_01M82AF7YTEGBGGS9B245D10JM["house training"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW6["leash"]
    cn_01M82AG9DZ4Q7M3Z8RX016AKWJ["leash training"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKS["local authority"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKT["microchip"]
    cn_01M82AF7YTEGBGGS9B245D10JK["mother"]
    cn_01M82AJ8HWH90DHFSC2JB20DG2["obedience test"]
    cn_01M82AF7YTEGBGGS9B245D10JJ["puppy"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9YA["rabies vaccination"]
    cn_01M82AKNKGVB3WQ6AJ3QXNT526["safety harness"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKQ["training"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y9["vaccination"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKR["veterinary care"]
    cn_01M82AFTZDSHCD0SK6T4N2YZWA["walk"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "needs" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKN
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "needs" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKP
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "needs" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKQ
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "needs" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKR
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "is registered with" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKS
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "carries" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKT
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "receives" .-> cn_01M82AE56ZYS5Y2Z0C35ECC9YA
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "has" .-> cn_01M82AE56ZYS5Y2Z0C35ECC9YC
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "has" .-> cn_01M82AEQW4JVCNX0WEDNNR61W4
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "has" .-> cn_01M82AEQW4JVCNX0WEDNNR61W5
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "is kept on" .-> cn_01M82AFTZDSHCD0SK6T4N2YZW6
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "should learn" .-> cn_01M82AJ8HWH90DHFSC2JB20DFW
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "travels in" .-> cn_01M82AKNKGVB3WQ6AJ3QXNT525
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "wears" .-> cn_01M82AKNKGVB3WQ6AJ3QXNT526
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "causes" .-> cn_01M82AM9P6EWS5D1VJCAH8Z7VF
    cn_01M82ADJQKNCFSCKCDMA3H0R86 -. "is fed times per day" .-> cn_01M82ADJQKNCFSCKCDMA3H0R88
    cn_01M82ADJQKNCFSCKCDMA3H0R86 -. "needs" .-> cn_01M82AFTZDSHCD0SK6T4N2YZWA
    cn_01M82AF7YTEGBGGS9B245D10JJ -. "is fed times per day" .-> cn_01M82ADJQKNCFSCKCDMA3H0R88
    cn_01M82AF7YTEGBGGS9B245D10JJ -. "receives" .-> cn_01M82AE56ZYS5Y2Z0C35ECC9Y9
    cn_01M82AF7YTEGBGGS9B245D10JJ -. "should not leave before 8 weeks" .-> cn_01M82AF7YTEGBGGS9B245D10JK
    cn_01M82AF7YTEGBGGS9B245D10JJ -. "undergoes" .-> cn_01M82AF7YTEGBGGS9B245D10JM
    cn_01M82AF7YTEGBGGS9B245D10JJ -. "undergoes" .-> cn_01M82AG9DZ4Q7M3Z8RX016AKWJ
    cn_01M82AJ8HWH90DHFSC2JB20DG1 -. "belongs to" .-> cn_01M82ACZDNRYXG7FZCA8KC7FD2
    cn_01M82AJ8HWH90DHFSC2JB20DG1 -. "must pass" .-> cn_01M82AJ8HWH90DHFSC2JB20DG2
    class cn_01M82ADJQKNCFSCKCDMA3H0R86,cn_01M82AJ8HWH90DHFSC2JB20DFW,cn_01M82AE56ZYS5Y2Z0C35ECC9YC,cn_01M82AEQW4JVCNX0WEDNNR61W4,cn_01M82AC66KMJH32E2MQ3Z7ZBKP,cn_01M82AKNKGVB3WQ6AJ3QXNT525,cn_01M82AC66KMJH32E2MQ3Z7ZBKN,cn_01M82AM9P6EWS5D1VJCAH8Z7VF,cn_01M82ACZDNRYXG7FZCA8KC7FD2,cn_01M82AC66KMJH32E2MQ3Z7ZBKM,cn_01M82AEQW4JVCNX0WEDNNR61W5,cn_01M82AJ8HWH90DHFSC2JB20DG1,cn_01M82ADJQKNCFSCKCDMA3H0R88,cn_01M82AF7YTEGBGGS9B245D10JM,cn_01M82AFTZDSHCD0SK6T4N2YZW6,cn_01M82AG9DZ4Q7M3Z8RX016AKWJ,cn_01M82AC66KMJH32E2MQ3Z7ZBKS,cn_01M82AC66KMJH32E2MQ3Z7ZBKT,cn_01M82AF7YTEGBGGS9B245D10JK,cn_01M82AJ8HWH90DHFSC2JB20DG2,cn_01M82AF7YTEGBGGS9B245D10JJ,cn_01M82AE56ZYS5Y2Z0C35ECC9YA,cn_01M82AKNKGVB3WQ6AJ3QXNT526,cn_01M82AC66KMJH32E2MQ3Z7ZBKQ,cn_01M82AE56ZYS5Y2Z0C35ECC9Y9,cn_01M82AC66KMJH32E2MQ3Z7ZBKR,cn_01M82AFTZDSHCD0SK6T4N2YZWA draft
```

### Relations under dog training course

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AJ8HWH90DHFSC2JB20DFZ["certified trainer"]
    cn_01M82AJ8HWH90DHFSC2JB20DFY["dog training course"]
    cn_01M82AJ8HWH90DHFSC2JB20DFY -. "is given by" .-> cn_01M82AJ8HWH90DHFSC2JB20DFZ
    class cn_01M82AJ8HWH90DHFSC2JB20DFZ,cn_01M82AJ8HWH90DHFSC2JB20DFY draft
```

### Relations under dog waste

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AH1GXVV72WP99JQXMH6XS["dog waste"]
    cn_01M82AH1GXVV72WP99JQXMH6XT["waste bin"]
    cn_01M82AH1GXVV72WP99JQXMH6XS -. "is put in" .-> cn_01M82AH1GXVV72WP99JQXMH6XT
    class cn_01M82AH1GXVV72WP99JQXMH6XS,cn_01M82AH1GXVV72WP99JQXMH6XT draft
```

### Relations under family

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AHPS6SQKW9E9EPJYC3KMN["command word"]
    cn_01M82AHPS6SQKW9E9EPJYC3KMP["family"]
    cn_01M82AHPS6SQKW9E9EPJYC3KMP -. "uses" .-> cn_01M82AHPS6SQKW9E9EPJYC3KMN
    class cn_01M82AHPS6SQKW9E9EPJYC3KMN,cn_01M82AHPS6SQKW9E9EPJYC3KMP draft
```

### Relations under food poisonous to dogs

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM["dog"]
    cn_01M82ADJQKNCFSCKCDMA3H0R8A["food poisonous to dogs"]
    cn_01M82ADJQKNCFSCKCDMA3H0R8A -. "is poisonous to" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKM
    class cn_01M82AC66KMJH32E2MQ3Z7ZBKM,cn_01M82ADJQKNCFSCKCDMA3H0R8A draft
```

### Relations under free-running sign

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AM9P6EWS5D1VJCAH8Z7VG["free-running sign"]
    cn_01M82AM9P6EWS5D1VJCAH8Z7VE["public place"]
    cn_01M82AM9P6EWS5D1VJCAH8Z7VG -. "is located in" .-> cn_01M82AM9P6EWS5D1VJCAH8Z7VE
    class cn_01M82AM9P6EWS5D1VJCAH8Z7VG,cn_01M82AM9P6EWS5D1VJCAH8Z7VE draft
```

### Relations under grooming

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AEQW4JVCNX0WEDNNR61W1["brushing"]
    cn_01M82AEQW4JVCNX0WEDNNR61W4["claw"]
    cn_01M82AEQW4JVCNX0WEDNNR61W2["claw trimming"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM["dog"]
    cn_01M82AEQW4JVCNX0WEDNNR61W1 -. "is applied to" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKM
    cn_01M82AEQW4JVCNX0WEDNNR61W2 -. "is applied to" .-> cn_01M82AEQW4JVCNX0WEDNNR61W4
    class cn_01M82AEQW4JVCNX0WEDNNR61W1,cn_01M82AEQW4JVCNX0WEDNNR61W4,cn_01M82AEQW4JVCNX0WEDNNR61W2,cn_01M82AC66KMJH32E2MQ3Z7ZBKM draft
```

### Relations under leash

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AFTZDSHCD0SK6T4N2YZWB["busy street"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW8["collar"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW9["harness"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW6["leash"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW7["retractable leash"]
    cn_01M82AFTZDSHCD0SK6T4N2YZWA["walk"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW6 -. "is attached to" .-> cn_01M82AFTZDSHCD0SK6T4N2YZW8
    cn_01M82AFTZDSHCD0SK6T4N2YZW6 -. "is attached to" .-> cn_01M82AFTZDSHCD0SK6T4N2YZW9
    cn_01M82AFTZDSHCD0SK6T4N2YZW6 -. "is used for" .-> cn_01M82AFTZDSHCD0SK6T4N2YZWA
    cn_01M82AFTZDSHCD0SK6T4N2YZW7 -. "is not suitable in" .-> cn_01M82AFTZDSHCD0SK6T4N2YZWB
    class cn_01M82AFTZDSHCD0SK6T4N2YZWB,cn_01M82AFTZDSHCD0SK6T4N2YZW8,cn_01M82AFTZDSHCD0SK6T4N2YZW9,cn_01M82AFTZDSHCD0SK6T4N2YZW6,cn_01M82AFTZDSHCD0SK6T4N2YZW7,cn_01M82AFTZDSHCD0SK6T4N2YZWA draft
```

### Relations under leash training

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AFTZDSHCD0SK6T4N2YZW6["leash"]
    cn_01M82AG9DZ4Q7M3Z8RX016AKWJ["leash training"]
    cn_01M82AG9DZ4Q7M3Z8RX016AKWJ -. "uses" .-> cn_01M82AFTZDSHCD0SK6T4N2YZW6
    class cn_01M82AFTZDSHCD0SK6T4N2YZW6,cn_01M82AG9DZ4Q7M3Z8RX016AKWJ draft
```

### Relations under local authority

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82ACZDNRYXG7FZCA8KC7FD2["dangerous breed"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKS["local authority"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKS -. "classifies as dangerous" .-> cn_01M82ACZDNRYXG7FZCA8KC7FD2
    cn_01M82AC66KMJH32E2MQ3Z7ZBKS -. "classifies as dangerous" .-> cn_01M82ACZDNRYXG7FZCA8KC7FD2
    class cn_01M82ACZDNRYXG7FZCA8KC7FD2,cn_01M82AC66KMJH32E2MQ3Z7ZBKS draft
```

### Relations under local list of dangerous breeds

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82ACZDNRYXG7FZCA8KC7FD2["dangerous breed"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD4["local list of dangerous breeds"]
    cn_01M82ACZDNRYXG7FZCA8KC7FD4 -. "lists" .-> cn_01M82ACZDNRYXG7FZCA8KC7FD2
    class cn_01M82ACZDNRYXG7FZCA8KC7FD2,cn_01M82ACZDNRYXG7FZCA8KC7FD4 draft
```

### Relations under owner

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AM9P6EWS5D1VJCAH8Z7VF["damage"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM["dog"]
    cn_01M82AH1GXVV72WP99JQXMH6XS["dog waste"]
    cn_01M82ADJQKNCFSCKCDMA3H0R89["fresh water"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8["owner"]
    cn_01M82AK1Z9HNB4ZNT1JN5CCR6R["safe chew toy"]
    cn_01M82AM9P6EWS5D1VJCAH8Z7VA["third-party liability insurance"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9YB["veterinarian"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8 -. "is the lead of" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKM
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8 -. "leaves alone" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKM
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8 -. "walks before leaving" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKM
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8 -. "leaves for the dog" .-> cn_01M82ADJQKNCFSCKCDMA3H0R89
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8 -. "takes dog to" .-> cn_01M82AE56ZYS5Y2Z0C35ECC9YB
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8 -. "picks up" .-> cn_01M82AH1GXVV72WP99JQXMH6XS
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8 -. "leaves for the dog" .-> cn_01M82AK1Z9HNB4ZNT1JN5CCR6R
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8 -. "holds" .-> cn_01M82AM9P6EWS5D1VJCAH8Z7VA
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8 -. "is liable for" .-> cn_01M82AM9P6EWS5D1VJCAH8Z7VF
    class cn_01M82AM9P6EWS5D1VJCAH8Z7VF,cn_01M82AC66KMJH32E2MQ3Z7ZBKM,cn_01M82AH1GXVV72WP99JQXMH6XS,cn_01M82ADJQKNCFSCKCDMA3H0R89,cn_01M82AE56ZYS5Y2Z0C35ECC9Y8,cn_01M82AK1Z9HNB4ZNT1JN5CCR6R,cn_01M82AM9P6EWS5D1VJCAH8Z7VA,cn_01M82AE56ZYS5Y2Z0C35ECC9YB draft
```

### Relations under reward

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AHPS6SQKW9E9EPJYC3KMR["good behaviour"]
    cn_01M82AHPS6SQKW9E9EPJYC3KMT["reward"]
    cn_01M82AHPS6SQKW9E9EPJYC3KMT -. "is given for" .-> cn_01M82AHPS6SQKW9E9EPJYC3KMR
    class cn_01M82AHPS6SQKW9E9EPJYC3KMR,cn_01M82AHPS6SQKW9E9EPJYC3KMT draft
```

### Relations under safety harness

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AKNKGVB3WQ6AJ3QXNT526["safety harness"]
    cn_01M82AKNKGVB3WQ6AJ3QXNT527["seat belt"]
    cn_01M82AKNKGVB3WQ6AJ3QXNT526 -. "is attached to" .-> cn_01M82AKNKGVB3WQ6AJ3QXNT527
    class cn_01M82AKNKGVB3WQ6AJ3QXNT526,cn_01M82AKNKGVB3WQ6AJ3QXNT527 draft
```

### Relations under travel abroad

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AC66KMJH32E2MQ3Z7ZBKT["microchip"]
    cn_01M82AKNKGVB3WQ6AJ3QXNT528["pet passport"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9YA["rabies vaccination"]
    cn_01M82AKNKGVB3WQ6AJ3QXNT52B["travel abroad"]
    cn_01M82AKNKGVB3WQ6AJ3QXNT52B -. "requires" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKT
    cn_01M82AKNKGVB3WQ6AJ3QXNT52B -. "requires" .-> cn_01M82AE56ZYS5Y2Z0C35ECC9YA
    cn_01M82AKNKGVB3WQ6AJ3QXNT52B -. "requires" .-> cn_01M82AKNKGVB3WQ6AJ3QXNT528
    class cn_01M82AC66KMJH32E2MQ3Z7ZBKT,cn_01M82AKNKGVB3WQ6AJ3QXNT528,cn_01M82AE56ZYS5Y2Z0C35ECC9YA,cn_01M82AKNKGVB3WQ6AJ3QXNT52B draft
```

## Concepts

<a id="cn_01M82ADJQKNCFSCKCDMA3H0R86"></a>
### adult dog · ● proposed

- **Is a:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM)
- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH), [§15](#su_01M82ABDR28HTPAFF4C44FRBZG), [§23](#su_01M82ABDR30PE47ZK8WSGY3HX2)

<a id="cn_01M82AK1Z9HNB4ZNT1JN5CCR6S"></a>
### barking or howling · ● proposed

- **Synonyms:** barks or howls
- **Level:** 3
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="cn_01M82AJ8HWH90DHFSC2JB20DFW"></a>
### basic command · ● proposed

- **Level:** 2
- **Evidence:** [§21](#su_01M82ABDR28HTPAFF4C44FRBZR)

<a id="cn_01M82AEQW4JVCNX0WEDNNR61W6"></a>
### blanket · ● proposed

- **Synonyms:** blankets
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="cn_01M82ACZDNRYXG7FZCA8KC7FCX"></a>
### breed · ● proposed

- **Level:** 2
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHBB), [§7](#su_01M82ABDR1CAX5PFZ2HWSEQHBF)

<a id="cn_01M82AEQW4JVCNX0WEDNNR61W1"></a>
### brushing · ● proposed

- **Is a:** [grooming](#cn_01M82ACZDNRYXG7FZCA8KC7FD6)
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="cn_01M82AFTZDSHCD0SK6T4N2YZWB"></a>
### busy street · ● proposed

- **Synonyms:** busy streets
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="cn_01M82AKNKGVB3WQ6AJ3QXNT524"></a>
### car · ● proposed

- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="cn_01M82AJ8HWH90DHFSC2JB20DFZ"></a>
### certified trainer · ● proposed

- **Level:** 2
- **Evidence:** [§22](#su_01M82ABDR28HTPAFF4C44FRBZS)

<a id="cn_01M82AE56ZYS5Y2Z0C35ECC9YC"></a>
### check-up · ● proposed

- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="cn_01M82ADJQKNCFSCKCDMA3H0R8B"></a>
### chocolate · ● proposed

- **Is a:** [food poisonous to dogs](#cn_01M82ADJQKNCFSCKCDMA3H0R8A)
- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="cn_01M82AEQW4JVCNX0WEDNNR61W4"></a>
### claw · ● proposed

- **Synonyms:** claws
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="cn_01M82AEQW4JVCNX0WEDNNR61W2"></a>
### claw trimming · ● proposed

- **Is a:** [grooming](#cn_01M82ACZDNRYXG7FZCA8KC7FD6)
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="cn_01M82AFTZDSHCD0SK6T4N2YZW8"></a>
### collar · ● proposed

- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="cn_01M82AHPS6SQKW9E9EPJYC3KMN"></a>
### command word · ● proposed

- **Level:** 2
- **Evidence:** [§17](#su_01M82ABDR28HTPAFF4C44FRBZK)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKP"></a>
### company · ● proposed

- **Level:** 2
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="cn_01M82AKNKGVB3WQ6AJ3QXNT525"></a>
### crate · ● proposed

- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKN"></a>
### daily exercise · ● proposed

- **Level:** 2
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="cn_01M82AM9P6EWS5D1VJCAH8Z7VF"></a>
### damage · ● proposed

- **Level:** 2
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82ACZDNRYXG7FZCA8KC7FD2"></a>
### dangerous breed · ● proposed

A breed classified as dangerous by the local authority.

- **Synonyms:** breeds classified as dangerous, dangerous
- **Is a:** [breed](#cn_01M82ACZDNRYXG7FZCA8KC7FCX)
- **Level:** 3
- **Evidence:** [§7](#su_01M82ABDR1CAX5PFZ2HWSEQHBF), [§22](#su_01M82ABDR28HTPAFF4C44FRBZS), [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKM"></a>
### dog · ● proposed

A social animal.

- **Level:** 1
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8), [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9), [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH), [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK), [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN), [§11](#su_01M82ABDR28HTPAFF4C44FRBZ9), [§14](#su_01M82ABDR28HTPAFF4C44FRBZE), [§15](#su_01M82ABDR28HTPAFF4C44FRBZG), [§16](#su_01M82ABDR28HTPAFF4C44FRBZJ), [§20](#su_01M82ABDR28HTPAFF4C44FRBZP), [§21](#su_01M82ABDR28HTPAFF4C44FRBZR), [§22](#su_01M82ABDR28HTPAFF4C44FRBZS), [§23](#su_01M82ABDR30PE47ZK8WSGY3HX2), [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3), [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5), [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AEQW4JVCNX0WEDNNR61W5"></a>
### dog bed · ● proposed

- **Synonyms:** bed
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="cn_01M82AJ8HWH90DHFSC2JB20DG1"></a>
### dog of a dangerous breed · ● proposed

- **Is a:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM)
- **Level:** 3
- **Evidence:** [§22](#su_01M82ABDR28HTPAFF4C44FRBZS)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKV"></a>
### dog registration · ● proposed

- **Synonyms:** registered
- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="cn_01M82AJ8HWH90DHFSC2JB20DFY"></a>
### dog training course · ● proposed

- **Level:** 2
- **Evidence:** [§22](#su_01M82ABDR28HTPAFF4C44FRBZS)

<a id="cn_01M82AH1GXVV72WP99JQXMH6XS"></a>
### dog waste · ● proposed

- **Synonyms:** waste
- **Level:** 1
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="cn_01M82ACZDNRYXG7FZCA8KC7FD7"></a>
### exercise · ● proposed

- **Level:** 2
- **Evidence:** [§4](#su_01M82ABDR1CAX5PFZ2HWSEQHBC), [§5](#su_01M82ABDR1CAX5PFZ2HWSEQHBD)

<a id="cn_01M82AHPS6SQKW9E9EPJYC3KMP"></a>
### family · ● proposed

- **Level:** 2
- **Evidence:** [§17](#su_01M82ABDR28HTPAFF4C44FRBZK)

<a id="cn_01M82ADJQKNCFSCKCDMA3H0R88"></a>
### feeding · ● proposed

- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="cn_01M82ACZDNRYXG7FZCA8KC7FD5"></a>
### flat · ● proposed

- **Synonyms:** flats
- **Level:** 2
- **Evidence:** [§4](#su_01M82ABDR1CAX5PFZ2HWSEQHBC)

<a id="cn_01M82ADJQKNCFSCKCDMA3H0R8A"></a>
### food poisonous to dogs · ● proposed

- **Synonyms:** poisonous
- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="cn_01M82AM9P6EWS5D1VJCAH8Z7VG"></a>
### free-running sign · ● proposed

- **Synonyms:** sign allowing free running
- **Level:** 2
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82ADJQKNCFSCKCDMA3H0R89"></a>
### fresh water · ● proposed

- **Synonyms:** water
- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH), [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="cn_01M82AHPS6SQKW9E9EPJYC3KMR"></a>
### good behaviour · ● proposed

- **Level:** 2
- **Evidence:** [§19](#su_01M82ABDR28HTPAFF4C44FRBZN)

<a id="cn_01M82ADJQKNCFSCKCDMA3H0R8C"></a>
### grape · ● proposed

- **Synonyms:** grapes
- **Is a:** [food poisonous to dogs](#cn_01M82ADJQKNCFSCKCDMA3H0R8A)
- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="cn_01M82ACZDNRYXG7FZCA8KC7FD6"></a>
### grooming · ● proposed

- **Level:** 2
- **Evidence:** [§6](#su_01M82ABDR1CAX5PFZ2HWSEQHBE), [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="cn_01M82AFTZDSHCD0SK6T4N2YZW9"></a>
### harness · ● proposed

- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="cn_01M82AF7YTEGBGGS9B245D10JM"></a>
### house training · ● proposed

- **Level:** 3
- **Evidence:** [§12](#su_01M82ABDR28HTPAFF4C44FRBZA)

<a id="cn_01M82AHPS6SQKW9E9EPJYC3KMQ"></a>
### household rule for the dog · ● proposed

- **Level:** 2
- **Evidence:** [§18](#su_01M82ABDR28HTPAFF4C44FRBZM)

<a id="cn_01M82ACZDNRYXG7FZCA8KC7FCZ"></a>
### large and working breed · ● proposed

- **Synonyms:** large and working breeds
- **Is a:** [breed](#cn_01M82ACZDNRYXG7FZCA8KC7FCX)
- **Level:** 2
- **Evidence:** [§5](#su_01M82ABDR1CAX5PFZ2HWSEQHBD)

<a id="cn_01M82AH1GXVV72WP99JQXMH6XQ"></a>
### large breed · ● proposed

- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="cn_01M82AHPS6SQKW9E9EPJYC3KMM"></a>
### lead (leader) · ● proposed

A calm, consistent and confident leader whose signals the dog can trust.

- **Level:** 2
- **Evidence:** [§16](#su_01M82ABDR28HTPAFF4C44FRBZJ), [§20](#su_01M82ABDR28HTPAFF4C44FRBZP)

<a id="cn_01M82AFTZDSHCD0SK6T4N2YZW6"></a>
### leash · ● proposed

- **Level:** 1
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC), [§14](#su_01M82ABDR28HTPAFF4C44FRBZE), [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AG9DZ4Q7M3Z8RX016AKWJ"></a>
### leash training · ● proposed

- **Level:** 2
- **Evidence:** [§14](#su_01M82ABDR28HTPAFF4C44FRBZE)

<a id="cn_01M82AK1Z8YRQBGAGXAECRMD6W"></a>
### leaving the dog alone · ● proposed

- **Level:** 2
- **Evidence:** [§23](#su_01M82ABDR30PE47ZK8WSGY3HX2), [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKS"></a>
### local authority · ● proposed

- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9), [§7](#su_01M82ABDR1CAX5PFZ2HWSEQHBF), [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82ACZDNRYXG7FZCA8KC7FD4"></a>
### local list of dangerous breeds · ● proposed

- **Synonyms:** local list
- **Level:** 3
- **Evidence:** [§7](#su_01M82ABDR1CAX5PFZ2HWSEQHBF)

<a id="cn_01M82ACZDNRYXG7FZCA8KC7FD0"></a>
### long-haired breed · ● proposed

- **Synonyms:** long-haired breeds
- **Is a:** [breed](#cn_01M82ACZDNRYXG7FZCA8KC7FCX)
- **Level:** 2
- **Evidence:** [§6](#su_01M82ABDR1CAX5PFZ2HWSEQHBE), [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKT"></a>
### microchip · ● proposed

- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9), [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="cn_01M82AF7YTEGBGGS9B245D10JK"></a>
### mother · ● proposed

- **Is a:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM)
- **Level:** 3
- **Evidence:** [§11](#su_01M82ABDR28HTPAFF4C44FRBZ9)

<a id="cn_01M82AJ8HWH90DHFSC2JB20DG2"></a>
### obedience test · ● proposed

- **Level:** 3
- **Evidence:** [§22](#su_01M82ABDR28HTPAFF4C44FRBZS)

<a id="cn_01M82ADJQKNCFSCKCDMA3H0R8D"></a>
### onion · ● proposed

- **Synonyms:** onions
- **Is a:** [food poisonous to dogs](#cn_01M82ADJQKNCFSCKCDMA3H0R8A)
- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="cn_01M82AE56ZYS5Y2Z0C35ECC9Y8"></a>
### owner · ● proposed

- **Synonyms:** dog owner
- **Level:** 1
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK), [§15](#su_01M82ABDR28HTPAFF4C44FRBZG), [§20](#su_01M82ABDR28HTPAFF4C44FRBZP), [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3), [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AKNKGVB3WQ6AJ3QXNT528"></a>
### pet passport · ● proposed

- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="cn_01M82AM9P6EWS5D1VJCAH8Z7VE"></a>
### public place · ● proposed

- **Level:** 2
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AF7YTEGBGGS9B245D10JJ"></a>
### puppy · ● proposed

A dog younger than 6 months.

- **Is a:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM)
- **Level:** 3
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH), [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK), [§11](#su_01M82ABDR28HTPAFF4C44FRBZ9), [§12](#su_01M82ABDR28HTPAFF4C44FRBZA), [§14](#su_01M82ABDR28HTPAFF4C44FRBZE), [§15](#su_01M82ABDR28HTPAFF4C44FRBZG), [§23](#su_01M82ABDR30PE47ZK8WSGY3HX2)

<a id="cn_01M82AE56ZYS5Y2Z0C35ECC9YA"></a>
### rabies vaccination · ● proposed

- **Is a:** [vaccination](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y9)
- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK), [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="cn_01M82AFTZDSHCD0SK6T4N2YZW7"></a>
### retractable leash · ● proposed

- **Is a:** [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6)
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="cn_01M82AHPS6SQKW9E9EPJYC3KMT"></a>
### reward · ● proposed

- **Level:** 2
- **Evidence:** [§19](#su_01M82ABDR28HTPAFF4C44FRBZN)

<a id="cn_01M82AK1Z9HNB4ZNT1JN5CCR6R"></a>
### safe chew toy · ● proposed

- **Synonyms:** chew toy
- **Level:** 2
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="cn_01M82AKNKGVB3WQ6AJ3QXNT526"></a>
### safety harness · ● proposed

- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="cn_01M82AKNKGVB3WQ6AJ3QXNT527"></a>
### seat belt · ● proposed

- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="cn_01M82ACZDNRYXG7FZCA8KC7FD1"></a>
### short-haired breed · ● proposed

- **Synonyms:** short-haired breeds
- **Is a:** [breed](#cn_01M82ACZDNRYXG7FZCA8KC7FCX)
- **Level:** 2
- **Evidence:** [§6](#su_01M82ABDR1CAX5PFZ2HWSEQHBE)

<a id="cn_01M82AH1GXVV72WP99JQXMH6XP"></a>
### small breed · ● proposed

- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="cn_01M82ACZDNRYXG7FZCA8KC7FCY"></a>
### small companion breed · ● proposed

- **Synonyms:** small companion breeds
- **Is a:** [breed](#cn_01M82ACZDNRYXG7FZCA8KC7FCX)
- **Level:** 2
- **Evidence:** [§4](#su_01M82ABDR1CAX5PFZ2HWSEQHBC)

<a id="cn_01M82AK1Z9HNB4ZNT1JN5CCR6T"></a>
### step-by-step alone training · ● proposed

- **Synonyms:** train it to be alone
- **Level:** 3
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="cn_01M82AM9P6EWS5D1VJCAH8Z7VA"></a>
### third-party liability insurance · ● proposed

- **Level:** 2
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKQ"></a>
### training · ● proposed

- **Level:** 2
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="cn_01M82AJ8HWH90DHFSC2JB20DFX"></a>
### training session · ● proposed

- **Level:** 2
- **Evidence:** [§21](#su_01M82ABDR28HTPAFF4C44FRBZR)

<a id="cn_01M82AKNKGVB3WQ6AJ3QXNT52B"></a>
### travel abroad · ● proposed

- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="cn_01M82AHPS6SQKW9E9EPJYC3KMS"></a>
### unwanted behaviour · ● proposed

- **Level:** 2
- **Evidence:** [§19](#su_01M82ABDR28HTPAFF4C44FRBZN)

<a id="cn_01M82AE56ZYS5Y2Z0C35ECC9Y9"></a>
### vaccination · ● proposed

- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="cn_01M82AE56ZYS5Y2Z0C35ECC9YB"></a>
### veterinarian · ● proposed

- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKR"></a>
### veterinary care · ● proposed

- **Level:** 2
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="cn_01M82AFTZDSHCD0SK6T4N2YZWA"></a>
### walk · ● proposed

- **Synonyms:** everyday walks
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC), [§15](#su_01M82ABDR28HTPAFF4C44FRBZG), [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="cn_01M82AH1GXVV72WP99JQXMH6XT"></a>
### waste bin · ● proposed

- **Level:** 1
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="cn_01M82AH1GXVV72WP99JQXMH6XR"></a>
### working breed · ● proposed

- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="cn_01M82ADJQKNCFSCKCDMA3H0R8E"></a>
### xylitol · ● proposed

- **Is a:** [food poisonous to dogs](#cn_01M82ADJQKNCFSCKCDMA3H0R8A)
- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

## Relations

<a id="rl_01M82ACZDNRYXG7FZCA8KC7FDA"></a>
### adapts well to · ● proposed

- [small companion breed](#cn_01M82ACZDNRYXG7FZCA8KC7FCY) — adapts well to → [flat](#cn_01M82ACZDNRYXG7FZCA8KC7FD5)
- **Level:** 2
- **Evidence:** [§4](#su_01M82ABDR1CAX5PFZ2HWSEQHBC)

<a id="rl_01M82AJ8HWH90DHFSC2JB20DG5"></a>
### belongs to · ● proposed

- [dog of a dangerous breed](#cn_01M82AJ8HWH90DHFSC2JB20DG1) — belongs to → [dangerous breed](#cn_01M82ACZDNRYXG7FZCA8KC7FD2)
- **Level:** 3
- **Evidence:** [§22](#su_01M82ABDR28HTPAFF4C44FRBZS)

<a id="rl_01M82AC66KMJH32E2MQ3Z7ZBM1"></a>
### carries · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — carries → [microchip](#cn_01M82AC66KMJH32E2MQ3Z7ZBKT)
- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="rl_01M82AM9P6EWS5D1VJCAH8Z7VJ"></a>
### causes · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — causes → [damage](#cn_01M82AM9P6EWS5D1VJCAH8Z7VF)
- **Level:** 2
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="rl_01M82ACZDNRYXG7FZCA8KC7FD8"></a>
### classifies as dangerous · ● proposed

- [local authority](#cn_01M82AC66KMJH32E2MQ3Z7ZBKS) — classifies as dangerous → [dangerous breed](#cn_01M82ACZDNRYXG7FZCA8KC7FD2)
- **Level:** 3
- **Evidence:** [§7](#su_01M82ABDR1CAX5PFZ2HWSEQHBF)

<a id="rl_01M82AM9P6EWS5D1VJCAH8Z7VK"></a>
### classifies as dangerous · ● proposed

- [local authority](#cn_01M82AC66KMJH32E2MQ3Z7ZBKS) — classifies as dangerous → [dangerous breed](#cn_01M82ACZDNRYXG7FZCA8KC7FD2)
- **Level:** 3
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="rl_01M82AE56ZYS5Y2Z0C35ECC9YF"></a>
### has · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — has → [check-up](#cn_01M82AE56ZYS5Y2Z0C35ECC9YC)
- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="rl_01M82AEQW4JVCNX0WEDNNR61W7"></a>
### has · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — has → [claw](#cn_01M82AEQW4JVCNX0WEDNNR61W4)
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="rl_01M82AEQW4JVCNX0WEDNNR61WA"></a>
### has · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — has → [dog bed](#cn_01M82AEQW4JVCNX0WEDNNR61W5)
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="rl_01M82AM9P6EWS5D1VJCAH8Z7VP"></a>
### holds · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — holds → [third-party liability insurance](#cn_01M82AM9P6EWS5D1VJCAH8Z7VA)
- **Level:** 2
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="rl_01M82AK1Z9HNB4ZNT1JN5CCR6Z"></a>
### is addressed by · ● proposed

- [barking or howling](#cn_01M82AK1Z9HNB4ZNT1JN5CCR6S) — is addressed by → [step-by-step alone training](#cn_01M82AK1Z9HNB4ZNT1JN5CCR6T)
- **Level:** 3
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="rl_01M82AEQW4JVCNX0WEDNNR61W8"></a>
### is applied to · ● proposed

- [claw trimming](#cn_01M82AEQW4JVCNX0WEDNNR61W2) — is applied to → [claw](#cn_01M82AEQW4JVCNX0WEDNNR61W4)
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="rl_01M82AEQW4JVCNX0WEDNNR61W9"></a>
### is applied to · ● proposed

- [brushing](#cn_01M82AEQW4JVCNX0WEDNNR61W1) — is applied to → [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM)
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="rl_01M82AFTZDSHCD0SK6T4N2YZWC"></a>
### is attached to · ● proposed

- [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6) — is attached to → [collar](#cn_01M82AFTZDSHCD0SK6T4N2YZW8)
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="rl_01M82AFTZDSHCD0SK6T4N2YZWD"></a>
### is attached to · ● proposed

- [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6) — is attached to → [harness](#cn_01M82AFTZDSHCD0SK6T4N2YZW9)
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="rl_01M82AKNKGVB3WQ6AJ3QXNT52E"></a>
### is attached to · ● proposed

- [safety harness](#cn_01M82AKNKGVB3WQ6AJ3QXNT526) — is attached to → [seat belt](#cn_01M82AKNKGVB3WQ6AJ3QXNT527)
- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="rl_01M82ADJQKNCFSCKCDMA3H0R8G"></a>
### is fed times per day · ● proposed

- [adult dog](#cn_01M82ADJQKNCFSCKCDMA3H0R86) — is fed times per day → [feeding](#cn_01M82ADJQKNCFSCKCDMA3H0R88)
- **Cardinality:** at least 2, at most 2
- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="rl_01M82ADJQKNCFSCKCDMA3H0R8H"></a>
### is fed times per day · ● proposed

- [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ) — is fed times per day → [feeding](#cn_01M82ADJQKNCFSCKCDMA3H0R88)
- **Cardinality:** at least 3, at most 4
- **Level:** 3
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="rl_01M82AJ8HWH90DHFSC2JB20DG4"></a>
### is given by · ● proposed

- [dog training course](#cn_01M82AJ8HWH90DHFSC2JB20DFY) — is given by → [certified trainer](#cn_01M82AJ8HWH90DHFSC2JB20DFZ)
- **Level:** 2
- **Evidence:** [§22](#su_01M82ABDR28HTPAFF4C44FRBZS)

<a id="rl_01M82AHPS6SQKW9E9EPJYC3KMX"></a>
### is given for · ● proposed

- [reward](#cn_01M82AHPS6SQKW9E9EPJYC3KMT) — is given for → [good behaviour](#cn_01M82AHPS6SQKW9E9EPJYC3KMR)
- **Level:** 2
- **Evidence:** [§19](#su_01M82ABDR28HTPAFF4C44FRBZN)

<a id="rl_01M82AM9P6EWS5D1VJCAH8Z7VM"></a>
### is kept on · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — is kept on → [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6)
- **Level:** 1
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="rl_01M82AM9P6EWS5D1VJCAH8Z7VH"></a>
### is liable for · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — is liable for → [damage](#cn_01M82AM9P6EWS5D1VJCAH8Z7VF)
- **Level:** 1
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="rl_01M82AM9P6EWS5D1VJCAH8Z7VN"></a>
### is located in · ● proposed

- [free-running sign](#cn_01M82AM9P6EWS5D1VJCAH8Z7VG) — is located in → [public place](#cn_01M82AM9P6EWS5D1VJCAH8Z7VE)
- **Level:** 2
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="rl_01M82AFTZDSHCD0SK6T4N2YZWF"></a>
### is not suitable in · ● proposed

- [retractable leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW7) — is not suitable in → [busy street](#cn_01M82AFTZDSHCD0SK6T4N2YZWB)
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="rl_01M82ADJQKNCFSCKCDMA3H0R8F"></a>
### is poisonous to · ● proposed

- [food poisonous to dogs](#cn_01M82ADJQKNCFSCKCDMA3H0R8A) — is poisonous to → [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM)
- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="rl_01M82AH1GXVV72WP99JQXMH6XY"></a>
### is put in · ● proposed

- [dog waste](#cn_01M82AH1GXVV72WP99JQXMH6XS) — is put in → [waste bin](#cn_01M82AH1GXVV72WP99JQXMH6XT)
- **Level:** 1
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="rl_01M82AC66KMJH32E2MQ3Z7ZBM0"></a>
### is registered with · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — is registered with → [local authority](#cn_01M82AC66KMJH32E2MQ3Z7ZBKS)
- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="rl_01M82AHPS6SQKW9E9EPJYC3KMV"></a>
### is the lead of · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — is the lead of → [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM)
- **Level:** 2
- **Evidence:** [§16](#su_01M82ABDR28HTPAFF4C44FRBZJ), [§20](#su_01M82ABDR28HTPAFF4C44FRBZP)

<a id="rl_01M82AFTZDSHCD0SK6T4N2YZWE"></a>
### is used for · ● proposed

- [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6) — is used for → [walk](#cn_01M82AFTZDSHCD0SK6T4N2YZWA)
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="rl_01M82AK1Z9HNB4ZNT1JN5CCR6V"></a>
### leaves alone · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — leaves alone → [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM)
- **Level:** 2
- **Evidence:** [§23](#su_01M82ABDR30PE47ZK8WSGY3HX2), [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="rl_01M82AK1Z9HNB4ZNT1JN5CCR6X"></a>
### leaves for the dog · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — leaves for the dog → [fresh water](#cn_01M82ADJQKNCFSCKCDMA3H0R89)
- **Level:** 2
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="rl_01M82AK1Z9HNB4ZNT1JN5CCR6Y"></a>
### leaves for the dog · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — leaves for the dog → [safe chew toy](#cn_01M82AK1Z9HNB4ZNT1JN5CCR6R)
- **Level:** 2
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="rl_01M82ACZDNRYXG7FZCA8KC7FD9"></a>
### lists · ● proposed

- [local list of dangerous breeds](#cn_01M82ACZDNRYXG7FZCA8KC7FD4) — lists → [dangerous breed](#cn_01M82ACZDNRYXG7FZCA8KC7FD2)
- **Level:** 3
- **Evidence:** [§7](#su_01M82ABDR1CAX5PFZ2HWSEQHBF)

<a id="rl_01M82AJ8HWH90DHFSC2JB20DG6"></a>
### must pass · ● proposed

- [dog of a dangerous breed](#cn_01M82AJ8HWH90DHFSC2JB20DG1) — must pass → [obedience test](#cn_01M82AJ8HWH90DHFSC2JB20DG2)
- **Level:** 3
- **Evidence:** [§22](#su_01M82ABDR28HTPAFF4C44FRBZS)

<a id="rl_01M82AC66KMJH32E2MQ3Z7ZBKW"></a>
### needs · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — needs → [daily exercise](#cn_01M82AC66KMJH32E2MQ3Z7ZBKN)
- **Level:** 2
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="rl_01M82AC66KMJH32E2MQ3Z7ZBKX"></a>
### needs · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — needs → [company](#cn_01M82AC66KMJH32E2MQ3Z7ZBKP)
- **Level:** 2
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="rl_01M82AC66KMJH32E2MQ3Z7ZBKY"></a>
### needs · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — needs → [training](#cn_01M82AC66KMJH32E2MQ3Z7ZBKQ)
- **Level:** 2
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="rl_01M82AC66KMJH32E2MQ3Z7ZBKZ"></a>
### needs · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — needs → [veterinary care](#cn_01M82AC66KMJH32E2MQ3Z7ZBKR)
- **Level:** 2
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="rl_01M82AH1GXVV72WP99JQXMH6XW"></a>
### needs · ● proposed

- [adult dog](#cn_01M82ADJQKNCFSCKCDMA3H0R86) — needs → [walk](#cn_01M82AFTZDSHCD0SK6T4N2YZWA)
- **Cardinality:** at least 2
- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="rl_01M82ACZDNRYXG7FZCA8KC7FDD"></a>
### needs less · ● proposed

- [small companion breed](#cn_01M82ACZDNRYXG7FZCA8KC7FCY) — needs less → [exercise](#cn_01M82ACZDNRYXG7FZCA8KC7FD7)
- **Level:** 2
- **Evidence:** [§4](#su_01M82ABDR1CAX5PFZ2HWSEQHBC)

<a id="rl_01M82ACZDNRYXG7FZCA8KC7FDB"></a>
### needs more · ● proposed

- [long-haired breed](#cn_01M82ACZDNRYXG7FZCA8KC7FD0) — needs more → [grooming](#cn_01M82ACZDNRYXG7FZCA8KC7FD6)
- **Level:** 2
- **Evidence:** [§6](#su_01M82ABDR1CAX5PFZ2HWSEQHBE)

<a id="rl_01M82ACZDNRYXG7FZCA8KC7FDC"></a>
### needs more · ● proposed

- [large and working breed](#cn_01M82ACZDNRYXG7FZCA8KC7FCZ) — needs more → [exercise](#cn_01M82ACZDNRYXG7FZCA8KC7FD7)
- **Level:** 2
- **Evidence:** [§5](#su_01M82ABDR1CAX5PFZ2HWSEQHBD)

<a id="rl_01M82AH1GXVV72WP99JQXMH6XX"></a>
### picks up · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — picks up → [dog waste](#cn_01M82AH1GXVV72WP99JQXMH6XS)
- **Level:** 1
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="rl_01M82AE56ZYS5Y2Z0C35ECC9YD"></a>
### receives · ● proposed

- [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ) — receives → [vaccination](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y9)
- **Level:** 3
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="rl_01M82AE56ZYS5Y2Z0C35ECC9YG"></a>
### receives · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — receives → [rabies vaccination](#cn_01M82AE56ZYS5Y2Z0C35ECC9YA)
- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="rl_01M82AKNKHBHSK6HA7XAZBSVGS"></a>
### requires · ● proposed

- [travel abroad](#cn_01M82AKNKGVB3WQ6AJ3QXNT52B) — requires → [pet passport](#cn_01M82AKNKGVB3WQ6AJ3QXNT528)
- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="rl_01M82AKNKHBHSK6HA7XAZBSVGT"></a>
### requires · ● proposed

- [travel abroad](#cn_01M82AKNKGVB3WQ6AJ3QXNT52B) — requires → [microchip](#cn_01M82AC66KMJH32E2MQ3Z7ZBKT)
- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="rl_01M82AKNKHBHSK6HA7XAZBSVGV"></a>
### requires · ● proposed

- [travel abroad](#cn_01M82AKNKGVB3WQ6AJ3QXNT52B) — requires → [rabies vaccination](#cn_01M82AE56ZYS5Y2Z0C35ECC9YA)
- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="rl_01M82AJ8HWH90DHFSC2JB20DG3"></a>
### should learn · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — should learn → [basic command](#cn_01M82AJ8HWH90DHFSC2JB20DFW)
- **Cardinality:** at least 5, at most 5
- **Level:** 2
- **Evidence:** [§21](#su_01M82ABDR28HTPAFF4C44FRBZR)

<a id="rl_01M82AF7YTEGBGGS9B245D10JN"></a>
### should not leave before 8 weeks · ● proposed

- [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ) — should not leave before 8 weeks → [mother](#cn_01M82AF7YTEGBGGS9B245D10JK)
- **Level:** 3
- **Evidence:** [§11](#su_01M82ABDR28HTPAFF4C44FRBZ9)

<a id="rl_01M82AE56ZYS5Y2Z0C35ECC9YE"></a>
### takes dog to · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — takes dog to → [veterinarian](#cn_01M82AE56ZYS5Y2Z0C35ECC9YB)
- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="rl_01M82AKNKGVB3WQ6AJ3QXNT52C"></a>
### travels in · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — travels in → [crate](#cn_01M82AKNKGVB3WQ6AJ3QXNT525)
- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="rl_01M82AF7YTEGBGGS9B245D10JP"></a>
### undergoes · ● proposed

- [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ) — undergoes → [house training](#cn_01M82AF7YTEGBGGS9B245D10JM)
- **Level:** 3
- **Evidence:** [§12](#su_01M82ABDR28HTPAFF4C44FRBZA)

<a id="rl_01M82AG9DZ4Q7M3Z8RX016AKWP"></a>
### undergoes · ● proposed

- [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ) — undergoes → [leash training](#cn_01M82AG9DZ4Q7M3Z8RX016AKWJ)
- **Level:** 3
- **Evidence:** [§14](#su_01M82ABDR28HTPAFF4C44FRBZE)

<a id="rl_01M82AG9DZ4Q7M3Z8RX016AKWQ"></a>
### uses · ● proposed

- [leash training](#cn_01M82AG9DZ4Q7M3Z8RX016AKWJ) — uses → [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6)
- **Level:** 2
- **Evidence:** [§14](#su_01M82ABDR28HTPAFF4C44FRBZE)

<a id="rl_01M82AHPS6SQKW9E9EPJYC3KMW"></a>
### uses · ● proposed

- [family](#cn_01M82AHPS6SQKW9E9EPJYC3KMP) — uses → [command word](#cn_01M82AHPS6SQKW9E9EPJYC3KMN)
- **Level:** 2
- **Evidence:** [§17](#su_01M82ABDR28HTPAFF4C44FRBZK)

<a id="rl_01M82AK1Z9HNB4ZNT1JN5CCR6W"></a>
### walks before leaving · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — walks before leaving → [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM)
- **Level:** 2
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="rl_01M82AKNKGVB3WQ6AJ3QXNT52D"></a>
### wears · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — wears → [safety harness](#cn_01M82AKNKGVB3WQ6AJ3QXNT526)
- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

## Rules

<a id="ru_01M82AK1Z9HNB4ZNT1JN5CCR70"></a>
### Adult dog alone at most 6 hours · ● proposed

owner **must not** leave an adult dog alone at home for more than 6 hours

- **Limit:** ≤ 6 h
- **Refers to:** [adult dog](#cn_01M82ADJQKNCFSCKCDMA3H0R86), [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [leaving the dog alone](#cn_01M82AK1Z8YRQBGAGXAECRMD6W), [leaves alone](#rl_01M82AK1Z9HNB4ZNT1JN5CCR6V)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§23](#su_01M82ABDR30PE47ZK8WSGY3HX2)

<a id="ru_01M82AH1GXVV72WP99JQXMH6XZ"></a>
### Adult dog needs at least two walks a day · ● proposed

owner **must** take an adult dog for walks every day

- **When:** the dog is an adult dog
- **Limit:** ≥ 2 walks per day
- **Refers to:** [adult dog](#cn_01M82ADJQKNCFSCKCDMA3H0R86), [walk](#cn_01M82AFTZDSHCD0SK6T4N2YZWA), [needs](#rl_01M82AH1GXVV72WP99JQXMH6XW)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="ru_01M82AH1GXVV72WP99JQXMH6Y3"></a>
### Always pick up dog waste and put it in a waste bin · ● proposed

owner **must** always pick up the dog's waste and put it in a waste bin

- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [dog waste](#cn_01M82AH1GXVV72WP99JQXMH6XS), [waste bin](#cn_01M82AH1GXVV72WP99JQXMH6XT), [picks up](#rl_01M82AH1GXVV72WP99JQXMH6XX), [is put in](#rl_01M82AH1GXVV72WP99JQXMH6XY)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="ru_01M82AFTZDSHCD0SK6T4N2YZWK"></a>
### Attach leash to well-fitting collar or harness · ● proposed

dog owner **must** attach the leash to a well-fitting collar or harness

- **Refers to:** [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6), [collar](#cn_01M82AFTZDSHCD0SK6T4N2YZW8), [harness](#cn_01M82AFTZDSHCD0SK6T4N2YZW9), [is attached to](#rl_01M82AFTZDSHCD0SK6T4N2YZWC), [is attached to](#rl_01M82AFTZDSHCD0SK6T4N2YZWD)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="ru_01M82AEQW4JVCNX0WEDNNR61WB"></a>
### Brush dog at least once a week · ● proposed

dog owner **must** brush the dog at least once a week

- **Limit:** ≥ 1 times per week
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [brushing](#cn_01M82AEQW4JVCNX0WEDNNR61W1), [is applied to](#rl_01M82AEQW4JVCNX0WEDNNR61W9)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="ru_01M82AEQW4JVCNX0WEDNNR61WC"></a>
### Brush long-haired breeds daily · ● proposed

dog owner **must** brush the dog every day

- **When:** the dog is of a long-haired breed
- **Limit:** = 1 times per day
- **Refers to:** [long-haired breed](#cn_01M82ACZDNRYXG7FZCA8KC7FD0), [brushing](#cn_01M82AEQW4JVCNX0WEDNNR61W1)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="ru_01M82AC66KMJH32E2MQ3Z7ZBM2"></a>
### Check fit before getting a dog · ● proposed

person who wants to get a dog **must** check that their home, working hours and budget fit the dog they want

- **When:** before getting a dog
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="ru_01M82ACZDNRYXG7FZCA8KC7FDE"></a>
### Check the local list of dangerous breeds before choosing · ● proposed

person choosing a breed **must** check the local list of dangerous breeds

- **When:** before choosing a breed
- **Refers to:** [local authority](#cn_01M82AC66KMJH32E2MQ3Z7ZBKS), [dangerous breed](#cn_01M82ACZDNRYXG7FZCA8KC7FD2), [local list of dangerous breeds](#cn_01M82ACZDNRYXG7FZCA8KC7FD4), [classifies as dangerous](#rl_01M82ACZDNRYXG7FZCA8KC7FD8)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§7](#su_01M82ABDR1CAX5PFZ2HWSEQHBF)

<a id="ru_01M82AJ8HWH90DHFSC2JB20DGC"></a>
### Dangerous breeds must pass obedience test · ● proposed

dog of a dangerous breed **must** pass an obedience test

- **When:** the dog's breed is classified as dangerous
- **Refers to:** [dangerous breed](#cn_01M82ACZDNRYXG7FZCA8KC7FD2), [dog of a dangerous breed](#cn_01M82AJ8HWH90DHFSC2JB20DG1), [obedience test](#cn_01M82AJ8HWH90DHFSC2JB20DG2), [must pass](#rl_01M82AJ8HWH90DHFSC2JB20DG6)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§22](#su_01M82ABDR28HTPAFF4C44FRBZS)

<a id="ru_01M82AHPS6SQKW9E9EPJYC3KN3"></a>
### Do not shout at unwanted behaviour · ● proposed

owner **must not** shout at the dog for unwanted behaviour

- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [unwanted behaviour](#cn_01M82AHPS6SQKW9E9EPJYC3KMS)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§19](#su_01M82ABDR28HTPAFF4C44FRBZN)

<a id="ru_01M82AKNKHBHSK6HA7XAZBSVGW"></a>
### Dog in car must travel in crate or wear harness · ● proposed

dog **must** travel in a crate or wear a safety harness attached to the seat belt

- **When:** when travelling in a car
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [car](#cn_01M82AKNKGVB3WQ6AJ3QXNT524), [crate](#cn_01M82AKNKGVB3WQ6AJ3QXNT525), [safety harness](#cn_01M82AKNKGVB3WQ6AJ3QXNT526), [seat belt](#cn_01M82AKNKGVB3WQ6AJ3QXNT527), [travels in](#rl_01M82AKNKGVB3WQ6AJ3QXNT52C), [wears](#rl_01M82AKNKGVB3WQ6AJ3QXNT52D), [is attached to](#rl_01M82AKNKGVB3WQ6AJ3QXNT52E)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="ru_01M82AC66KMJH32E2MQ3Z7ZBM4"></a>
### Dog microchip · ● proposed

dog owner **must** ensure the dog carries a microchip

- **When:** the dog is older than 4 months
- **Limit:** &gt; 4 months
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [microchip](#cn_01M82AC66KMJH32E2MQ3Z7ZBKT), [carries](#rl_01M82AC66KMJH32E2MQ3Z7ZBM1)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="ru_01M82AKNKHBHSK6HA7XAZBSVGZ"></a>
### Dog needs microchip for travel abroad · ● proposed

dog **must** have a microchip

- **When:** for travel abroad
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [microchip](#cn_01M82AC66KMJH32E2MQ3Z7ZBKT), [travel abroad](#cn_01M82AKNKGVB3WQ6AJ3QXNT52B), [requires](#rl_01M82AKNKHBHSK6HA7XAZBSVGT)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="ru_01M82AKNKHBHSK6HA7XAZBSVGY"></a>
### Dog needs pet passport for travel abroad · ● proposed

dog **must** have a pet passport

- **When:** for travel abroad
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [pet passport](#cn_01M82AKNKGVB3WQ6AJ3QXNT528), [travel abroad](#cn_01M82AKNKGVB3WQ6AJ3QXNT52B), [requires](#rl_01M82AKNKHBHSK6HA7XAZBSVGS)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="ru_01M82AKNKHBHSK6HA7XAZBSVH0"></a>
### Dog needs valid rabies vaccination for travel abroad · ● proposed

dog **must** have a valid rabies vaccination

- **When:** for travel abroad
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [rabies vaccination](#cn_01M82AE56ZYS5Y2Z0C35ECC9YA), [travel abroad](#cn_01M82AKNKGVB3WQ6AJ3QXNT52B), [requires](#rl_01M82AKNKHBHSK6HA7XAZBSVGV)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="ru_01M82AC66KMJH32E2MQ3Z7ZBM3"></a>
### Dog registration · ● proposed

dog owner **must** register the dog with the local authority

- **When:** the dog is older than 4 months
- **Limit:** &gt; 4 months
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [local authority](#cn_01M82AC66KMJH32E2MQ3Z7ZBKS), [dog registration](#cn_01M82AC66KMJH32E2MQ3Z7ZBKV), [is registered with](#rl_01M82AC66KMJH32E2MQ3Z7ZBM0)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="ru_01M82AJ8HWH90DHFSC2JB20DG7"></a>
### Dog should learn five basic commands · ● proposed

dog **must** learn the five basic commands sit, down, stay, come and leave it

- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [basic command](#cn_01M82AJ8HWH90DHFSC2JB20DFW), [should learn](#rl_01M82AJ8HWH90DHFSC2JB20DG3)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§21](#su_01M82ABDR28HTPAFF4C44FRBZR)

<a id="ru_01M82AJ8HWH90DHFSC2JB20DGA"></a>
### End training with a success · ● proposed

owner **must** always end a training session with a success

- **Refers to:** [training session](#cn_01M82AJ8HWH90DHFSC2JB20DFX)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§21](#su_01M82ABDR28HTPAFF4C44FRBZR)

<a id="ru_01M82AFTZDSHCD0SK6T4N2YZWG"></a>
### Everyday leash at least 1.5 m · ● proposed

dog owner **must** use a leash of at least 1.5 metres for everyday walks

- **When:** on everyday walks
- **Limit:** ≥ 1.5 m
- **Refers to:** [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6), [walk](#cn_01M82AFTZDSHCD0SK6T4N2YZWA), [is used for](#rl_01M82AFTZDSHCD0SK6T4N2YZWE)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="ru_01M82AFTZDSHCD0SK6T4N2YZWH"></a>
### Everyday leash at most 2 m · ● proposed

dog owner **must** use a leash of at most 2 metres for everyday walks

- **When:** on everyday walks
- **Limit:** ≤ 2 m
- **Refers to:** [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6), [walk](#cn_01M82AFTZDSHCD0SK6T4N2YZWA), [is used for](#rl_01M82AFTZDSHCD0SK6T4N2YZWE)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="ru_01M82ADJQKNCFSCKCDMA3H0R8K"></a>
### Feed a puppy three to four times a day · ● proposed

owner **must** feed a puppy three to four times a day

- **Cardinality:** at least 3, at most 4 of [is fed times per day](#rl_01M82ADJQKNCFSCKCDMA3H0R8H)
- **Refers to:** [feeding](#cn_01M82ADJQKNCFSCKCDMA3H0R88), [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ), [is fed times per day](#rl_01M82ADJQKNCFSCKCDMA3H0R8H)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="ru_01M82ADJQKNCFSCKCDMA3H0R8J"></a>
### Feed an adult dog twice a day · ● proposed

owner **must** feed an adult dog twice a day

- **Limit:** = 2 times per day
- **Refers to:** [adult dog](#cn_01M82ADJQKNCFSCKCDMA3H0R86), [feeding](#cn_01M82ADJQKNCFSCKCDMA3H0R88), [is fed times per day](#rl_01M82ADJQKNCFSCKCDMA3H0R8G)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="ru_01M82ADJQKNCFSCKCDMA3H0R8M"></a>
### Fresh water always available · ● proposed

owner **must** keep fresh water always available to the dog

- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [fresh water](#cn_01M82ADJQKNCFSCKCDMA3H0R89)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="ru_01M82AHPS6SQKW9E9EPJYC3KN2"></a>
### Ignore unwanted behaviour instead of shouting · ● proposed

owner **must** ignore unwanted behaviour instead of shouting

- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [unwanted behaviour](#cn_01M82AHPS6SQKW9E9EPJYC3KMS)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§19](#su_01M82ABDR28HTPAFF4C44FRBZN)

<a id="ru_01M82AM9P6EWS5D1VJCAH8Z7VS"></a>
### Insurance mandatory for dangerous breeds · ● proposed

dog owner **must** hold third-party liability insurance

- **When:** the dog is of a breed classified as dangerous by the local authority
- **Refers to:** [local authority](#cn_01M82AC66KMJH32E2MQ3Z7ZBKS), [dangerous breed](#cn_01M82ACZDNRYXG7FZCA8KC7FD2), [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [third-party liability insurance](#cn_01M82AM9P6EWS5D1VJCAH8Z7VA), [classifies as dangerous](#rl_01M82AM9P6EWS5D1VJCAH8Z7VK), [holds](#rl_01M82AM9P6EWS5D1VJCAH8Z7VP)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="ru_01M82AK1Z9HNB4ZNT1JN5CCR74"></a>
### Keep departure low-key · ● proposed

owner **must** keep the departure low-key

- **When:** when leaving the dog alone
- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [leaving the dog alone](#cn_01M82AK1Z8YRQBGAGXAECRMD6W)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="ru_01M82AM9P6EWS5D1VJCAH8Z7VT"></a>
### Leash in public places · ● proposed

dog owner **must** keep the dog on a leash in public places

- **When:** unless a sign allows free running
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6), [public place](#cn_01M82AM9P6EWS5D1VJCAH8Z7VE), [free-running sign](#cn_01M82AM9P6EWS5D1VJCAH8Z7VG), [is kept on](#rl_01M82AM9P6EWS5D1VJCAH8Z7VM), [is located in](#rl_01M82AM9P6EWS5D1VJCAH8Z7VN)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="ru_01M82AK1Z9HNB4ZNT1JN5CCR73"></a>
### Leave water and a safe chew toy · ● proposed

owner **must** leave water and a safe chew toy for the dog

- **When:** before leaving the dog alone
- **Refers to:** [fresh water](#cn_01M82ADJQKNCFSCKCDMA3H0R89), [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [safe chew toy](#cn_01M82AK1Z9HNB4ZNT1JN5CCR6R), [leaves for the dog](#rl_01M82AK1Z9HNB4ZNT1JN5CCR6X), [leaves for the dog](#rl_01M82AK1Z9HNB4ZNT1JN5CCR6Y)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="ru_01M82AM9P6EWS5D1VJCAH8Z7VR"></a>
### Liability insurance recommended · ● proposed

dog owner **may** take out third-party liability insurance (strongly recommended)

- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [third-party liability insurance](#cn_01M82AM9P6EWS5D1VJCAH8Z7VA), [holds](#rl_01M82AM9P6EWS5D1VJCAH8Z7VP)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="ru_01M82AG9DZ4Q7M3Z8RX016AKWV"></a>
### Never jerk the leash · ● proposed

owner **must not** jerk the leash

- **Refers to:** [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6), [uses](#rl_01M82AG9DZ4Q7M3Z8RX016AKWQ)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§14](#su_01M82ABDR28HTPAFF4C44FRBZE)

<a id="ru_01M82AKNKHBHSK6HA7XAZBSVGX"></a>
### Never leave dog in parked car in warm weather · ● proposed

owner **must not** leave a dog in a parked car

- **When:** in warm weather
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [car](#cn_01M82AKNKGVB3WQ6AJ3QXNT524)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="ru_01M82AFTZDSHCD0SK6T4N2YZWJ"></a>
### No retractable leash in busy streets · ● proposed

dog owner **must not** use a retractable leash

- **When:** in busy streets
- **Refers to:** [retractable leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW7), [busy street](#cn_01M82AFTZDSHCD0SK6T4N2YZWB), [is not suitable in](#rl_01M82AFTZDSHCD0SK6T4N2YZWF)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="ru_01M82AM9P6EWS5D1VJCAH8Z7VQ"></a>
### Owner is liable for dog damage · ● proposed

dog owner **must** be liable for any damage the dog causes

- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [damage](#cn_01M82AM9P6EWS5D1VJCAH8Z7VF), [is liable for](#rl_01M82AM9P6EWS5D1VJCAH8Z7VH), [causes](#rl_01M82AM9P6EWS5D1VJCAH8Z7VJ)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="ru_01M82AHPS6SQKW9E9EPJYC3KMY"></a>
### Owner must be the dog's lead · ● proposed

owner **must** be the dog's lead: a calm, consistent and confident leader whose signals it can trust

- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [lead (leader)](#cn_01M82AHPS6SQKW9E9EPJYC3KMM), [is the lead of](#rl_01M82AHPS6SQKW9E9EPJYC3KMV)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§16](#su_01M82ABDR28HTPAFF4C44FRBZJ)

<a id="ru_01M82AF7YTEGBGGS9B245D10JS"></a>
### Praise puppy when relieving outside · ● proposed

owner **must** praise the puppy when it relieves itself outside

- **Refers to:** [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ), [house training](#cn_01M82AF7YTEGBGGS9B245D10JM)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§12](#su_01M82ABDR28HTPAFF4C44FRBZA)

<a id="ru_01M82AK1Z9HNB4ZNT1JN5CCR71"></a>
### Puppy alone at most 2 hours · ● proposed

owner **must not** leave a puppy alone for more than 2 hours

- **Limit:** ≤ 2 h
- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ), [leaving the dog alone](#cn_01M82AK1Z8YRQBGAGXAECRMD6W), [leaves alone](#rl_01M82AK1Z9HNB4ZNT1JN5CCR6V)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§23](#su_01M82ABDR30PE47ZK8WSGY3HX2)

<a id="ru_01M82AF7YTEGBGGS9B245D10JQ"></a>
### Puppy stays with mother until 8 weeks · ● proposed

puppy **must not** leave its mother

- **When:** before 8 weeks of age
- **Limit:** &lt; 8 weeks
- **Refers to:** [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ), [mother](#cn_01M82AF7YTEGBGGS9B245D10JK), [should not leave before 8 weeks](#rl_01M82AF7YTEGBGGS9B245D10JN)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§11](#su_01M82ABDR28HTPAFF4C44FRBZ9)

<a id="ru_01M82AE56ZYS5Y2Z0C35ECC9YH"></a>
### Rabies vaccination is mandatory · ● proposed

owner **must** have the dog vaccinated against rabies

- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [rabies vaccination](#cn_01M82AE56ZYS5Y2Z0C35ECC9YA), [receives](#rl_01M82AE56ZYS5Y2Z0C35ECC9YG)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="ru_01M82AE56ZYS5Y2Z0C35ECC9YJ"></a>
### Rabies vaccination renewed every year · ● proposed

owner **must** renew the dog's rabies vaccination every year

- **Limit:** ≤ 1 year
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [rabies vaccination](#cn_01M82AE56ZYS5Y2Z0C35ECC9YA), [receives](#rl_01M82AE56ZYS5Y2Z0C35ECC9YG)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="ru_01M82AHPS6SQKW9E9EPJYC3KN1"></a>
### Reward good behaviour immediately · ● proposed

owner **must** reward good behaviour immediately

- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [good behaviour](#cn_01M82AHPS6SQKW9E9EPJYC3KMR), [reward](#cn_01M82AHPS6SQKW9E9EPJYC3KMT), [is given for](#rl_01M82AHPS6SQKW9E9EPJYC3KMX)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§19](#su_01M82ABDR28HTPAFF4C44FRBZN)

<a id="ru_01M82AG9DZ4Q7M3Z8RX016AKWS"></a>
### Reward the dog when the leash is loose · ● proposed

owner **must** reward the dog

- **When:** when the leash is loose
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6), [leash training](#cn_01M82AG9DZ4Q7M3Z8RX016AKWJ)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§14](#su_01M82ABDR28HTPAFF4C44FRBZE)

<a id="ru_01M82AHPS6SQKW9E9EPJYC3KN0"></a>
### Set clear rules and keep them · ● proposed

owner **must** set clear rules for the dog (for example, whether it may lie on the sofa) and keep them

- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [household rule for the dog](#cn_01M82AHPS6SQKW9E9EPJYC3KMQ)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§18](#su_01M82ABDR28HTPAFF4C44FRBZM)

<a id="ru_01M82AF7YTEGBGGS9B245D10JT"></a>
### Socialise puppy between 8 and 16 weeks · ● proposed

owner **must** let the puppy get to know many people, sounds, surfaces and traffic in a calm way

- **When:** between 8 and 16 weeks of age
- **Refers to:** [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§12](#su_01M82ABDR28HTPAFF4C44FRBZA)

<a id="ru_01M82AG9DZ4Q7M3Z8RX016AKWR"></a>
### Start leash training at 8 to 10 weeks · ● proposed

owner **must** start leash training when the puppy is 8 to 10 weeks old

- **Refers to:** [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ), [leash training](#cn_01M82AG9DZ4Q7M3Z8RX016AKWJ), [undergoes](#rl_01M82AG9DZ4Q7M3Z8RX016AKWP)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§14](#su_01M82ABDR28HTPAFF4C44FRBZE)

<a id="ru_01M82AG9DZ4Q7M3Z8RX016AKWT"></a>
### Stop walking when the dog pulls · ● proposed

owner **must** stop walking

- **When:** when the dog pulls
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [leash training](#cn_01M82AG9DZ4Q7M3Z8RX016AKWJ)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§14](#su_01M82ABDR28HTPAFF4C44FRBZE)

<a id="ru_01M82AH1GXVV72WP99JQXMH6Y2"></a>
### Take a puppy outside to relieve itself every 2 to 3 hours · ● proposed

owner **must** take the puppy outside to relieve itself every 2 to 3 hours

- **When:** the dog is a puppy
- **Refers to:** [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="ru_01M82AF7YTEGBGGS9B245D10JR"></a>
### Take puppy outside for house training · ● proposed

owner **must** take the puppy outside after every meal, after every nap and after play, starting on the first day

- **Refers to:** [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ), [house training](#cn_01M82AF7YTEGBGGS9B245D10JM), [undergoes](#rl_01M82AF7YTEGBGGS9B245D10JP)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§12](#su_01M82ABDR28HTPAFF4C44FRBZA)

<a id="ru_01M82AH1GXVV72WP99JQXMH6Y1"></a>
### Total daily walk time for large and working breeds · ● proposed

owner **must** walk an adult large or working breed dog up to 2 hours in total per day

- **When:** the adult dog is of a large or working breed
- **Limit:** ≤ 2 hours per day
- **Refers to:** [adult dog](#cn_01M82ADJQKNCFSCKCDMA3H0R86), [walk](#cn_01M82AFTZDSHCD0SK6T4N2YZWA), [large breed](#cn_01M82AH1GXVV72WP99JQXMH6XQ), [working breed](#cn_01M82AH1GXVV72WP99JQXMH6XR)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="ru_01M82AH1GXVV72WP99JQXMH6Y0"></a>
### Total daily walk time for small breeds · ● proposed

owner **must** walk an adult small-breed dog 30 to 60 minutes in total per day

- **When:** the adult dog is of a small breed
- **Refers to:** [adult dog](#cn_01M82ADJQKNCFSCKCDMA3H0R86), [walk](#cn_01M82AFTZDSHCD0SK6T4N2YZWA), [small breed](#cn_01M82AH1GXVV72WP99JQXMH6XP)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="ru_01M82AK1Z9HNB4ZNT1JN5CCR75"></a>
### Train a barking dog to be alone · ● proposed

owner **must** train the dog to be alone step by step, starting with a few minutes

- **When:** if the dog barks or howls while the owner is away
- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [barking or howling](#cn_01M82AK1Z9HNB4ZNT1JN5CCR6S), [step-by-step alone training](#cn_01M82AK1Z9HNB4ZNT1JN5CCR6T), [is addressed by](#rl_01M82AK1Z9HNB4ZNT1JN5CCR6Z)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 3
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="ru_01M82AJ8HWH90DHFSC2JB20DGB"></a>
### Training course recommended in first year · ● proposed

owner **may** attend a dog training course with a certified trainer

- **When:** in the dog's first year (recommended)
- **Refers to:** [dog training course](#cn_01M82AJ8HWH90DHFSC2JB20DFY), [certified trainer](#cn_01M82AJ8HWH90DHFSC2JB20DFZ), [is given by](#rl_01M82AJ8HWH90DHFSC2JB20DG4)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§22](#su_01M82ABDR28HTPAFF4C44FRBZS)

<a id="ru_01M82AJ8HWH90DHFSC2JB20DG8"></a>
### Training session at least 5 minutes · ● proposed

owner **must** train in sessions of at least 5 minutes

- **Limit:** ≥ 5 min
- **Refers to:** [training session](#cn_01M82AJ8HWH90DHFSC2JB20DFX)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§21](#su_01M82ABDR28HTPAFF4C44FRBZR)

<a id="ru_01M82AJ8HWH90DHFSC2JB20DG9"></a>
### Training session at most 10 minutes · ● proposed

owner **must** train in short sessions of at most 10 minutes, several times a day

- **Limit:** ≤ 10 min
- **Refers to:** [training session](#cn_01M82AJ8HWH90DHFSC2JB20DFX)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§21](#su_01M82ABDR28HTPAFF4C44FRBZR)

<a id="ru_01M82AEQW4JVCNX0WEDNNR61WD"></a>
### Trim claws when they click · ● proposed

dog owner **must** trim the dog's claws

- **When:** the claws can be heard clicking on the floor
- **Refers to:** [claw trimming](#cn_01M82AEQW4JVCNX0WEDNNR61W2), [claw](#cn_01M82AEQW4JVCNX0WEDNNR61W4), [is applied to](#rl_01M82AEQW4JVCNX0WEDNNR61W8)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="ru_01M82AFTZDSHCD0SK6T4N2YZWM"></a>
### Two fingers fit under collar · ● proposed

dog owner **must** be able to slide two fingers under the collar

- **Limit:** = 2 fingers
- **Refers to:** [collar](#cn_01M82AFTZDSHCD0SK6T4N2YZW8)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="ru_01M82AHPS6SQKW9E9EPJYC3KMZ"></a>
### Use the same command words every time · ● proposed

owner **must** use the same command words every time and make sure everyone in the family uses them too

- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [command word](#cn_01M82AHPS6SQKW9E9EPJYC3KMN), [family](#cn_01M82AHPS6SQKW9E9EPJYC3KMP), [uses](#rl_01M82AHPS6SQKW9E9EPJYC3KMW)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§17](#su_01M82ABDR28HTPAFF4C44FRBZK)

<a id="ru_01M82AK1Z9HNB4ZNT1JN5CCR72"></a>
### Walk the dog before leaving · ● proposed

owner **must** walk the dog

- **When:** before leaving the dog alone
- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [walk](#cn_01M82AFTZDSHCD0SK6T4N2YZWA), [walks before leaving](#rl_01M82AK1Z9HNB4ZNT1JN5CCR6W)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="ru_01M82AEQW4JVCNX0WEDNNR61WE"></a>
### Wash bed and blankets weekly at 60 °C · ● proposed

dog owner **must** wash the dog's bed and blankets once a week

- **Limit:** = 1 times per week
- **Refers to:** [dog bed](#cn_01M82AEQW4JVCNX0WEDNNR61W5), [blanket](#cn_01M82AEQW4JVCNX0WEDNNR61W6), [has](#rl_01M82AEQW4JVCNX0WEDNNR61WA)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="ru_01M82AE56ZYS5Y2Z0C35ECC9YK"></a>
### Yearly veterinary check-up · ● proposed

owner **must** take the dog to the veterinarian for a check-up at least once a year

- **Limit:** ≥ 1 per year
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [veterinarian](#cn_01M82AE56ZYS5Y2Z0C35ECC9YB), [check-up](#cn_01M82AE56ZYS5Y2Z0C35ECC9YC), [takes dog to](#rl_01M82AE56ZYS5Y2Z0C35ECC9YE), [has](#rl_01M82AE56ZYS5Y2Z0C35ECC9YF)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

## Properties

<a id="pr_01M82ADJQKNCFSCKCDMA3H0R8N"></a>
### Adult dog feeding frequency · ● proposed

- **Of:** [adult dog](#cn_01M82ADJQKNCFSCKCDMA3H0R86)
- **feeding frequency:** 2 times per day
- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="pr_01M82AE56ZYS5Y2Z0C35ECC9YM"></a>
### Age of puppy at first vaccinations · ● proposed

- **Of:** [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ)
- **age at first vaccinations:** 8 weeks
- **Level:** 3
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="pr_01M82AFTZDSHCD0SK6T4N2YZWP"></a>
### Collar fit · ● proposed

- **Of:** [collar](#cn_01M82AFTZDSHCD0SK6T4N2YZW8)
- **fit:** two fingers can slide under the collar
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="pr_01M82AHPS6SQKW9E9EPJYC3KN5"></a>
### Consequence of no reliable lead · ● proposed

- **Of:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM)
- **behaviour without a reliable lead:** may become anxious or try to take control
- **Level:** 3
- **Evidence:** [§20](#su_01M82ABDR28HTPAFF4C44FRBZP)

<a id="pr_01M82AH1GXVV72WP99JQXMH6Y5"></a>
### Daily walk time of large breeds · ● proposed

- **Of:** [large breed](#cn_01M82AH1GXVV72WP99JQXMH6XQ)
- **total daily walk time:** up to 2 hours
- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="pr_01M82AH1GXVV72WP99JQXMH6Y4"></a>
### Daily walk time of small breeds · ● proposed

- **Of:** [small breed](#cn_01M82AH1GXVV72WP99JQXMH6XP)
- **total daily walk time:** 30 to 60 minutes
- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="pr_01M82AH1GXVV72WP99JQXMH6Y6"></a>
### Daily walk time of working breeds · ● proposed

- **Of:** [working breed](#cn_01M82AH1GXVV72WP99JQXMH6XR)
- **total daily walk time:** up to 2 hours
- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="pr_01M82AC66KMJH32E2MQ3Z7ZBM5"></a>
### Dog lifespan · ● proposed

- **Of:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM)
- **lifespan:** 10 to 15 years
- **Level:** 2
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="pr_01M82AFTZDSHCD0SK6T4N2YZWN"></a>
### Everyday leash length · ● proposed

- **Of:** [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6)
- **length for everyday walks:** 1.5 to 2 m
- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="pr_01M82ACZDNRYXG7FZCA8KC7FDJ"></a>
### Exercise need of large and working breeds · ● proposed

- **Of:** [large and working breed](#cn_01M82ACZDNRYXG7FZCA8KC7FCZ)
- **exercise need:** more
- **Level:** 2
- **Evidence:** [§5](#su_01M82ABDR1CAX5PFZ2HWSEQHBD)

<a id="pr_01M82ACZDNRYXG7FZCA8KC7FDG"></a>
### Exercise need of small companion breeds · ● proposed

- **Of:** [small companion breed](#cn_01M82ACZDNRYXG7FZCA8KC7FCY)
- **exercise need:** less
- **Level:** 2
- **Evidence:** [§4](#su_01M82ABDR1CAX5PFZ2HWSEQHBC)

<a id="pr_01M82ACZDNRYXG7FZCA8KC7FDM"></a>
### Grooming need of long-haired breeds · ● proposed

- **Of:** [long-haired breed](#cn_01M82ACZDNRYXG7FZCA8KC7FD0)
- **grooming need:** more than short-haired breeds
- **Level:** 2
- **Evidence:** [§6](#su_01M82ABDR1CAX5PFZ2HWSEQHBE)

<a id="pr_01M82AG9DZ4Q7M3Z8RX016AKWW"></a>
### Leash training start age · ● proposed

- **Of:** [leash training](#cn_01M82AG9DZ4Q7M3Z8RX016AKWJ)
- **start age:** 8 to 10 weeks
- **Level:** 3
- **Evidence:** [§14](#su_01M82ABDR28HTPAFF4C44FRBZE)

<a id="pr_01M82AK1Z9HNB4ZNT1JN5CCR77"></a>
### Maximum time a puppy may be alone · ● proposed

- **Of:** [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ)
- **maximum time alone:** 2 h
- **Level:** 3
- **Evidence:** [§23](#su_01M82ABDR30PE47ZK8WSGY3HX2)

<a id="pr_01M82AK1Z9HNB4ZNT1JN5CCR76"></a>
### Maximum time an adult dog may be alone · ● proposed

- **Of:** [adult dog](#cn_01M82ADJQKNCFSCKCDMA3H0R86)
- **maximum time alone at home:** 6 h
- **Level:** 2
- **Evidence:** [§23](#su_01M82ABDR30PE47ZK8WSGY3HX2)

<a id="pr_01M82ACZDNRYXG7FZCA8KC7FDK"></a>
### Mental work need of large and working breeds · ● proposed

- **Of:** [large and working breed](#cn_01M82ACZDNRYXG7FZCA8KC7FCZ)
- **mental work need:** more
- **Level:** 2
- **Evidence:** [§5](#su_01M82ABDR1CAX5PFZ2HWSEQHBD)

<a id="pr_01M82AH1GXVV72WP99JQXMH6Y8"></a>
### Minimum walks per day for an adult dog · ● proposed

- **Of:** [adult dog](#cn_01M82ADJQKNCFSCKCDMA3H0R86)
- **minimum walks per day:** 2 walks
- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="pr_01M82AJ8HWH90DHFSC2JB20DGD"></a>
### Number of basic commands · ● proposed

- **Of:** [basic command](#cn_01M82AJ8HWH90DHFSC2JB20DFW)
- **count:** 5
- **Level:** 2
- **Evidence:** [§21](#su_01M82ABDR28HTPAFF4C44FRBZR)

<a id="pr_01M82AF7YTEGBGGS9B245D10JV"></a>
### Puppy age limit · ● proposed

- **Of:** [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ)
- **age:** younger than 6 months
- **Level:** 3
- **Evidence:** [§11](#su_01M82ABDR28HTPAFF4C44FRBZ9)

<a id="pr_01M82ADJQKNCFSCKCDMA3H0R8P"></a>
### Puppy feeding frequency · ● proposed

- **Of:** [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ)
- **feeding frequency:** 3 to 4 times per day
- **Level:** 3
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="pr_01M82AH1GXVV72WP99JQXMH6Y7"></a>
### Puppy relief interval · ● proposed

- **Of:** [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ)
- **relief interval:** 2 to 3 hours
- **Level:** 3
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="pr_01M82AHPS6SQKW9E9EPJYC3KN4"></a>
### Qualities of a good lead · ● proposed

- **Of:** [lead (leader)](#cn_01M82AHPS6SQKW9E9EPJYC3KMM)
- **qualities:** calm, consistent and confident; signals the dog can trust
- **Level:** 2
- **Evidence:** [§16](#su_01M82ABDR28HTPAFF4C44FRBZJ)

<a id="pr_01M82AE56ZYS5Y2Z0C35ECC9YN"></a>
### Rabies vaccination renewal interval · ● proposed

- **Of:** [rabies vaccination](#cn_01M82AE56ZYS5Y2Z0C35ECC9YA)
- **renewal interval:** 1 year
- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="pr_01M82AF7YTEGBGGS9B245D10JW"></a>
### Socialisation period · ● proposed

- **Of:** [puppy](#cn_01M82AF7YTEGBGGS9B245D10JJ)
- **socialisation period:** 8 to 16 weeks
- **Level:** 3
- **Evidence:** [§12](#su_01M82ABDR28HTPAFF4C44FRBZA)

<a id="pr_01M82ACZDNRYXG7FZCA8KC7FDH"></a>
### Space need of large and working breeds · ● proposed

- **Of:** [large and working breed](#cn_01M82ACZDNRYXG7FZCA8KC7FCZ)
- **space need:** more
- **Level:** 2
- **Evidence:** [§5](#su_01M82ABDR1CAX5PFZ2HWSEQHBD)

<a id="pr_01M82ACZDNRYXG7FZCA8KC7FDF"></a>
### Space need of small companion breeds · ● proposed

- **Of:** [small companion breed](#cn_01M82ACZDNRYXG7FZCA8KC7FCY)
- **space need:** less
- **Level:** 2
- **Evidence:** [§4](#su_01M82ABDR1CAX5PFZ2HWSEQHBC)

<a id="pr_01M82AK1Z9HNB4ZNT1JN5CCR78"></a>
### Starting duration of alone training · ● proposed

- **Of:** [step-by-step alone training](#cn_01M82AK1Z9HNB4ZNT1JN5CCR6T)
- **starting duration:** a few minutes
- **Level:** 3
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="pr_01M82AJ8HWH90DHFSC2JB20DGF"></a>
### Training session frequency · ● proposed

- **Of:** [training session](#cn_01M82AJ8HWH90DHFSC2JB20DFX)
- **frequency:** several times a day
- **Level:** 2
- **Evidence:** [§21](#su_01M82ABDR28HTPAFF4C44FRBZR)

<a id="pr_01M82AJ8HWH90DHFSC2JB20DGE"></a>
### Training session length · ● proposed

- **Of:** [training session](#cn_01M82AJ8HWH90DHFSC2JB20DFX)
- **duration:** 5 to 10 min
- **Level:** 2
- **Evidence:** [§21](#su_01M82ABDR28HTPAFF4C44FRBZR)

<a id="pr_01M82AEQW4JVCNX0WEDNNR61WF"></a>
### Wash temperature for bed and blankets · ● proposed

- **Of:** [Wash bed and blankets weekly at 60 °C](#ru_01M82AEQW4JVCNX0WEDNNR61WE)
- **washing temperature:** 60 °C
- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

## Statements

<a id="st_01M82AK1Z8YRQBGAGXAECRMD6C"></a>
### Adult dog alone at most 6 hours · ● proposed

An adult dog must never be left alone at home for more than 6 hours.

- **Level:** 2
- **Evidence:** [§23](#su_01M82ABDR30PE47ZK8WSGY3HX2)

<a id="st_01M82ADJQKNCFSCKCDMA3H0R7R"></a>
### Adult dog feeding frequency · ● proposed

An adult dog is fed twice a day.

- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="st_01M82AH1GXVV72WP99JQXMH6X5"></a>
### Adult dog walk frequency · ● proposed

An adult dog needs at least two walks a day.

- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="st_01M82ACZDMSZ5RR2QTW9X92PB7"></a>
### Breeds differ · ● proposed

Breeds differ in size, energy and the care they need.

- **Level:** 2
- **Evidence:** [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHBB)

<a id="st_01M82AC66KMJH32E2MQ3Z7ZBK9"></a>
### Check fit before getting a dog · ● proposed

Before you get a dog, check that your home, your working hours and your budget fit the dog you want.

- **Level:** 2
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="st_01M82ACZDNRYXG7FZCA8KC7FCH"></a>
### Check the local list · ● proposed

Check the local list of dangerous breeds before you choose a breed.

- **Level:** 3
- **Evidence:** [§7](#su_01M82ABDR1CAX5PFZ2HWSEQHBF)

<a id="st_01M82AEQW4JVCNX0WEDNNR61VQ"></a>
### Claw trimming · ● proposed

Trim the dog's claws when you can hear them clicking on the floor.

- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="st_01M82AFTZDSHCD0SK6T4N2YZVZ"></a>
### Collar fit check · ● proposed

You should be able to slide two fingers under the collar.

- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="st_01M82AHPS6SQKW9E9EPJYC3KMH"></a>
### Consequence of lacking a reliable lead · ● proposed

A dog that does not see its owner as a reliable lead may become anxious or try to take control.

- **Level:** 3
- **Evidence:** [§20](#su_01M82ABDR28HTPAFF4C44FRBZP)

<a id="st_01M82AEQW4JVCNX0WEDNNR61VP"></a>
### Daily brushing for long-haired breeds · ● proposed

Long-haired breeds need brushing every day.

- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="st_01M82AKNKGVB3WQ6AJ3QXNT51Q"></a>
### Dog in car travels in crate or harness · ● proposed

In a car, a dog must travel in a crate or wear a safety harness attached to the seat belt.

- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="st_01M82AC66KMJH32E2MQ3Z7ZBK7"></a>
### Dog lifespan · ● proposed

A dog lives 10 to 15 years.

- **Level:** 1
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="st_01M82AHPS6SQKW9E9EPJYC3KMB"></a>
### Dog looks to owner for direction · ● proposed

A dog looks to its owner for direction.

- **Level:** 2
- **Evidence:** [§16](#su_01M82ABDR28HTPAFF4C44FRBZJ)

<a id="st_01M82AC66KMJH32E2MQ3Z7ZBKB"></a>
### Dog microchip · ● proposed

A dog older than 4 months must carry a microchip.

- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="st_01M82AC66KMJH32E2MQ3Z7ZBKA"></a>
### Dog registration · ● proposed

A dog older than 4 months must be registered with the local authority.

- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="st_01M82AK1Z8YRQBGAGXAECRMD6B"></a>
### Dogs are social · ● proposed

Dogs are social animals.

- **Level:** 2
- **Evidence:** [§23](#su_01M82ABDR30PE47ZK8WSGY3HX2)

<a id="st_01M82AJ8HWH90DHFSC2JB20DFR"></a>
### End with a success · ● proposed

A training session should always end with a success.

- **Level:** 2
- **Evidence:** [§21](#su_01M82ABDR28HTPAFF4C44FRBZR)

<a id="st_01M82AFTZDSHCD0SK6T4N2YZVW"></a>
### Everyday leash length · ● proposed

A leash of 1.5 to 2 metres should be used for everyday walks.

- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="st_01M82AJ8HWH90DHFSC2JB20DFP"></a>
### Five basic commands · ● proposed

Every dog should learn five basic commands: sit, down, stay, come and leave it.

- **Level:** 2
- **Evidence:** [§21](#su_01M82ABDR28HTPAFF4C44FRBZR)

<a id="st_01M82ADJQKNCFSCKCDMA3H0R7V"></a>
### Foods poisonous to dogs · ● proposed

Chocolate, grapes, onions and xylitol are poisonous to dogs.

- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="st_01M82ADJQKNCFSCKCDMA3H0R7T"></a>
### Fresh water always available · ● proposed

Fresh water must always be available.

- **Level:** 2
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="st_01M82AF7YTEGBGGS9B245D10J9"></a>
### House training starts on day one · ● proposed

House training of a puppy starts on the first day.

- **Level:** 3
- **Evidence:** [§12](#su_01M82ABDR28HTPAFF4C44FRBZA)

<a id="st_01M82AHPS6SQKW9E9EPJYC3KMG"></a>
### Ignore unwanted behaviour · ● proposed

Unwanted behaviour should be ignored instead of shouting.

- **Level:** 2
- **Evidence:** [§19](#su_01M82ABDR28HTPAFF4C44FRBZN)

<a id="st_01M82AM9P6EWS5D1VJCAH8Z7TX"></a>
### Insurance mandatory for dangerous breeds · ● proposed

Third-party liability insurance is mandatory for breeds classified as dangerous by the local authority.

- **Level:** 3
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="st_01M82ACZDNRYXG7FZCA8KC7FCE"></a>
### Large and working breeds need more · ● proposed

Large and working breeds need more space, more exercise and more mental work.

- **Level:** 2
- **Evidence:** [§5](#su_01M82ABDR1CAX5PFZ2HWSEQHBD)

<a id="st_01M82AFTZDSHCD0SK6T4N2YZVY"></a>
### Leash attachment · ● proposed

The leash is attached to a well-fitting collar or harness.

- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="st_01M82AM9P6EWS5D1VJCAH8Z7TY"></a>
### Leash in public places · ● proposed

In public places, a dog must be kept on a leash unless a sign allows free running.

- **Level:** 1
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="st_01M82AG9DZ4Q7M3Z8RX016AKWA"></a>
### Leash training start age · ● proposed

Leash training starts when the puppy is 8 to 10 weeks old.

- **Level:** 3
- **Evidence:** [§14](#su_01M82ABDR28HTPAFF4C44FRBZE)

<a id="st_01M82AM9P5HMXJKJ1997DWSW21"></a>
### Liability insurance recommended · ● proposed

Third-party liability insurance for dog owners is strongly recommended.

- **Level:** 2
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="st_01M82AC66KMJH32E2MQ3Z7ZBK8"></a>
### Lifelong needs of a dog · ● proposed

A dog needs daily exercise, company, training and veterinary care for its whole life.

- **Level:** 1
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="st_01M82ACZDNRYXG7FZCA8KC7FCF"></a>
### Long-haired breeds need more grooming · ● proposed

Long-haired breeds need more grooming than short-haired breeds.

- **Level:** 2
- **Evidence:** [§6](#su_01M82ABDR1CAX5PFZ2HWSEQHBE)

<a id="st_01M82AG9DZ4Q7M3Z8RX016AKWD"></a>
### Never jerk the leash · ● proposed

The leash is never jerked.

- **Level:** 2
- **Evidence:** [§14](#su_01M82ABDR28HTPAFF4C44FRBZE)

<a id="st_01M82AKNKGVB3WQ6AJ3QXNT51R"></a>
### Never leave dog in parked car in warm weather · ● proposed

A dog must never be left in a parked car in warm weather.

- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="st_01M82AJ8HWH90DHFSC2JB20DFT"></a>
### Obedience test for dangerous breeds · ● proposed

Dogs of breeds classified as dangerous must pass an obedience test.

- **Level:** 3
- **Evidence:** [§22](#su_01M82ABDR28HTPAFF4C44FRBZS)

<a id="st_01M82AM9P5HMXJKJ1997DWSW20"></a>
### Owner liable for dog damage · ● proposed

The dog owner is liable for any damage the dog causes.

- **Level:** 1
- **Evidence:** [§26](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="st_01M82AHPS6SQKW9E9EPJYC3KMC"></a>
### Owner should be the dog's lead · ● proposed

The owner should be the dog's lead: a calm, consistent and confident leader whose signals the dog can trust.

- **Level:** 2
- **Evidence:** [§16](#su_01M82ABDR28HTPAFF4C44FRBZJ)

<a id="st_01M82AH1GXVV72WP99JQXMH6X9"></a>
### Pick up dog waste · ● proposed

The owner must always pick up the dog's waste and put it in a waste bin.

- **Level:** 1
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="st_01M82AF7YTEGBGGS9B245D10JB"></a>
### Praise when relieving outside · ● proposed

The puppy is praised when it relieves itself outside.

- **Level:** 3
- **Evidence:** [§12](#su_01M82ABDR28HTPAFF4C44FRBZA)

<a id="st_01M82AK1Z8YRQBGAGXAECRMD6E"></a>
### Preparing before leaving · ● proposed

Before leaving, the owner should walk the dog, leave water and a safe chew toy, and keep the departure low-key.

- **Level:** 2
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="st_01M82AK1Z8YRQBGAGXAECRMD6D"></a>
### Puppy alone at most 2 hours · ● proposed

Puppies should not be left alone for more than 2 hours.

- **Level:** 3
- **Evidence:** [§23](#su_01M82ABDR30PE47ZK8WSGY3HX2)

<a id="st_01M82AF7YTEGBGGS9B245D10J7"></a>
### Puppy definition · ● proposed

A puppy is a dog younger than 6 months.

- **Level:** 3
- **Evidence:** [§11](#su_01M82ABDR28HTPAFF4C44FRBZ9)

<a id="st_01M82ADJQKNCFSCKCDMA3H0R7S"></a>
### Puppy feeding frequency · ● proposed

A puppy is fed three to four times a day.

- **Level:** 3
- **Evidence:** [§8](#su_01M82ABDR1CAX5PFZ2HWSEQHBH)

<a id="st_01M82AE56ZYS5Y2Z0C35ECC9Y2"></a>
### Puppy first vaccinations · ● proposed

A puppy receives its first vaccinations at 8 weeks of age.

- **Level:** 3
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="st_01M82AH1GXVV72WP99JQXMH6X8"></a>
### Puppy relief interval · ● proposed

A puppy must be taken outside to relieve itself every 2 to 3 hours.

- **Level:** 3
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="st_01M82AF7YTEGBGGS9B245D10J8"></a>
### Puppy stays with mother · ● proposed

Puppies should not leave their mother before 8 weeks of age.

- **Level:** 3
- **Evidence:** [§11](#su_01M82ABDR28HTPAFF4C44FRBZ9)

<a id="st_01M82AE56ZYS5Y2Z0C35ECC9Y3"></a>
### Rabies vaccination mandatory · ● proposed

The rabies vaccination is mandatory.

- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="st_01M82AE56ZYS5Y2Z0C35ECC9Y4"></a>
### Rabies vaccination renewed yearly · ● proposed

The rabies vaccination must be renewed every year.

- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

<a id="st_01M82AKNKGVB3WQ6AJ3QXNT51S"></a>
### Requirements for travel abroad · ● proposed

For travel abroad, a dog needs a pet passport, a microchip and a valid rabies vaccination.

- **Level:** 3
- **Evidence:** [§25](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="st_01M82AFTZDSHCD0SK6T4N2YZVX"></a>
### Retractable leash in busy streets · ● proposed

A retractable leash is not suitable in busy streets.

- **Level:** 2
- **Evidence:** [§13](#su_01M82ABDR28HTPAFF4C44FRBZC)

<a id="st_01M82AHPS6SQKW9E9EPJYC3KMF"></a>
### Reward good behaviour immediately · ● proposed

Good behaviour should be rewarded immediately.

- **Level:** 2
- **Evidence:** [§19](#su_01M82ABDR28HTPAFF4C44FRBZN)

<a id="st_01M82AG9DZ4Q7M3Z8RX016AKWB"></a>
### Reward loose leash · ● proposed

The dog is rewarded when the leash is loose.

- **Level:** 2
- **Evidence:** [§14](#su_01M82ABDR28HTPAFF4C44FRBZE)

<a id="st_01M82AHPS6SQKW9E9EPJYC3KME"></a>
### Set and keep clear rules for the dog · ● proposed

The owner should set clear rules for the dog, such as whether it may lie on the sofa, and keep them.

- **Level:** 2
- **Evidence:** [§18](#su_01M82ABDR28HTPAFF4C44FRBZM)

<a id="st_01M82ACZDNRYXG7FZCA8KC7FCD"></a>
### Small companion breeds suit flats · ● proposed

Small companion breeds need less space and less exercise and adapt well to flats.

- **Level:** 2
- **Evidence:** [§4](#su_01M82ABDR1CAX5PFZ2HWSEQHBC)

<a id="st_01M82AF7YTEGBGGS9B245D10JC"></a>
### Socialisation period · ● proposed

Between 8 and 16 weeks, the puppy should get to know many people, sounds, surfaces and traffic in a calm way.

- **Level:** 3
- **Evidence:** [§12](#su_01M82ABDR28HTPAFF4C44FRBZA)

<a id="st_01M82ACZDNRYXG7FZCA8KC7FCG"></a>
### Some breeds classified dangerous · ● proposed

Some breeds are classified as dangerous by the local authority.

- **Level:** 3
- **Evidence:** [§7](#su_01M82ABDR1CAX5PFZ2HWSEQHBF)

<a id="st_01M82AG9DZ4Q7M3Z8RX016AKWC"></a>
### Stop when dog pulls · ● proposed

The walk is stopped when the dog pulls.

- **Level:** 2
- **Evidence:** [§14](#su_01M82ABDR28HTPAFF4C44FRBZE)

<a id="st_01M82AF7YTEGBGGS9B245D10JA"></a>
### Take puppy outside · ● proposed

During house training, the puppy is taken outside after every meal, after every nap and after play.

- **Level:** 3
- **Evidence:** [§12](#su_01M82ABDR28HTPAFF4C44FRBZA)

<a id="st_01M82AK1Z8YRQBGAGXAECRMD6F"></a>
### Training a barking dog to be alone · ● proposed

If a dog barks or howls while the owner is away, the owner should train it to be alone step by step, starting with a few minutes.

- **Level:** 3
- **Evidence:** [§24](#su_01M82ABDR30PE47ZK8WSGY3HX3)

<a id="st_01M82AJ8HWH90DHFSC2JB20DFS"></a>
### Training course recommended · ● proposed

A dog training course with a certified trainer is recommended in the first year.

- **Level:** 2
- **Evidence:** [§22](#su_01M82ABDR28HTPAFF4C44FRBZS)

<a id="st_01M82AJ8HWH90DHFSC2JB20DFQ"></a>
### Training session length · ● proposed

Training is done in short sessions of 5 to 10 minutes, several times a day.

- **Level:** 2
- **Evidence:** [§21](#su_01M82ABDR28HTPAFF4C44FRBZR)

<a id="st_01M82AHPS6SQKW9E9EPJYC3KMD"></a>
### Use the same command words · ● proposed

The same command words should be used every time, and everyone in the family should use them too.

- **Level:** 2
- **Evidence:** [§17](#su_01M82ABDR28HTPAFF4C44FRBZK)

<a id="st_01M82AH1GXVV72WP99JQXMH6X7"></a>
### Walk time for large and working breeds · ● proposed

Large and working breeds need up to 2 hours of walking a day.

- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="st_01M82AH1GXVV72WP99JQXMH6X6"></a>
### Walk time for small breeds · ● proposed

Small breeds need 30 to 60 minutes of walking a day in total.

- **Level:** 2
- **Evidence:** [§15](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="st_01M82AEQW4JVCNX0WEDNNR61VR"></a>
### Washing bed and blankets · ● proposed

Wash the dog's bed and blankets once a week at 60 °C.

- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="st_01M82AEQW4JVCNX0WEDNNR61VN"></a>
### Weekly brushing · ● proposed

A dog should be brushed at least once a week.

- **Level:** 2
- **Evidence:** [§10](#su_01M82ABDR1CAX5PFZ2HWSEQHBN)

<a id="st_01M82AE56ZYS5Y2Z0C35ECC9Y5"></a>
### Yearly veterinary check-up · ● proposed

The owner must take the dog to the veterinarian for a check-up at least once a year.

- **Level:** 2
- **Evidence:** [§9](#su_01M82ABDR1CAX5PFZ2HWSEQHBK)

## Evidence

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHB8"></a>
**§1** · 01-before-you-get-a-dog.md › 1. Before You Get a Dog

> A dog lives 10 to 15 years. It needs daily exercise, company, training and veterinary care for its whole life. Before you get a dog, check that your home, your working hours and your budget fit the dog you want.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHB9"></a>
**§2** · 01-before-you-get-a-dog.md › 1. Before You Get a Dog

> A dog older than 4 months must be registered with the local authority and must carry a microchip.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBB"></a>
**§3** · 02-choosing-a-breed.md › 2. Choosing a Breed

> Breeds differ in size, energy and the care they need.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBC"></a>
**§4** · 02-choosing-a-breed.md › 2. Choosing a Breed

> **Small companion breeds** (for example, Maltese or Pug) need less space and less exercise and adapt well to flats.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBD"></a>
**§5** · 02-choosing-a-breed.md › 2. Choosing a Breed

> **Large and working breeds** (for example, Border Collie or German Shepherd) need more space, more exercise and more mental work.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBE"></a>
**§6** · 02-choosing-a-breed.md › 2. Choosing a Breed

> **Long-haired breeds** need more grooming than short-haired breeds.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBF"></a>
**§7** · 02-choosing-a-breed.md › 2. Choosing a Breed

> Some breeds are classified as dangerous by the local authority. Check the local list before you choose a breed.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBH"></a>
**§8** · 03-health-and-care/01-feeding.md › 3. Health and Care — 3.1 Feeding

> Feed an adult dog twice a day and a puppy three to four times a day. Fresh water must always be available. Chocolate, grapes, onions and xylitol are poisonous to dogs.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBK"></a>
**§9** · 03-health-and-care/02-vaccination-and-the-veterinarian.md › 3. Health and Care — 3.2 Vaccination and the Veterinarian

> A puppy receives its first vaccinations at 8 weeks of age. The rabies vaccination is mandatory and must be renewed every year. Take your dog to the veterinarian for a check-up at least once a year.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBN"></a>
**§10** · 03-health-and-care/03-grooming-and-hygiene.md › 3. Health and Care — 3.3 Grooming and Hygiene

> Brush your dog at least once a week; long-haired breeds need brushing every day. Trim the claws when you can hear them clicking on the floor. Wash your dog's bed and blankets once a week at 60 °C.

<a id="su_01M82ABDR28HTPAFF4C44FRBZ9"></a>
**§11** · 04-puppy-basics.md › 4. Puppy Basics

> A puppy is a dog younger than 6 months. Puppies should not leave their mother before 8 weeks of age.

<a id="su_01M82ABDR28HTPAFF4C44FRBZA"></a>
**§12** · 04-puppy-basics.md › 4. Puppy Basics

> House training starts on the first day: take the puppy outside after every meal, after every nap and after play, and praise it when it relieves itself outside. Between 8 and 16 weeks, let the puppy get to know many people, sounds, surfaces and traffic in a calm way.

<a id="su_01M82ABDR28HTPAFF4C44FRBZC"></a>
**§13** · 05-walking-and-the-leash/01-choosing-a-leash.md › 5. Walking and the Leash — 5.1 Choosing a Leash

> Use a leash of 1.5 to 2 metres for everyday walks. A retractable leash is not suitable in busy streets. Attach the leash to a well-fitting collar or harness: you should be able to slide two fingers under the collar.

<a id="su_01M82ABDR28HTPAFF4C44FRBZE"></a>
**§14** · 05-walking-and-the-leash/02-leash-training.md › 5. Walking and the Leash — 5.2 Leash Training

> Start leash training when the puppy is 8 to 10 weeks old. Reward the dog when the leash is loose, and stop walking when the dog pulls. Never jerk the leash.

<a id="su_01M82ABDR28HTPAFF4C44FRBZG"></a>
**§15** · 05-walking-and-the-leash/03-daily-walks.md › 5. Walking and the Leash — 5.3 Daily Walks

> An adult dog needs at least two walks a day: 30 to 60 minutes in total for small breeds and up to 2 hours for large and working breeds. A puppy must be taken outside to relieve itself every 2 to 3 hours. Always pick up your dog's waste and put it in a waste bin.

<a id="su_01M82ABDR28HTPAFF4C44FRBZJ"></a>
**§16** · 06-being-a-good-lead-for-your-dog.md › 6. Being a Good Lead for Your Dog

> Your dog looks to you for direction. Be its lead: a calm, consistent and confident leader whose signals it can trust.

<a id="su_01M82ABDR28HTPAFF4C44FRBZK"></a>
**§17** · 06-being-a-good-lead-for-your-dog.md › 6. Being a Good Lead for Your Dog

> Use the same command words every time, and make sure everyone in the family uses them too.

<a id="su_01M82ABDR28HTPAFF4C44FRBZM"></a>
**§18** · 06-being-a-good-lead-for-your-dog.md › 6. Being a Good Lead for Your Dog

> Set clear rules (for example, whether the dog may lie on the sofa) and keep them.

<a id="su_01M82ABDR28HTPAFF4C44FRBZN"></a>
**§19** · 06-being-a-good-lead-for-your-dog.md › 6. Being a Good Lead for Your Dog

> Reward good behaviour immediately; ignore unwanted behaviour instead of shouting.

<a id="su_01M82ABDR28HTPAFF4C44FRBZP"></a>
**§20** · 06-being-a-good-lead-for-your-dog.md › 6. Being a Good Lead for Your Dog

> A dog that does not see its owner as a reliable lead may become anxious or try to take control.

<a id="su_01M82ABDR28HTPAFF4C44FRBZR"></a>
**§21** · 07-training-and-commands.md › 7. Training and Commands

> Every dog should learn five basic commands: *sit*, *down*, *stay*, *come* and *leave it*. Train in short sessions of 5 to 10 minutes, several times a day, and always end with a success.

<a id="su_01M82ABDR28HTPAFF4C44FRBZS"></a>
**§22** · 07-training-and-commands.md › 7. Training and Commands

> A dog training course with a certified trainer is recommended in the first year. Dogs of breeds classified as dangerous must pass an obedience test.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX2"></a>
**§23** · 08-leaving-your-dog-alone.md › 8. Leaving Your Dog Alone

> Dogs are social animals. **Never leave an adult dog alone at home for more than 6 hours.** Puppies should not be left alone for more than 2 hours.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX3"></a>
**§24** · 08-leaving-your-dog-alone.md › 8. Leaving Your Dog Alone

> Before you leave, walk the dog, leave water and a safe chew toy, and keep your departure low-key. If your dog barks or howls while you are away, train it to be alone step by step, starting with a few minutes.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX5"></a>
**§25** · 09-travelling-with-your-dog.md › 9. Travelling with Your Dog

> In a car, a dog must travel in a crate or wear a safety harness attached to the seat belt. Never leave a dog in a parked car in warm weather. For travel abroad, your dog needs a pet passport, a microchip and a valid rabies vaccination.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX7"></a>
**§26** · 10-legal-obligations-and-responsibility.md › 10. Legal Obligations and Responsibility

> You are liable for any damage your dog causes. Third-party liability insurance for dog owners is strongly recommended, and it is mandatory for breeds classified as dangerous by the local authority. In public places, your dog must be kept on a leash unless a sign allows free running.
