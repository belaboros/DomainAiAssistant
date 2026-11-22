# pets-and-house-rules · level 1

**Version:** raw+759da11 · **Release:** raw · This file holds level 1, the core of the domain.

Explain what it takes to own a dog or a cat in a residential complex, and which house rules apply to pets and their owners.

This is the raw release: it also holds elements that are not approved yet. They are marked
`● proposed` or `◐ waiting for approval`, and drawn dashed in the diagrams.

## Taxonomy

```mermaid
flowchart TB
    classDef draft stroke-dasharray: 5 5
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM["dog"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKV["dog registration"]
    cn_01M82AH1GXVV72WP99JQXMH6XS["dog waste"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW6["leash"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKS["local authority"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKT["microchip"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8["owner"]
    cn_01M82AH1GXVV72WP99JQXMH6XT["waste bin"]
    class cn_01M82AC66KMJH32E2MQ3Z7ZBKM,cn_01M82AC66KMJH32E2MQ3Z7ZBKV,cn_01M82AH1GXVV72WP99JQXMH6XS,cn_01M82AFTZDSHCD0SK6T4N2YZW6,cn_01M82AC66KMJH32E2MQ3Z7ZBKS,cn_01M82AC66KMJH32E2MQ3Z7ZBKT,cn_01M82AE56ZYS5Y2Z0C35ECC9Y8,cn_01M82AH1GXVV72WP99JQXMH6XT draft
```

## Concepts and relations

```mermaid
flowchart LR
    classDef draft stroke-dasharray: 5 5
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM["dog"]
    cn_01M82AH1GXVV72WP99JQXMH6XS["dog waste"]
    cn_01M82AFTZDSHCD0SK6T4N2YZW6["leash"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKS["local authority"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKT["microchip"]
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8["owner"]
    cn_01M82AH1GXVV72WP99JQXMH6XT["waste bin"]
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "is registered with" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKS
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "carries" .-> cn_01M82AC66KMJH32E2MQ3Z7ZBKT
    cn_01M82AC66KMJH32E2MQ3Z7ZBKM -. "is kept on" .-> cn_01M82AFTZDSHCD0SK6T4N2YZW6
    cn_01M82AE56ZYS5Y2Z0C35ECC9Y8 -. "picks up" .-> cn_01M82AH1GXVV72WP99JQXMH6XS
    cn_01M82AH1GXVV72WP99JQXMH6XS -. "is put in" .-> cn_01M82AH1GXVV72WP99JQXMH6XT
    class cn_01M82AC66KMJH32E2MQ3Z7ZBKM,cn_01M82AH1GXVV72WP99JQXMH6XS,cn_01M82AFTZDSHCD0SK6T4N2YZW6,cn_01M82AC66KMJH32E2MQ3Z7ZBKS,cn_01M82AC66KMJH32E2MQ3Z7ZBKT,cn_01M82AE56ZYS5Y2Z0C35ECC9Y8,cn_01M82AH1GXVV72WP99JQXMH6XT draft
```

## Concepts

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKM"></a>
### dog · ● proposed

A social animal.

