# Changelog for ndx-optogenetics

# v0.3.0 (Upcoming)

## Fixed
- Fixed compatibility of `ExcitationSourceModel` and `OpticalFiberModel` with PyNWB 3.1.0 and later. `ExcitationSourceModel` and `OpticalFiberModel` now inherit from `DeviceModel` instead of `Device` [PR #11](https://github.com/rly/ndx-optogenetics/pull/11). This aligns with the usage of the new `DeviceModel` class in PyNWB 3.1.0 (NWB schema 2.9.0) and later. Importantly, this change requires users to update their code to use `add_device_model` instead of `add_device` when adding these models to an NWB file.

## Changed
- Made the `OptogeneticViruses` and `OptogeneticVirusInjections` groups optional for the `OptogeneticExperimentMetadata` group [PR #5](https://github.com/rly/ndx-optogenetics/pull/5).