# Migration Guide: ndx-optogenetics v0.2.0 to v0.3.0

This guide provides detailed instructions for migrating from ndx-optogenetics version 0.2.0 to version 0.3.0. Version 0.3.0 introduces significant architectural changes that improve modularity and coordination with the [ndx-ophys-devices](https://github.com/catalystneuro/ndx-ophys-devices/) extension,
which is being reviewed by the NWB Technical Advisory Board for [integration with the core NWB standard](https://github.com/nwb-extensions/nwbep-review/issues/6) and which is used in [ndx-microscopy](https://github.com/catalystneuro/ndx-microscopy/) and will be used in [ndx-fiber-photometry](https://github.com/catalystneuro/ndx-fiber-photometry/pull/37).

## Overview of Changes

Version 0.3.0 represents a major refactoring that:

1. **Introduces dependency on ndx-ophys-devices**: Device and biological component specifications are now handled by the ndx-ophys-devices extension
2. **Consolidates location tracking**: Replaces `OpticalFiberLocationsTable` with `OptogeneticSitesTable` and `FiberInsertion` for better organization and cross-linking
3. **Updates virus/injection handling**: Uses `ViralVector`, `ViralVectorInjection`, and `Effector` from ndx-ophys-devices
4. **Enhances epochs table**: Adds excitation wavelength tracking per-epoch and new link to rows of the `OptogeneticSitesTable`

## Breaking Changes

### 1. New Dependency: ndx-ophys-devices

**Before (v0.2.0):**
```python
from ndx_optogenetics import (
    ExcitationSourceModel,
    ExcitationSource,
    OpticalFiberModel,
    OpticalFiber,
    OptogeneticVirus,
    OptogeneticVirusInjection,
    # ... other imports
)
```

**After (v0.3.0):**
```python
# Device and biological components now come from ndx-ophys-devices
from ndx_ophys_devices import (
    ExcitationSourceModel,
    ExcitationSource,
    OpticalFiberModel,
    OpticalFiber,
    FiberInsertion,
    ViralVector,
    ViralVectorInjection,
    Effector,
)

# Optogenetics-specific components still come from ndx-optogenetics
from ndx_optogenetics import (
    OptogeneticSitesTable,
    OptogeneticViruses,
    OptogeneticVirusInjections,
    OptogeneticEffectors,
    OptogeneticExperimentMetadata,
    OptogeneticEpochsTable,
)
```

### 2. ExcitationSourceModel Changes

**Before (v0.2.0):**
```python
excitation_source_model = ExcitationSourceModel(
    name="Omicron LuxX+ 488-100 Model",
    description="Laser for optogenetic stimulation.",
    manufacturer="Omicron",
    illumination_type="laser",  # OLD ATTRIBUTE
    wavelength_range_in_nm=[488.0, 488.0],
)
```

**After (v0.3.0):**
```python
# New ExcitationSourceModel class from ndx-ophys-devices
excitation_source_model = ExcitationSourceModel(
    name="Omicron LuxX+ 488-100 Model",
    description="Laser for optogenetic stimulation.",
    manufacturer="Omicron",
    source_type="laser",  # NEW ATTRIBUTE NAME
    excitation_mode="one-photon",  # NEW ATTRIBUTE
    wavelength_range_in_nm=[488.0, 488.0],
)
```

### 3. ExcitationSource Changes

**Before (v0.2.0):**
```python
excitation_source = ExcitationSource(
    name="Omicron LuxX+ 488-100",
    model=excitation_source_model,
    wavelength_in_nm=488.0,  # REMOVED
    power_in_W=0.077,
    intensity_in_W_per_m2=1.0e10,
)
```

**After (v0.3.0):**
```python
# New ExcitationSource class from ndx-ophys-devices
excitation_source = ExcitationSource(
    name="Omicron LuxX+ 488-100",
    model=excitation_source_model,
    # wavelength_in_nm removed - now specified in epochs table
    power_in_W=0.077,
    intensity_in_W_per_m2=1.0e10,
)
```

### 4. OpticalFiberModel Changes

**Before (v0.2.0):**
```python
optical_fiber_model = OpticalFiberModel(
    name="Lambda Model",
    description="Lambda fiber (tapered fiber) from Optogenix.",
    fiber_name="Lambda",  # REMOVED
    fiber_model="lambda_b5",  # RENAMED
    manufacturer="Optogenix",
    numerical_aperture=0.39,
    core_diameter_in_um=200.0,
    active_length_in_mm=2.0,
    ferrule_name="cFCF - ∅2.5mm Ceramic Ferrule",
    ferrule_model="FC-PC-2.5",
    ferrule_diameter_in_mm=2.5,
)
```

**After (v0.3.0):**
```python
# New OpticalFiberModel class from ndx-ophys-devices
optical_fiber_model = OpticalFiberModel(
    name="Lambda Model",
    description="Lambda fiber (tapered fiber) from Optogenix.",
    # fiber_name removed - use just the name of this object
    model_number="lambda_b5",  # renamed from fiber_model
    manufacturer="Optogenix",
    numerical_aperture=0.39,
    core_diameter_in_um=200.0,
    active_length_in_mm=2.0,
    ferrule_name="cFCF - ∅2.5mm Ceramic Ferrule",
    ferrule_model="FC-PC-2.5",
    ferrule_diameter_in_mm=2.5,
)
```

### 5. OpticalFiber Changes and OpticalFiberLocationsTable Migration

**Important**: The location data that was previously stored in `OpticalFiberLocationsTable` in v0.2.0 now goes into `FiberInsertion` objects in v0.3.0. The linking between excitation source and optical fiber is now done through the `OptogeneticSitesTable`.

**Before (v0.2.0):**
```python
# Simple fiber object - location data stored separately in OpticalFiberLocationsTable
optical_fiber = OpticalFiber(
    name="Lambda",
    model=optical_fiber_model,
)

optical_fiber_locations_table = OpticalFiberLocationsTable(
    description="Information about implanted optical fiber locations",
    reference="Bregma at the cortical surface",  # MOVES to FiberInsertion.position_reference
)

optical_fiber_locations_table.add_row(
    implanted_fiber_description="Lambda fiber implanted into right GPe.",  # MOVES to OpticalFiber.description
    location="GPe",
    hemisphere="right",   # MOVES to FiberInsertion.hemisphere
    ap_in_mm=-1.5,        # MOVES to FiberInsertion.insertion_position_ap_in_mm
    ml_in_mm=3.2,         # MOVES to FiberInsertion.insertion_position_ml_in_mm
    dv_in_mm=-5.8,        # MOVES to FiberInsertion.insertion_position_dv_in_mm
    roll_in_deg=0.0,      # MOVES to FiberInsertion.insertion_angle_roll_in_deg
    pitch_in_deg=0.0,     # MOVES to FiberInsertion.insertion_angle_pitch_in_deg
    yaw_in_deg=0.0,       # MOVES to FiberInsertion.insertion_angle_yaw_in_deg
    excitation_source=excitation_source,
    optical_fiber=optical_fiber,
)
```

**After (v0.3.0):**
```python
# New FiberInsertion class from ndx-ophys-devices that contains the fiber location data
fiber_insertion = FiberInsertion(
    name="fiber_insertion",
    insertion_position_ap_in_mm=-1.5,  # from ap_in_mm
    insertion_position_ml_in_mm=3.2,   # from ml_in_mm
    insertion_position_dv_in_mm=-5.8,  # from dv_in_mm
    position_reference="Bregma at the cortical surface",  # from table reference
    hemisphere="right",  # from hemisphere
    insertion_angle_roll_in_deg=0.0,  # from roll_in_deg
    insertion_angle_pitch_in_deg=0.0,  # from pitch_in_deg
    insertion_angle_yaw_in_deg=0.0,  # from yaw_in_deg
    depth_in_mm=5.8,  # NEW OPTIONAL ATTRIBUTE. If the angles are 0, this should be -1 * dv_in_mm
)

# New OpticalFiber class from ndx-ophys-devices
optical_fiber = OpticalFiber(
    name="Lambda",
    description="Lambda fiber implanted into right GPe.",  # from OpticalFiberLocationsTable.implanted_fiber_description
    model=optical_fiber_model,
    fiber_insertion=fiber_insertion,  # NEW REQUIRED ATTRIBUTE - contains the location data
)
```

When migrating from v0.2.0 to v0.3.0, take the coordinate and location data from each row in your `OpticalFiberLocationsTable` and use it to create `FiberInsertion` objects that get attached to your `OpticalFiber` instances. The `OptogeneticSitesTable` is then used only to link these fibers with their corresponding excitation sources and effectors.


### 6. OpticalFiberLocationsTable → OptogeneticSitesTable

See also Section 5. "OpticalFiber Changes and OpticalFiberLocationsTable Migration" above.

**Before (v0.2.0):**
```python
optical_fiber_locations_table = OpticalFiberLocationsTable(
    description="Information about implanted optical fiber locations",
    reference="Bregma at the cortical surface",
)
optical_fiber_locations_table.add_row(
    implanted_fiber_description="Lambda fiber implanted into right GPe.",
    location="GPe",
    hemisphere="right",
    ap_in_mm=-1.5,
    ml_in_mm=3.2,
    dv_in_mm=-5.8,
    roll_in_deg=0.0,
    pitch_in_deg=0.0,
    yaw_in_deg=0.0,
    excitation_source=excitation_source,  # This linkage moves to OptogeneticSitesTable
    optical_fiber=optical_fiber,  # This linkage moves to OptogeneticSitesTable
)
```

**After (v0.3.0):**
```python
# New table that consolidates all site information
optogenetic_sites_table = OptogeneticSitesTable(
    description="Information about the optogenetic stimulation sites."
)
optogenetic_sites_table.add_row(
    excitation_source=excitation_source,
    optical_fiber=optical_fiber,
    effector=effector,  # NEW REQUIRED reference to effector
)
```


### 7. Virus and Injection Changes

**Before (v0.2.0):**
```python
# Old virus class
virus = OptogeneticVirus(
    name="AAV-EF1a-DIO-hChR2(H134R)-EYFP",
    construct_name="AAV-EF1a-DIO-hChR2(H134R)-EYFP",
    description="Excitatory optogenetic construct for ChR2-EYFP expression",
    manufacturer="UNC Vector Core",
    titer_in_vg_per_ml=1.0e12,
)

# Old injection class
virus_injection = OptogeneticVirusInjection(
    name="AAV-EF1a-DIO-hChR2(H134R)-EYFP Injection",
    description="AAV-EF1a-DIO-hChR2(H134R)-EYFP injection into GPe.",
    hemisphere="right",
    location="GPe",
    ap_in_mm=-1.5,
    ml_in_mm=3.2,
    dv_in_mm=-6.0,
    # ... other coordinates
    virus=virus,  # OLD ATTRIBUTE NAME
    volume_in_uL=0.45,
    injection_date="1970-01-01T00:00:00+00:00",
)
```

**After (v0.3.0):**
```python
# New ViralVector class from ndx-ophys-devices. All fields are the same as in OptogeneticVirus
virus = ViralVector(
    name="AAV-EF1a-DIO-hChR2(H134R)-EYFP",
    construct_name="AAV-EF1a-DIO-hChR2(H134R)-EYFP",
    description="Excitatory optogenetic construct for ChR2-EYFP expression",
    manufacturer="UNC Vector Core",
    titer_in_vg_per_ml=1.0e12,
)

# New ViralVectorInjection class from ndx-ophys-devices. Almost all fields are the same as in OptogeneticVirusInjection
virus_injection = ViralVectorInjection(
    name="AAV-EF1a-DIO-hChR2(H134R)-EYFP Injection",
    description="AAV-EF1a-DIO-hChR2(H134R)-EYFP injection into GPe.",
    hemisphere="right",
    location="GPe",
    ap_in_mm=-1.5,
    ml_in_mm=3.2,
    dv_in_mm=-6.0,
    # ... other coordinates
    viral_vector=virus,  # NEW ATTRIBUTE NAME
    volume_in_uL=0.45,
    injection_date="1970-01-01T00:00:00+00:00",
)
```

### 8. Container Changes

**Before (v0.2.0):**
```python
optogenetic_viruses = OptogeneticViruses(optogenetic_virus=[virus])
optogenetic_virus_injections = OptogeneticVirusInjections(
    optogenetic_virus_injections=[virus_injection]
)
```

**After (v0.3.0):**
```python
optogenetic_viruses = OptogeneticViruses(viral_vectors=[virus])  # NEW ATTRIBUTE NAME
optogenetic_virus_injections = OptogeneticVirusInjections(
    viral_vector_injections=[virus_injection]  # NEW ATTRIBUTE NAME
)

# NEW: Effector container from ndx-ophys-devices that links to ViralVectorInjection
effector = Effector(
    name="effector",
    description="Excitatory opsin",
    label="hChR2-EYFP",
    viral_vector_injection=virus_injection,
)
optogenetic_effectors = OptogeneticEffectors(effectors=[effector])
```

### 9. OptogeneticExperimentMetadata Changes

**Before (v0.2.0):**
```python
optogenetic_experiment_metadata = OptogeneticExperimentMetadata(
    optical_fiber_locations_table=optical_fiber_locations_table,  # OLD
    optogenetic_viruses=optogenetic_viruses,  # REQUIRED in v0.2.0
    optogenetic_virus_injections=optogenetic_virus_injections,  # REQUIRED in v0.2.0
    stimulation_software="FSGUI 2.0",
)
```

**After (v0.3.0):**
```python
optogenetic_experiment_metadata = OptogeneticExperimentMetadata(
    optogenetic_sites_table=optogenetic_sites_table,  # NEW
    optogenetic_viruses=optogenetic_viruses,  # NOW OPTIONAL
    optogenetic_virus_injections=optogenetic_virus_injections,  # NOW OPTIONAL
    optogenetic_effectors=optogenetic_effectors,  # NEW (see Section 8 above)
    stimulation_software="FSGUI 2.0",
)
```

### 10. OptogeneticEpochsTable Changes

**Before (v0.2.0):**
```python
opto_epochs_table = OptogeneticEpochsTable(
    name="optogenetic_epochs",
    description="Metadata about optogenetic stimulation parameters per epoch",
    target_tables={"optical_fiber_locations": optical_fiber_locations_table},  # OLD
)
opto_epochs_table.add_row(
    start_time=0.0,
    stop_time=100.0,
    stimulation_on=True,
    pulse_length_in_ms=40.0,
    period_in_ms=250.0,
    number_pulses_per_pulse_train=100,
    number_trains=1,
    intertrain_interval_in_ms=0.0,
    power_in_mW=77.0,
)
```

**After (v0.3.0):**
```python
opto_epochs_table = OptogeneticEpochsTable(
    name="optogenetic_epochs",
    description="Metadata about optogenetic stimulation parameters per epoch",
    target_tables={"optogenetic_sites": optogenetic_sites_table},  # NEW
)
opto_epochs_table.add_row(
    start_time=0.0,
    stop_time=100.0,
    stimulation_on=True,
    pulse_length_in_ms=40.0,
    period_in_ms=250.0,
    number_pulses_per_pulse_train=100,
    number_trains=1,
    intertrain_interval_in_ms=0.0,
    power_in_mW=77.0,
    wavelength_in_nm=488.0,  # NEW: Wavelength now specified per epoch
    optogenetic_sites=[0],  # NEW list of references to row indices of the linked OptogeneticSitesTable
)
```


### Install the New Version

```bash
pip install ndx-optogenetics==0.3.0
```

## Step-by-Step Migration Process

### 1. Update Imports

Replace all device and biological component imports:

```python
# Remove these imports
# from ndx_optogenetics import (
#     ExcitationSourceModel,
#     ExcitationSource,
#     OpticalFiberModel,
#     OpticalFiber,
#     OptogeneticVirus,
#     OptogeneticVirusInjection,
# )

# Add these imports
from ndx_ophys_devices import (
    ExcitationSourceModel,
    ExcitationSource,
    OpticalFiberModel,
    OpticalFiber,
    FiberInsertion,
    ViralVector,
    ViralVectorInjection,
    Effector,
)
```

### 2. Update Device Creation

Modify your device creation code according to the examples above, paying special attention to:
- Attribute name changes (`illumination_type` → `source_type`, `fiber_model` → `model_number`)
- New required attributes (`excitation_mode`, `serial_number`, `fiber_insertion`)
- Removed attributes (`wavelength_in_nm` from `ExcitationSource`, `fiber_name` from `OpticalFiberModel`)

### 3. Update Virus and Injection Handling

Replace `OptogeneticVirus` with `ViralVector` and `OptogeneticVirusInjection` with `ViralVectorInjection`.

### 4. Create Effector Objects

Add effector creation and container:

```python
effector = Effector(
    name="effector",
    description="Excitatory opsin",
    label="hChR2-EYFP",
    viral_vector_injection=virus_injection,
)
optogenetic_effectors = OptogeneticEffectors(effectors=[effector])
```

### 5. Replace OpticalFiberLocationsTable

Convert your fiber locations table to the new sites table format:

```python
# Instead of adding location data to a separate table, create OptogeneticSitesTable with device references
optogenetic_sites_table = OptogeneticSitesTable(
    description="Information about the optogenetic stimulation sites."
)
optogenetic_sites_table.add_row(
    excitation_source=excitation_source,
    optical_fiber=optical_fiber,
    effector=effector,
)
```

### 6. Update Experiment Metadata

Add the effectors container and update table references:

```python
optogenetic_experiment_metadata = OptogeneticExperimentMetadata(
    optogenetic_sites_table=optogenetic_sites_table,  # Changed
    optogenetic_viruses=optogenetic_viruses,
    optogenetic_virus_injections=optogenetic_virus_injections,
    optogenetic_effectors=optogenetic_effectors,  # New
    stimulation_software="FSGUI 2.0",
)
```

### 7. Update Epochs Table

Update the epochs table to use the new sites table and add wavelength information:

```python
opto_epochs_table = OptogeneticEpochsTable(
    name="optogenetic_epochs",
    description="Metadata about optogenetic stimulation parameters per epoch",
    target_tables={"optogenetic_sites": optogenetic_sites_table},  # Changed
)
opto_epochs_table.add_row(
    # ... existing parameters ...
    wavelength_in_nm=488.0,  # New
    optogenetic_sites=[0],  # New
)
```

### Validation

After migration, validate your code by:

1. Running your updated code to ensure it executes without errors
2. Writing and reading NWB files to verify data integrity
3. Checking that all metadata is properly preserved
4. Testing with your existing analysis pipelines

## Support

If you encounter issues during migration:

1. Check the [ndx-optogenetics GitHub repository](https://github.com/rly/ndx-optogenetics) for examples
2. Review the [ndx-ophys-devices documentation](https://github.com/catalystneuro/ndx-ophys-devices)
3. Open an issue on the respective GitHub repositories for support

