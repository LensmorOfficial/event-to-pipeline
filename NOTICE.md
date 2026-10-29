# Licensing and source provenance

The existing 15 root-level Skills, repository material and newly authored documentation/helpers are covered by the root MIT license unless a file says otherwise.

The six generated research Skills under `mcp-skills/` are derived from Lensmor's canonical Agent Skills source, version `0.7.3`, whose declared license is ISC. Every generated Skill includes its own ISC `LICENSE`, including when copied by the installer. The bundled `research-exhibitors/scripts/` helper is MIT and carries its own license; this does not relicense the ISC instructions.

`mcp-skills/bundle-manifest.json` records source hashes, generated hashes and the reviewed transformation. It intentionally excludes private repository URLs, absolute maintainer paths, tokens and customer data. To regenerate it, a maintainer supplies a separately authorized canonical checkout using `scripts/build_mcp_bundle.py --source PATH`; end users do not need that checkout.

The public scope note limits this candidate to research and explains unbundled action handoffs. The exhibitor Skill additionally documents the optional public REST export helper. The canonical business instructions and UI dependency metadata are otherwise preserved. Review both licenses and the public file list before publishing a release. This repository does not grant access to Lensmor's private service implementation or data.