- **Level:** 1
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8), [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9), [§4](#su_01M82ABDR1CAX5PFZ2HWSEQHBH), [§5](#su_01M82ABDR1CAX5PFZ2HWSEQHBK), [§6](#su_01M82ABDR1CAX5PFZ2HWSEQHBN), [§7](#su_01M82ABDR28HTPAFF4C44FRBZ9), [§9](#su_01M82ABDR28HTPAFF4C44FRBZE), [§10](#su_01M82ABDR28HTPAFF4C44FRBZG), [§11](#su_01M82ABDR28HTPAFF4C44FRBZJ), [§12](#su_01M82ABDR28HTPAFF4C44FRBZP), [§13](#su_01M82ABDR28HTPAFF4C44FRBZR), [§14](#su_01M82ABDR28HTPAFF4C44FRBZS), [§15](#su_01M82ABDR30PE47ZK8WSGY3HX2), [§16](#su_01M82ABDR30PE47ZK8WSGY3HX3), [§17](#su_01M82ABDR30PE47ZK8WSGY3HX5), [§18](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKV"></a>
### dog registration · ● proposed

- **Synonyms:** registered
- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="cn_01M82AH1GXVV72WP99JQXMH6XS"></a>
### dog waste · ● proposed

- **Synonyms:** waste
- **Level:** 1
- **Evidence:** [§10](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="cn_01M82AFTZDSHCD0SK6T4N2YZW6"></a>
### leash · ● proposed

- **Level:** 1
- **Evidence:** [§8](#su_01M82ABDR28HTPAFF4C44FRBZC), [§9](#su_01M82ABDR28HTPAFF4C44FRBZE), [§18](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKS"></a>
### local authority · ● proposed

- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9), [§3](#su_01M82ABDR1CAX5PFZ2HWSEQHBF), [§18](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AC66KMJH32E2MQ3Z7ZBKT"></a>
### microchip · ● proposed

- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9), [§17](#su_01M82ABDR30PE47ZK8WSGY3HX5)

<a id="cn_01M82AE56ZYS5Y2Z0C35ECC9Y8"></a>
### owner · ● proposed

- **Synonyms:** dog owner
- **Level:** 1
- **Evidence:** [§5](#su_01M82ABDR1CAX5PFZ2HWSEQHBK), [§10](#su_01M82ABDR28HTPAFF4C44FRBZG), [§12](#su_01M82ABDR28HTPAFF4C44FRBZP), [§16](#su_01M82ABDR30PE47ZK8WSGY3HX3), [§18](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="cn_01M82AH1GXVV72WP99JQXMH6XT"></a>
### waste bin · ● proposed

- **Level:** 1
- **Evidence:** [§10](#su_01M82ABDR28HTPAFF4C44FRBZG)

## Relations

<a id="rl_01M82AC66KMJH32E2MQ3Z7ZBM1"></a>
### carries · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — carries → [microchip](#cn_01M82AC66KMJH32E2MQ3Z7ZBKT)
- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="rl_01M82AM9P6EWS5D1VJCAH8Z7VM"></a>
### is kept on · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — is kept on → [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6)
- **Level:** 1
- **Evidence:** [§18](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="rl_01M82AM9P6EWS5D1VJCAH8Z7VH"></a>
### is liable for · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — is liable for → damage
- **Level:** 1
- **Evidence:** [§18](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="rl_01M82AH1GXVV72WP99JQXMH6XY"></a>
### is put in · ● proposed

- [dog waste](#cn_01M82AH1GXVV72WP99JQXMH6XS) — is put in → [waste bin](#cn_01M82AH1GXVV72WP99JQXMH6XT)
- **Level:** 1
- **Evidence:** [§10](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="rl_01M82AC66KMJH32E2MQ3Z7ZBM0"></a>
### is registered with · ● proposed

- [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM) — is registered with → [local authority](#cn_01M82AC66KMJH32E2MQ3Z7ZBKS)
- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="rl_01M82AH1GXVV72WP99JQXMH6XX"></a>
### picks up · ● proposed

- [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8) — picks up → [dog waste](#cn_01M82AH1GXVV72WP99JQXMH6XS)
- **Level:** 1
- **Evidence:** [§10](#su_01M82ABDR28HTPAFF4C44FRBZG)

## Rules

<a id="ru_01M82AH1GXVV72WP99JQXMH6Y3"></a>
### Always pick up dog waste and put it in a waste bin · ● proposed

owner **must** always pick up the dog's waste and put it in a waste bin

- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), [dog waste](#cn_01M82AH1GXVV72WP99JQXMH6XS), [waste bin](#cn_01M82AH1GXVV72WP99JQXMH6XT), [picks up](#rl_01M82AH1GXVV72WP99JQXMH6XX), [is put in](#rl_01M82AH1GXVV72WP99JQXMH6XY)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§10](#su_01M82ABDR28HTPAFF4C44FRBZG)

<a id="ru_01M82AC66KMJH32E2MQ3Z7ZBM4"></a>
### Dog microchip · ● proposed

dog owner **must** ensure the dog carries a microchip

- **When:** the dog is older than 4 months
- **Limit:** &gt; 4 months
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [microchip](#cn_01M82AC66KMJH32E2MQ3Z7ZBKT), [carries](#rl_01M82AC66KMJH32E2MQ3Z7ZBM1)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="ru_01M82AC66KMJH32E2MQ3Z7ZBM3"></a>
### Dog registration · ● proposed

dog owner **must** register the dog with the local authority

- **When:** the dog is older than 4 months
- **Limit:** &gt; 4 months
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [local authority](#cn_01M82AC66KMJH32E2MQ3Z7ZBKS), [dog registration](#cn_01M82AC66KMJH32E2MQ3Z7ZBKV), [is registered with](#rl_01M82AC66KMJH32E2MQ3Z7ZBM0)
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§2](#su_01M82ABDR1CAX5PFZ2HWSEQHB9)

<a id="ru_01M82AM9P6EWS5D1VJCAH8Z7VT"></a>
### Leash in public places · ● proposed

dog owner **must** keep the dog on a leash in public places

- **When:** unless a sign allows free running
- **Refers to:** [dog](#cn_01M82AC66KMJH32E2MQ3Z7ZBKM), [leash](#cn_01M82AFTZDSHCD0SK6T4N2YZW6), public place, free-running sign, [is kept on](#rl_01M82AM9P6EWS5D1VJCAH8Z7VM), is located in
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§18](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="ru_01M82AM9P6EWS5D1VJCAH8Z7VQ"></a>
### Owner is liable for dog damage · ● proposed

dog owner **must** be liable for any damage the dog causes

- **Refers to:** [owner](#cn_01M82AE56ZYS5Y2Z0C35ECC9Y8), damage, [is liable for](#rl_01M82AM9P6EWS5D1VJCAH8Z7VH), causes
- **Applies to:** co_01M82ABDR0997QP7DGZPPDNF4H
- **Level:** 1
- **Evidence:** [§18](#su_01M82ABDR30PE47ZK8WSGY3HX7)

## Properties

_None at this level._

## Statements

<a id="st_01M82AC66KMJH32E2MQ3Z7ZBK7"></a>
### Dog lifespan · ● proposed

A dog lives 10 to 15 years.

- **Level:** 1
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

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

<a id="st_01M82AM9P6EWS5D1VJCAH8Z7TY"></a>
### Leash in public places · ● proposed

In public places, a dog must be kept on a leash unless a sign allows free running.

- **Level:** 1
- **Evidence:** [§18](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="st_01M82AC66KMJH32E2MQ3Z7ZBK8"></a>
### Lifelong needs of a dog · ● proposed

A dog needs daily exercise, company, training and veterinary care for its whole life.

- **Level:** 1
- **Evidence:** [§1](#su_01M82ABDR1CAX5PFZ2HWSEQHB8)

<a id="st_01M82AM9P5HMXJKJ1997DWSW20"></a>
### Owner liable for dog damage · ● proposed

The dog owner is liable for any damage the dog causes.

- **Level:** 1
- **Evidence:** [§18](#su_01M82ABDR30PE47ZK8WSGY3HX7)

<a id="st_01M82AH1GXVV72WP99JQXMH6X9"></a>
### Pick up dog waste · ● proposed

The owner must always pick up the dog's waste and put it in a waste bin.

- **Level:** 1
- **Evidence:** [§10](#su_01M82ABDR28HTPAFF4C44FRBZG)

## Evidence

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHB8"></a>
**§1** · 01-before-you-get-a-dog.md › 1. Before You Get a Dog

> A dog lives 10 to 15 years. It needs daily exercise, company, training and veterinary care for its whole life. Before you get a dog, check that your home, your working hours and your budget fit the dog you want.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHB9"></a>
**§2** · 01-before-you-get-a-dog.md › 1. Before You Get a Dog

> A dog older than 4 months must be registered with the local authority and must carry a microchip.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBF"></a>
**§3** · 02-choosing-a-breed.md › 2. Choosing a Breed

> Some breeds are classified as dangerous by the local authority. Check the local list before you choose a breed.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBH"></a>
**§4** · 03-health-and-care/01-feeding.md › 3. Health and Care — 3.1 Feeding

> Feed an adult dog twice a day and a puppy three to four times a day. Fresh water must always be available. Chocolate, grapes, onions and xylitol are poisonous to dogs.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBK"></a>
**§5** · 03-health-and-care/02-vaccination-and-the-veterinarian.md › 3. Health and Care — 3.2 Vaccination and the Veterinarian

> A puppy receives its first vaccinations at 8 weeks of age. The rabies vaccination is mandatory and must be renewed every year. Take your dog to the veterinarian for a check-up at least once a year.

<a id="su_01M82ABDR1CAX5PFZ2HWSEQHBN"></a>
**§6** · 03-health-and-care/03-grooming-and-hygiene.md › 3. Health and Care — 3.3 Grooming and Hygiene

> Brush your dog at least once a week; long-haired breeds need brushing every day. Trim the claws when you can hear them clicking on the floor. Wash your dog's bed and blankets once a week at 60 °C.

<a id="su_01M82ABDR28HTPAFF4C44FRBZ9"></a>
**§7** · 04-puppy-basics.md › 4. Puppy Basics

> A puppy is a dog younger than 6 months. Puppies should not leave their mother before 8 weeks of age.

<a id="su_01M82ABDR28HTPAFF4C44FRBZC"></a>
**§8** · 05-walking-and-the-leash/01-choosing-a-leash.md › 5. Walking and the Leash — 5.1 Choosing a Leash

> Use a leash of 1.5 to 2 metres for everyday walks. A retractable leash is not suitable in busy streets. Attach the leash to a well-fitting collar or harness: you should be able to slide two fingers under the collar.

<a id="su_01M82ABDR28HTPAFF4C44FRBZE"></a>
**§9** · 05-walking-and-the-leash/02-leash-training.md › 5. Walking and the Leash — 5.2 Leash Training

> Start leash training when the puppy is 8 to 10 weeks old. Reward the dog when the leash is loose, and stop walking when the dog pulls. Never jerk the leash.

<a id="su_01M82ABDR28HTPAFF4C44FRBZG"></a>
**§10** · 05-walking-and-the-leash/03-daily-walks.md › 5. Walking and the Leash — 5.3 Daily Walks

> An adult dog needs at least two walks a day: 30 to 60 minutes in total for small breeds and up to 2 hours for large and working breeds. A puppy must be taken outside to relieve itself every 2 to 3 hours. Always pick up your dog's waste and put it in a waste bin.

<a id="su_01M82ABDR28HTPAFF4C44FRBZJ"></a>
**§11** · 06-being-a-good-lead-for-your-dog.md › 6. Being a Good Lead for Your Dog

> Your dog looks to you for direction. Be its lead: a calm, consistent and confident leader whose signals it can trust.

<a id="su_01M82ABDR28HTPAFF4C44FRBZP"></a>
**§12** · 06-being-a-good-lead-for-your-dog.md › 6. Being a Good Lead for Your Dog

> A dog that does not see its owner as a reliable lead may become anxious or try to take control.

<a id="su_01M82ABDR28HTPAFF4C44FRBZR"></a>
**§13** · 07-training-and-commands.md › 7. Training and Commands

> Every dog should learn five basic commands: *sit*, *down*, *stay*, *come* and *leave it*. Train in short sessions of 5 to 10 minutes, several times a day, and always end with a success.

<a id="su_01M82ABDR28HTPAFF4C44FRBZS"></a>
**§14** · 07-training-and-commands.md › 7. Training and Commands

> A dog training course with a certified trainer is recommended in the first year. Dogs of breeds classified as dangerous must pass an obedience test.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX2"></a>
**§15** · 08-leaving-your-dog-alone.md › 8. Leaving Your Dog Alone

> Dogs are social animals. **Never leave an adult dog alone at home for more than 6 hours.** Puppies should not be left alone for more than 2 hours.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX3"></a>
**§16** · 08-leaving-your-dog-alone.md › 8. Leaving Your Dog Alone

> Before you leave, walk the dog, leave water and a safe chew toy, and keep your departure low-key. If your dog barks or howls while you are away, train it to be alone step by step, starting with a few minutes.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX5"></a>
**§17** · 09-travelling-with-your-dog.md › 9. Travelling with Your Dog

> In a car, a dog must travel in a crate or wear a safety harness attached to the seat belt. Never leave a dog in a parked car in warm weather. For travel abroad, your dog needs a pet passport, a microchip and a valid rabies vaccination.

<a id="su_01M82ABDR30PE47ZK8WSGY3HX7"></a>
**§18** · 10-legal-obligations-and-responsibility.md › 10. Legal Obligations and Responsibility

> You are liable for any damage your dog causes. Third-party liability insurance for dog owners is strongly recommended, and it is mandatory for breeds classified as dangerous by the local authority. In public places, your dog must be kept on a leash unless a sign allows free running.
