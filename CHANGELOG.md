# Changelog for ndx-optogenetics

## v0.4.0 (February 6, 2026)

- Added `OptogeneticPulsesTable` to record individual optogenetic pulses for irregular pulse presentations. [PR #17](https://github.com/rly/ndx-optogenetics/pull/17)

## v0.3.0 (September 23, 2025)

- Refactored the extension to depend on `ndx-ophys-devices` for device and biological component specification, replacing its previous standalone device types. Introduced the `OptogeneticSitesTable` to consolidate stimulation site metadata (excitation source, optical fiber, effector), updated the schema, API, docs, and tests accordingly, and improved modularity for optogenetic metadata. [PR #9](https://github.com/rly/ndx-optogenetics/pull/9)
- Added v0.2.0 to v0.3.0 migration guide. [PR #12](https://github.com/rly/ndx-optogenetics/pull/12)
- Updated requirements to depend on `ndx-ophys-devices>=0.3.1` [PR #14](https://github.com/rly/ndx-optogenetics/pull/14)
- Made the `OptogeneticViruses` and `OptogeneticVirusInjections` groups optional for the `OptogeneticExperimentMetadata` group [PR #5](https://github.com/rly/ndx-optogenetics/pull/5)
- Updated GitHub Actions workflows [PR #13](https://github.com/rly/ndx-optogenetics/pull/13)
