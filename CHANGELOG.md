# Changelog for ndx-optogenetics

# v0.3.0 (Upcoming)

- Refactored the extension to depend on ndx-ophys-devices for device and biological component specification, replacing its previous standalone device types. Introduced the OptogeneticSitesTable to consolidate stimulation site metadata (excitation source, optical fiber, effector), updated the schema, API, docs, and tests accordingly, and improved modularity for optogenetic metadata. [PR #9](https://github.com/rly/ndx-optogenetics/pull/9)

# v0.2.1 (Upcoming)

## Improvements

- Made the `OptogeneticViruses` and `OptogeneticVirusInjections` groups optional for the `OptogeneticExperimentMetadata` group [PR #5](https://github.com/rly/ndx-optogenetics/pull/5).