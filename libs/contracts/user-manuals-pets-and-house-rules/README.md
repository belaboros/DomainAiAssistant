# Dataset contract: user-manuals-pets-and-house-rules

| | |
|---|---|
| **Description** | Dog owner's, cat owner's and building rules manuals, one Markdown file per chapter, with seeded quality issues for testing a manual assistant. |
| **Owner (only writer)** | `generate-pets-and-building-user-manual` |
| **Readers** | see the system map in the [root architecture](../../../docs/architecture/architecture.md) |
| **Location at runtime** | `${SHARED_DATA_DIR}/user-manuals-pets-and-house-rules/` (`SHARED_DATA_DIR` comes from the root `.env`) |
| **In git** | commit: see `git` in the root `components.json` and `.gitignore` (ADR-0016) |
| **Contract version** | 0.1.0 (see [CHANGELOG.md](CHANGELOG.md)) |

The contract is what readers may rely on (ADR-0013). Anything not written here is an implementation detail of `generate-pets-and-building-user-manual` and may change without notice.

## Format

Plain Markdown files (UTF-8), one per chapter, under three manual folders:

```
user-manuals-pets-and-house-rules/
├── dog-owners-manual/
├── cat-owners-manual/
└── building-and-house-rules/
```

- **Chapter:** a file `NN-kebab-slug.md`, or, for a chapter with sub-chapters, a folder `NN-kebab-slug/` holding sub-chapter files `NN-kebab-slug.md`. `NN` is two digits, starting at `01`. A chapter folder has no file of its own.
- **Heading:** each file starts with exactly one level-1 heading: `# N. Title` for a chapter, `# N. Chapter Title — N.M Sub-chapter Title` for a sub-chapter. The numbers in the heading match the `NN` prefixes of the path.
- **Body:** prose and bullet lists; no front matter, no images, no links between files.
- **Size:** each manual has 8 to 12 chapters, of which 1 or 2 are folders holding 2 or 3 sub-chapter files.

## Guarantees

- The three manual folder names never change within a major version.
- The manual folders contain only chapter files and chapter folders as described above: no README, index or answer key. The answer key with the seeded issues lives outside the dataset, in `docs/research/notes/pet-manuals-corpus/`, so that readers under test cannot see it.
- The path of a chapter file is its identifier (for example `dog-owners-manual/05-walking-and-the-leash/03-daily-walks.md`). The section number in its heading (`5.3`) is its citation label.
- The content contains deliberate quality issues (a gap, a terminology drift, a contradiction). Readers must not treat the manuals as consistent.
- The files are written by hand or by an LLM following `apps/generate-pets-and-building-user-manual/instructions/generation-instructions.md`, and committed to git; there is no runtime writer.

## Versioning

Semantic versioning of the contract: **major** for anything that can break a reader (removed or renamed fields, changed meaning), **minor** for additions readers can ignore, **patch** for clarifications. A major change needs a root ADR and a plan for every reader listed in the system map.
