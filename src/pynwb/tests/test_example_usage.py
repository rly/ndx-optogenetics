def test_example_usage():
    from datetime import datetime, timezone
    from pynwb import NWBFile, NWBHDF5IO
    from ndx_optogenetics import (
        ExcitationSourceModel,
        ExcitationSource,
        OpticalFiberModel,
        OpticalFiber,
        OpticalFiberLocationsTable,
        OptogeneticVirus,
        OptogeneticVirusInjection,
        OptogeneticViruses,
        OptogeneticVirusInjections,
        OptogeneticExperimentMetadata,
        OptogeneticEpochsTable,
    )

    # Initialize NWB file
    nwbfile = NWBFile(
        session_description="session_description",
        identifier="identifier",
        session_start_time=datetime.now(timezone.utc),
    )

    # Create and add excitation source devices
    excitation_source_model = ExcitationSourceModel(
        name="Omicron LuxX+ 488-100 Model",
        description="Laser for optogenetic stimulation.",
        manufacturer="Omicron",
        illumination_type="laser",
        wavelength_range_in_nm=[488.0, 488.0],
    )
    excitation_source = ExcitationSource(
        name="Omicron LuxX+ 488-100",
        model=excitation_source_model,
        wavelength_in_nm=488.0,
        power_in_W=0.077,
        intensity_in_W_per_m2=1.0e10,
    )
    nwbfile.add_device_model(excitation_source_model)
    nwbfile.add_device(excitation_source)

    # Create and add optical fiber devices
    optical_fiber_model = OpticalFiberModel(
        name="Lambda Model",
        description="Lambda fiber (tapered fiber) from Optogenix.",
        fiber_name="Lambda",
        fiber_model="lambda_b5",
        manufacturer="Optogenix",
        numerical_aperture=0.39,
        core_diameter_in_um=200.0,
        active_length_in_mm=2.0,
        ferrule_name="cFCF - ∅2.5mm Ceramic Ferrule",
        ferrule_diameter_in_mm=2.5,
    )
    optical_fiber = OpticalFiber(
        name="Lambda",
        model=optical_fiber_model,
    )
    nwbfile.add_device_model(optical_fiber_model)
    nwbfile.add_device(optical_fiber)

    # Create optical fiber locations table
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
        excitation_source=excitation_source,
        optical_fiber=optical_fiber,
    )

    # Create virus and injection metadata
    virus = OptogeneticVirus(
        name="AAV-EF1a-DIO-hChR2(H134R)-EYFP",
        construct_name="AAV-EF1a-DIO-hChR2(H134R)-EYFP",
        description="Excitatory optogenetic construct for ChR2-EYFP expression",
        manufacturer="UNC Vector Core",
        titer_in_vg_per_ml=1.0e12,
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
        reference="Bregma at the cortical surface",
        virus=virus,
        volume_in_uL=0.45,
    )
    optogenetic_virus_injections = OptogeneticVirusInjections(optogenetic_virus_injections=[virus_injection])

    # Create experiment metadata container
    optogenetic_experiment_metadata = OptogeneticExperimentMetadata(
        optical_fiber_locations_table=optical_fiber_locations_table,
        optogenetic_viruses=optogenetic_viruses,
        optogenetic_virus_injections=optogenetic_virus_injections,
        stimulation_software="FSGUI 2.0",
    )
    nwbfile.add_lab_meta_data(optogenetic_experiment_metadata)

    # Create stimulation epochs table
    opto_epochs_table = OptogeneticEpochsTable(
        name="optogenetic_epochs",
        description="Metadata about optogenetic stimulation parameters per epoch",
        target_tables={"optical_fiber_locations": optical_fiber_locations_table},
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
        optical_fiber_locations=[0],
    )
    nwbfile.add_time_intervals(opto_epochs_table)

    # Write the file
    path = "test_optogenetics.nwb"
    with NWBHDF5IO(path, mode="w") as io:
        io.write(nwbfile)

    # read the NWBFile from disk and print out TODO
    with NWBHDF5IO(path, mode="r", load_namespaces=True) as io:
        read_nwbfile = io.read()

        read_excitation_source_model = read_nwbfile.device_models["Omicron LuxX+ 488-100 Model"]
        assert type(read_excitation_source_model) is ExcitationSourceModel
        assert read_excitation_source_model.name == "Omicron LuxX+ 488-100 Model"
        assert read_excitation_source_model.description == "Laser for optogenetic stimulation."
        assert read_excitation_source_model.manufacturer == "Omicron"
        assert read_excitation_source_model.illumination_type == "laser"
        assert all(read_excitation_source_model.wavelength_range_in_nm == [488.0, 488.0])

        read_excitation_source = read_nwbfile.devices["Omicron LuxX+ 488-100"]
        assert type(read_excitation_source) is ExcitationSource
        assert read_excitation_source.name == "Omicron LuxX+ 488-100"
        assert read_excitation_source.model is read_excitation_source_model
        assert read_excitation_source.wavelength_in_nm == 488.0
        assert read_excitation_source.power_in_W == 0.077
        assert read_excitation_source.intensity_in_W_per_m2 == 1.0e10

        read_optical_fiber_model = read_nwbfile.device_models["Lambda Model"]
        assert type(read_optical_fiber_model) is OpticalFiberModel
        assert read_optical_fiber_model.name == "Lambda Model"
        assert read_optical_fiber_model.description == "Lambda fiber (tapered fiber) from Optogenix."
        assert read_optical_fiber_model.fiber_name == "Lambda"
        assert read_optical_fiber_model.fiber_model == "lambda_b5"
        assert read_optical_fiber_model.manufacturer == "Optogenix"
        assert read_optical_fiber_model.numerical_aperture == 0.39
        assert read_optical_fiber_model.core_diameter_in_um == 200
        assert read_optical_fiber_model.active_length_in_mm == 2.0
        assert read_optical_fiber_model.ferrule_name == "cFCF - ∅2.5mm Ceramic Ferrule"
        assert read_optical_fiber_model.ferrule_diameter_in_mm == 2.5

        read_optical_fiber = read_nwbfile.devices["Lambda"]
        assert type(read_optical_fiber) is OpticalFiber
        assert read_optical_fiber.name == "Lambda"
        assert read_optical_fiber.model is read_optical_fiber_model

        read_optogenetic_experiment_metadata = read_nwbfile.lab_meta_data["optogenetic_experiment_metadata"]
        assert type(read_optogenetic_experiment_metadata) is OptogeneticExperimentMetadata
        assert read_optogenetic_experiment_metadata.stimulation_software == "FSGUI 2.0"

        read_fiber_locations_table = read_optogenetic_experiment_metadata.optical_fiber_locations_table
        assert type(read_fiber_locations_table) is OpticalFiberLocationsTable
        assert read_fiber_locations_table.description == "Information about implanted optical fiber locations"
        assert read_fiber_locations_table.reference == "Bregma at the cortical surface"

        assert len(read_fiber_locations_table) == 1
        assert read_fiber_locations_table[0, "implanted_fiber_description"] == "Lambda fiber implanted into right GPe."
        assert read_fiber_locations_table[0, "location"] == "GPe"
        assert read_fiber_locations_table[0, "hemisphere"] == "right"
        assert read_fiber_locations_table[0, "ap_in_mm"] == -1.5
        assert read_fiber_locations_table[0, "ml_in_mm"] == 3.2
        assert read_fiber_locations_table[0, "dv_in_mm"] == -5.8
        assert read_fiber_locations_table[0, "roll_in_deg"] == 0.0
        assert read_fiber_locations_table[0, "pitch_in_deg"] == 0.0
        assert read_fiber_locations_table[0, "yaw_in_deg"] == 0.0
        assert read_fiber_locations_table[0, "excitation_source"] is read_nwbfile.devices["Omicron LuxX+ 488-100"]
        assert read_fiber_locations_table[0, "optical_fiber"] is read_nwbfile.devices["Lambda"]

        assert len(read_optogenetic_experiment_metadata.optogenetic_viruses.optogenetic_virus) == 1
        read_virus = read_optogenetic_experiment_metadata.optogenetic_viruses.optogenetic_virus[
            "AAV-EF1a-DIO-hChR2(H134R)-EYFP"
        ]
        assert read_virus.name == "AAV-EF1a-DIO-hChR2(H134R)-EYFP"
        assert read_virus.construct_name == "AAV-EF1a-DIO-hChR2(H134R)-EYFP"
        assert read_virus.description == "Excitatory optogenetic construct for ChR2-EYFP expression"
        assert read_virus.manufacturer == "UNC Vector Core"
        assert read_virus.titer_in_vg_per_ml == int(1.0e12)

        assert len(read_optogenetic_experiment_metadata.optogenetic_virus_injections.optogenetic_virus_injections) == 1
        read_virus_injection = (
            read_optogenetic_experiment_metadata.optogenetic_virus_injections.optogenetic_virus_injections[
                "AAV-EF1a-DIO-hChR2(H134R)-EYFP Injection"
            ]
        )
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
        assert read_virus_injection.reference == "Bregma at the cortical surface"
        assert read_virus_injection.virus == read_virus
        assert read_virus_injection.volume_in_uL == 0.45

        read_optogenetic_epochs_table = read_nwbfile.intervals["optogenetic_epochs"]
        assert type(read_optogenetic_epochs_table) is OptogeneticEpochsTable
        assert read_optogenetic_epochs_table.name == "optogenetic_epochs"
        assert read_optogenetic_epochs_table.description == (
            "Metadata about optogenetic stimulation parameters per epoch"
        )
        assert len(read_optogenetic_epochs_table) == 1
        assert read_optogenetic_epochs_table[0, "start_time"] == 0.0
        assert read_optogenetic_epochs_table[0, "stop_time"] == 100.0
        assert read_optogenetic_epochs_table[0, "stimulation_on"] == True
        assert read_optogenetic_epochs_table[0, "pulse_length_in_ms"] == 40.0
        assert read_optogenetic_epochs_table[0, "period_in_ms"] == 250.0
        assert read_optogenetic_epochs_table[0, "number_pulses_per_pulse_train"] == 100
        assert read_optogenetic_epochs_table[0, "number_trains"] == 1
        assert read_optogenetic_epochs_table[0, "intertrain_interval_in_ms"] == 0.0
        assert read_optogenetic_epochs_table[0, "power_in_mW"] == 77.0
        assert read_optogenetic_epochs_table.optical_fiber_locations_index.data[:] == [1]
        assert read_optogenetic_epochs_table.optical_fiber_locations.data[:] == [0]
        assert read_optogenetic_epochs_table.optical_fiber_locations.table is read_fiber_locations_table
        assert read_optogenetic_epochs_table[0, "optical_fiber_locations"].equals(read_fiber_locations_table.to_dataframe()[0:1])
