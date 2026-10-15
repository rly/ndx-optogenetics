# Changelog for ndx-optogenetics

## v0.5.0 (Upcoming)

- Updated requirements to depend on `ndx-ophys-devices>=0.4.0,<0.5`. ndx-ophys-devices 0.4.0 replaces `FiberInsertion` and the coordinate fields of `ViralVectorInjection` with a `StereotacticPosition` group. Coordinates now describe the target (fiber tip or injection site) in the system given by `origin` and `orientation`:
  - `OpticalFiber.fiber_insertion` is now a `StereotacticPosition` and is optional. With `orientation="RAS"`, `insertion_position_ml_in_mm` becomes `x_in_mm`, `insertion_position_ap_in_mm` becomes `y_in_mm`, `insertion_position_dv_in_mm` becomes `z_in_mm`, `position_reference` becomes `origin`, and `insertion_angle_{pitch,yaw,roll}_in_deg` become `{pitch,yaw,roll}_in_deg`. `depth_in_mm` and `hemisphere` have no equivalent; the hemisphere follows from the sign of the ML coordinate.
  - `ViralVectorInjection` coordinates move into the optional `viral_injection_coordinates` group. `location` becomes `anatomical_target`, `reference` becomes `origin`, and `ml_in_mm`, `ap_in_mm` and `dv_in_mm` become `x_in_mm`, `y_in_mm` and `z_in_mm` with `orientation="RAS"`. `hemisphere` has no equivalent.
- Files written with ndx-optogenetics 0.4.0 or earlier cache ndx-ophys-devices 0.3.x and cannot be read in a Python session that has imported ndx-optogenetics 0.5.0 or ndx-ophys-devices 0.4.0. Open them in a session that does not import these packages; pynwb then loads the cached namespaces.
- Code that still imports `FiberInsertion` from ndx-ophys-devices, such as trodes_to_nwb, fails with ndx-optogenetics 0.5.0 until it is updated. Until then, install `"ndx-optogenetics<0.5"`, which resolves to 0.4.1 and ndx-ophys-devices 0.3.1.
- Dropped support for Python 3.9 and added Python 3.14 to the test matrix.
- Fixed example values in the README and tests: the excitation source intensity now matches 77 mW through a 200 um core, and `intertrain_interval_in_ms` is NaN for a single train. The test now writes to a temporary directory.

## v0.4.1 (October 14, 2026)

The schema is unchanged apart from the namespace version.

- Capped the ndx-ophys-devices dependency at `<0.4` because ndx-ophys-devices 0.4.0 removes `FiberInsertion`. If you use ndx-optogenetics 0.4.0, upgrade to 0.4.1. [PR #24](https://github.com/rly/ndx-optogenetics/pull/24)
- Updated the migration guide to install 0.4.1. [PR #25](https://github.com/rly/ndx-optogenetics/pull/25)

## v0.4.0 (February 6, 2026)

- Added `OptogeneticPulsesTable` to record individual optogenetic pulses for irregular pulse presentations. [PR #17](https://github.com/rly/ndx-optogenetics/pull/17)
- Made the `optical_fiber` field optional in the `OptogeneticSitesTable`. Not all experiments with optogenetic stimulation need an optical fiber to deliver the stimulus. [PR #21](https://github.com/rly/ndx-optogenetics/pull/21)

## v0.3.0 (September 23, 2025)

- Refactored the extension to depend on `ndx-ophys-devices` for device and biological component specification, replacing its previous standalone device types. Introduced the `OptogeneticSitesTable` to consolidate stimulation site metadata (excitation source, optical fiber, effector), updated the schema, API, docs, and tests accordingly, and improved modularity for optogenetic metadata. [PR #9](https://github.com/rly/ndx-optogenetics/pull/9)
- Added v0.2.0 to v0.3.0 migration guide. [PR #12](https://github.com/rly/ndx-optogenetics/pull/12)
- Updated requirements to depend on `ndx-ophys-devices>=0.3.1` [PR #14](https://github.com/rly/ndx-optogenetics/pull/14)
- Made the `OptogeneticViruses` and `OptogeneticVirusInjections` groups optional for the `OptogeneticExperimentMetadata` group [PR #5](https://github.com/rly/ndx-optogenetics/pull/5)
- Updated GitHub Actions workflows [PR #13](https://github.com/rly/ndx-optogenetics/pull/13)
