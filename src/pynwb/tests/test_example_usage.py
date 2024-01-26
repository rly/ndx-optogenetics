import datetime
import numpy as np
from pynwb import NWBFile, NWBHDF5IO
from ndx_optogenetics import (
    Laser,
    OpticFiber,
    OpticFiberImplantSite,
    OptogeneticVirus,
    OptogeneticVirusInjection,
    OptogeneticViruses,
    OptogeneticVirusInjections,
    OptogeneticExperimentMetadata,
    FrankLabOptogeneticEpochs,
)

# initialize an NWBFile object
nwbfile = NWBFile(
    session_description="session_description",
    identifier="identifier",
    session_start_time=datetime.datetime.now(datetime.timezone.utc),
)

laser = Laser(
    name="Omicron LuxX+ 488-100",
    description="Laser for optogenetic stimulation.",
    manufacturer="Omicron",
)
nwbfile.add_device(laser)

optic_fiber = OpticFiber(
    name="Lambda",
    description="Lambda fiber (tapered fiber) from Optogenix.",
    fiber_name="Lambda",
    fiber_manufacturer_code="lambda_b5",
    manufacturer="Optogenix",
    numerical_aperture=0.39,
    cannula_core_diameter=0.2,
    active_length=2.0,
    ferrule_name="cFCF - ∅2.5mm Ceramic Ferrule",
    ferrule_diameter=2.5,
)
nwbfile.add_device(optic_fiber)

optic_fiber_implant_site = OpticFiberImplantSite(
    name="Lambda_GPe",
    description="Optic fiber implanted into GPe stimulating at 488 nm and 77 mW.",
    excitation_lambda=488.0,
    location="GPe",
    ap=-1.5,
    ml=3.2,
    dv=-6.0,
    reference="bregma at the cortical surface",
    power=77.0,
    device=laser,
    optic_fiber=optic_fiber,
)
nwbfile.add_ogen_site(optic_fiber_implant_site)

virus = OptogeneticVirus(
    name="AAV-EF1a-DIO-hChR2(H134R)-EYFP",
    construct_name="AAV-EF1a-DIO-hChR2(H134R)-EYFP",
    description=(
        "Excitatory optogenetic construct designed to make neurons express the light sensitive opsin, hChR2-EYFP."
    ),
    manufacturer="UNC Vector Core",
    titer=int(1.0e12),
)
optogenetic_viruses = OptogeneticViruses(optogenetic_virus=[virus])

virus_injection = OptogeneticVirusInjection(
    name="AAV-EF1a-DIO-hChR2(H134R)-EYFP Injection",
    description="AAV-EF1a-DIO-hChR2(H134R)-EYFP injection into GPe.",
    location="GPe",
    ap=-1.5,
    ml=3.2,
    dv=-6.0,
    reference="bregma at the cortical surface",
    virus=virus,
    volume=0.45,
)
optogenetic_virus_injections = OptogeneticVirusInjections(
    optogenetic_virus_injections=[virus_injection]
)

optogenetic_experiment_metadata = OptogeneticExperimentMetadata(
    optogenetic_viruses=optogenetic_viruses,
    optogenetic_virus_injections=optogenetic_virus_injections,
    stimulation_software="FSGUI 2.0",
)
# when the extension is merged to core,
# this should be added to the NWBFile under the nwbfile/general/optogenetics group instead of labmetadata
nwbfile.add_lab_meta_data(optogenetic_experiment_metadata)

camera1 = nwbfile.create_device(
    name="overhead_run_camera 1",
    description="Camera used for tracking running",
    # TODO cm_per_pixel
)

camera2 = nwbfile.create_device(
    name="overhead_run_camera 2",
    description="Camera used for tracking running",
    # TODO cm_per_pixel
)

opto_epochs = FrankLabOptogeneticEpochs(
    name="optogenetic_epochs",
    description="Metadata about the optogenetic stimulation parameters that change per epoch.",
)

# test add one epoch
opto_epochs.add_row(
    start_time=0.0,
    stop_time=100.0,
    convenience_code="a1",
    epoch_name="lineartrack",
    stimulation_on=True,
    pulse_length_ms=40,
    period_ms=250,
    number_pulses_per_pulse_train=100,
    # interpulse_interval_ms=210.0,  # derived from period_ms and pulse_length_ms
    number_trains=1,
    intertrain_interval_ms=0,
    # manual_number_stims,
    # manual_time_between_stims,
    # manual_control_mins,
    # manual_control_start_mins_into_rec,
    # manual_control_end_mins_into_rec,
    # theta_filter_on=False,
    # theta_filter_degrees -- None
    # theta_filter_reference_ntrode=12,
    spatial_filter_on=True,
    # tracking_threshold,
    spatial_filter_bottom_left_coord=np.array([260, 920], dtype=np.uint),
    spatial_filter_top_right_coord=np.array([800, 1050], dtype=np.uint),
    spatial_filter_cameras=[camera1, camera2],
    # spatial_filter_lockout_period_samples -- None
    # lockout_period_samples_theta -- None
    # ripple_filter,
    # lockout_period_samples_ripple,
    # ripple_threshold_sd,
    # num_above_threshold_ripple
)
nwbfile.add_time_intervals(opto_epochs)

# write the NWBFile to disk
path = "test_optogenetics.nwb"
with NWBHDF5IO(path, mode="w") as io:
    io.write(nwbfile)

# read the NWBFile from disk and print out TODO
with NWBHDF5IO(path, mode="r", load_namespaces=True) as io:
    read_nwbfile = io.read()