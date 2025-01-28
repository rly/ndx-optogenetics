def test_example_usage():
    import datetime
    from pynwb import NWBFile, NWBHDF5IO
    from ndx_optogenetics import (
        Laser,
        OpticalFiber,
        OpticalFiberImplantSite,
        OptogeneticVirus,
        OptogeneticVirusInjection,
        OptogeneticViruses,
        OptogeneticVirusInjections,
        OptogeneticExperimentMetadata,
        OptogeneticEpochsTable,
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

    optical_fiber = OpticalFiber(
        name="Lambda",
        description="Lambda fiber (tapered fiber) from Optogenix.",
        fiber_name="Lambda",
        fiber_manufacturer_code="lambda_b5",
        manufacturer="Optogenix",
        numerical_aperture=0.39,
        core_diameter_in_um=200.0,
        active_length_in_mm=2.0,
        ferrule_name="cFCF - ∅2.5mm Ceramic Ferrule",
        ferrule_diameter_in_mm=2.5,
    )
    nwbfile.add_device(optical_fiber)

    optical_fiber_implant_site = OpticalFiberImplantSite(
        name="Lambda_GPe",
        description="Optical fiber implanted into GPe stimulating at 488 nm and 77 mW.",
        excitation_lambda=488.0,  # in nm
        hemisphere="right",
        location="GPe",
        ap_in_mm=-1.5,
        ml_in_mm=3.2,
        dv_in_mm=-5.8,
        roll_in_deg=0.0,
        pitch_in_deg=0.0,
        yaw_in_deg=0.0,
        reference="bregma at the cortical surface",
        device=laser,
        optical_fiber=optical_fiber,
    )
    nwbfile.add_ogen_site(optical_fiber_implant_site)

    virus = OptogeneticVirus(
        name="AAV-EF1a-DIO-hChR2(H134R)-EYFP",
        construct_name="AAV-EF1a-DIO-hChR2(H134R)-EYFP",
        description=(
            "Excitatory optogenetic construct designed to make neurons express the light sensitive opsin, hChR2-EYFP."
        ),
        manufacturer="UNC Vector Core",
        titer_in_vg_per_ml=int(1.0e12),
    )
    optogenetic_viruses = OptogeneticViruses(optogenetic_virus=[virus])

    virus_injection = OptogeneticVirusInjection(
        name="AAV-EF1a-DIO-hChR2(H134R)-EYFP Injection",
        description="AAV-EF1a-DIO-hChR2(H134R)-EYFP injection into GPe.",
        hemisphere="right",
        location="GPe",
        ap_in_mm=-1.5,
        ml_in_mm=3.2,
        dv_in_mm=-6.0,
        roll_in_deg=0.0,
        pitch_in_deg=0.0,
        yaw_in_deg=0.0,
        reference="bregma at the cortical surface",
        virus=virus,
        volume_in_uL=0.45,
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

    opto_epochs_table = OptogeneticEpochsTable(
        name="optogenetic_epochs",
        description="Metadata about the optogenetic stimulation parameters that change per epoch.",
    )

    # test add one epoch
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
    nwbfile.add_time_intervals(opto_epochs_table)

    # write the NWBFile to disk
    path = "test_optogenetics.nwb"
    with NWBHDF5IO(path, mode="w") as io:
        io.write(nwbfile)

    # read the NWBFile from disk and print out TODO
    with NWBHDF5IO(path, mode="r", load_namespaces=True) as io:
        read_nwbfile = io.read()

        assert type(read_nwbfile.devices["Omicron LuxX+ 488-100"]) is Laser
        assert read_nwbfile.devices["Omicron LuxX+ 488-100"].name == "Omicron LuxX+ 488-100"
        assert read_nwbfile.devices["Omicron LuxX+ 488-100"].description == "Laser for optogenetic stimulation."
        assert read_nwbfile.devices["Omicron LuxX+ 488-100"].manufacturer == "Omicron"

        assert type(read_nwbfile.devices["Lambda"]) is OpticalFiber
        assert read_nwbfile.devices["Lambda"].name == "Lambda"
        assert read_nwbfile.devices["Lambda"].description == "Lambda fiber (tapered fiber) from Optogenix."
        assert read_nwbfile.devices["Lambda"].fiber_name == "Lambda"
        assert read_nwbfile.devices["Lambda"].fiber_manufacturer_code == "lambda_b5"
        assert read_nwbfile.devices["Lambda"].manufacturer == "Optogenix"
        assert read_nwbfile.devices["Lambda"].numerical_aperture == 0.39
        assert read_nwbfile.devices["Lambda"].core_diameter_in_um == 200
        assert read_nwbfile.devices["Lambda"].active_length_in_mm == 2.0
        assert read_nwbfile.devices["Lambda"].ferrule_name == "cFCF - ∅2.5mm Ceramic Ferrule"
        assert read_nwbfile.devices["Lambda"].ferrule_diameter_in_mm == 2.5

        assert type(read_nwbfile.ogen_sites["Lambda_GPe"]) is OpticalFiberImplantSite
        assert read_nwbfile.ogen_sites["Lambda_GPe"].name == "Lambda_GPe"
        assert read_nwbfile.ogen_sites["Lambda_GPe"].description == "Optical fiber implanted into GPe stimulating at 488 nm and 77 mW."
        assert read_nwbfile.ogen_sites["Lambda_GPe"].excitation_lambda == 488.0
        assert read_nwbfile.ogen_sites["Lambda_GPe"].hemisphere == "right"
        assert read_nwbfile.ogen_sites["Lambda_GPe"].location == "GPe"
        assert read_nwbfile.ogen_sites["Lambda_GPe"].ap_in_mm == -1.5
        assert read_nwbfile.ogen_sites["Lambda_GPe"].ml_in_mm == 3.2
        assert read_nwbfile.ogen_sites["Lambda_GPe"].dv_in_mm == -5.8
        assert read_nwbfile.ogen_sites["Lambda_GPe"].roll_in_deg == 0.0
        assert read_nwbfile.ogen_sites["Lambda_GPe"].pitch_in_deg == 0.0
        assert read_nwbfile.ogen_sites["Lambda_GPe"].yaw_in_deg == 0.0
        assert read_nwbfile.ogen_sites["Lambda_GPe"].reference == "bregma at the cortical surface"
        assert read_nwbfile.ogen_sites["Lambda_GPe"].device == read_nwbfile.devices["Omicron LuxX+ 488-100"]
        assert read_nwbfile.ogen_sites["Lambda_GPe"].optical_fiber == read_nwbfile.devices["Lambda"]

        assert type(read_nwbfile.lab_meta_data["optogenetic_experiment_metadata"]) is OptogeneticExperimentMetadata
        assert read_nwbfile.lab_meta_data["optogenetic_experiment_metadata"].stimulation_software == "FSGUI 2.0"

        assert len(read_nwbfile.lab_meta_data["optogenetic_experiment_metadata"].optogenetic_viruses.optogenetic_virus) == 1
        read_virus = read_nwbfile.lab_meta_data["optogenetic_experiment_metadata"].optogenetic_viruses.optogenetic_virus["AAV-EF1a-DIO-hChR2(H134R)-EYFP"]
        assert read_virus.name == "AAV-EF1a-DIO-hChR2(H134R)-EYFP"
        assert read_virus.construct_name == "AAV-EF1a-DIO-hChR2(H134R)-EYFP"
        assert read_virus.description == "Excitatory optogenetic construct designed to make neurons express the light sensitive opsin, hChR2-EYFP."
        assert read_virus.manufacturer == "UNC Vector Core"
        assert read_virus.titer_in_vg_per_ml == int(1.0e12)

        assert len(read_nwbfile.lab_meta_data["optogenetic_experiment_metadata"].optogenetic_virus_injections.optogenetic_virus_injections) == 1
        read_virus_injection = read_nwbfile.lab_meta_data["optogenetic_experiment_metadata"].optogenetic_virus_injections.optogenetic_virus_injections["AAV-EF1a-DIO-hChR2(H134R)-EYFP Injection"]
        assert read_virus_injection.name == "AAV-EF1a-DIO-hChR2(H134R)-EYFP Injection"
        assert read_virus_injection.description == "AAV-EF1a-DIO-hChR2(H134R)-EYFP injection into GPe."
        assert read_virus_injection.hemisphere == "right"
        assert read_virus_injection.location == "GPe"
        assert read_virus_injection.ap_in_mm == -1.5
        assert read_virus_injection.ml_in_mm == 3.2
        assert read_virus_injection.dv_in_mm == -6.0
        assert read_virus_injection.roll_in_deg == 0.0
        assert read_virus_injection.pitch_in_deg == 0.0
        assert read_virus_injection.yaw_in_deg == 0.0
        assert read_virus_injection.reference == "bregma at the cortical surface"
        assert read_virus_injection.virus == read_virus
        assert read_virus_injection.volume_in_uL == 0.45

        assert type(read_nwbfile.intervals["optogenetic_epochs"]) is OptogeneticEpochsTable
        assert read_nwbfile.intervals["optogenetic_epochs"].name == "optogenetic_epochs"
        assert read_nwbfile.intervals["optogenetic_epochs"].description == "Metadata about the optogenetic stimulation parameters that change per epoch."
        assert len(read_nwbfile.intervals["optogenetic_epochs"]) == 1
        assert read_nwbfile.intervals["optogenetic_epochs"][0, "start_time"] == 0.0
        assert read_nwbfile.intervals["optogenetic_epochs"][0, "stop_time"] == 100.0
        assert read_nwbfile.intervals["optogenetic_epochs"][0, "stimulation_on"] == True
        assert read_nwbfile.intervals["optogenetic_epochs"][0, "pulse_length_in_ms"] == 40.0
        assert read_nwbfile.intervals["optogenetic_epochs"][0, "period_in_ms"] == 250.0
        assert read_nwbfile.intervals["optogenetic_epochs"][0, "number_pulses_per_pulse_train"] == 100
        assert read_nwbfile.intervals["optogenetic_epochs"][0, "number_trains"] == 1
        assert read_nwbfile.intervals["optogenetic_epochs"][0, "intertrain_interval_in_ms"] == 0.0
        assert read_nwbfile.intervals["optogenetic_epochs"][0, "power_in_mW"] == 77.0



