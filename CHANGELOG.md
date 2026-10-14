# Changelog for ndx-optogenetics

## v0.4.1 (October 14, 2026)

- Capped the ndx-ophys-devices dependency at `<0.4`. ndx-ophys-devices 0.4.0 removes `FiberInsertion`, which the README example and migration guide use to describe where an `OpticalFiber` is inserted. ndx-optogenetics 0.5.0 will adopt ndx-ophys-devices 0.4.0. If you have pinned `ndx-optogenetics==0.4.0` and `from ndx_ophys_devices import FiberInsertion` fails with `ImportError: cannot import name 'FiberInsertion'`, upgrade with `pip install "ndx-optogenetics==0.4.1"`. The schema is unchanged apart from the namespace version. [PR #24](https://github.com/rly/ndx-optogenetics/pull/24)
- Updated the install command in the v0.2.0 to v0.3.0 migration guide to `ndx-optogenetics==0.4.1` and noted that the guide's code works with 0.4.x. [PR #25](https://github.com/rly/ndx-optogenetics/pull/25)

## v0.4.0 (February 6, 2026)

- Added `OptogeneticPulsesTable` to record individual optogenetic pulses for irregular pulse presentations. [PR #17](https://github.com/rly/ndx-optogenetics/pull/17)
- Made the `optical_fiber` field optional in the `OptogeneticSitesTable`. Not all experiments with optogenetic stimulation need an optical fiber to deliver the stimulus. [PR #21](https://github.com/rly/ndx-optogenetics/pull/21)

## v0.3.0 (September 23, 2025)

- Refactored the extension to depend on `ndx-ophys-devices` for device and biological component specification, replacing its previous standalone device types. Introduced the `OptogeneticSitesTable` to consolidate stimulation site metadata (excitation source, optical fiber, effector), updated the schema, API, docs, and tests accordingly, and improved modularity for optogenetic metadata. [PR #9](https://github.com/rly/ndx-optogenetics/pull/9)
- Added v0.2.0 to v0.3.0 migration guide. [PR #12](https://github.com/rly/ndx-optogenetics/pull/12)
- Updated requirements to depend on `ndx-ophys-devices>=0.3.1` [PR #14](https://github.com/rly/ndx-optogenetics/pull/14)
- Made the `OptogeneticViruses` and `OptogeneticVirusInjections` groups optional for the `OptogeneticExperimentMetadata` group [PR #5](https://github.com/rly/ndx-optogenetics/pull/5)
- Updated GitHub Actions workflows [PR #13](https://github.com/rly/ndx-optogenetics/pull/13)
