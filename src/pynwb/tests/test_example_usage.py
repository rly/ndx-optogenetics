def test_example_usage(tmp_path):
    import math
    from datetime import datetime, timezone
    from pynwb import NWBFile, NWBHDF5IO
    from ndx_ophys_devices import (
        ViralVector,
        ViralVectorInjection,
        Effector,
        ExcitationSourceModel,
        ExcitationSource,
        OpticalFiberModel,
        OpticalFiber,
        StereotacticPosition,
    )
    from ndx_optogenetics import (
        OptogeneticSitesTable,
        OptogeneticViruses,
        OptogeneticVirusInjections,
        OptogeneticEffectors,
        OptogeneticExperimentMetadata,
        OptogeneticEpochsTable,
        OptogeneticPulsesTable,
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
        source_type="laser",
        excitation_mode="one-photon",
        wavelength_range_in_nm=[488.0, 488.0],
    )
    excitation_source = ExcitationSource(
        name="Omicron LuxX+ 488-100",
        model=excitation_source_model,
        power_in_W=0.077,
        intensity_in_W_per_m2=2.45e6,  # 77 mW over the area of a 200 um core
    )
    nwbfile.add_device_model(excitation_source_model)
    nwbfile.add_device(excitation_source)

    # Create and add optical fiber devices
    optical_fiber_model = OpticalFiberModel(
        name="Lambda Model",
        description="Lambda fiber (tapered fiber) from Optogenix.",
        model_number="lambda_b5",
        manufacturer="Optogenix",
        numerical_aperture=0.39,
        core_diameter_in_um=200.0,
        active_length_in_mm=2.0,
        ferrule_name="cFCF - ∅2.5mm Ceramic Ferrule",
        ferrule_diameter_in_mm=2.5,
    )
    fiber_insertion = StereotacticPosition(
        name="fiber_insertion",
        anatomical_target="GPe",
        origin="Bregma at the cortical surface",
        orientation="RAS",
        x_in_mm=3.2,
        y_in_mm=-1.5,
        z_in_mm=-5.8,
        pitch_in_deg=0.0,
    )
    optical_fiber = OpticalFiber(
        name="Lambda",
        description="Lambda fiber implanted into right GPe.",
        serial_number="123456",
        model=optical_fiber_model,
        fiber_insertion=fiber_insertion,
    )
    nwbfile.add_device_model(optical_fiber_model)
    nwbfile.add_device(optical_fiber)

    # Create virus and injection metadata
    virus = ViralVector(
        name="AAV-EF1a-DIO-hChR2(H134R)-EYFP",
        construct_name="AAV-EF1a-DIO-hChR2(H134R)-EYFP",
        description="Excitatory optogenetic construct for ChR2-EYFP expression",
        manufacturer="UNC Vector Core",
        titer_in_vg_per_ml=1.0e12,
    )
    optogenetic_viruses = OptogeneticViruses(viral_vectors=[virus])

    virus_injection = ViralVectorInjection(
        name="AAV-EF1a-DIO-hChR2(H134R)-EYFP Injection",
        description="AAV-EF1a-DIO-hChR2(H134R)-EYFP injection into GPe.",
        viral_injection_coordinates=StereotacticPosition(
            name="viral_injection_coordinates",
            anatomical_target="GPe",
            origin="Bregma at the cortical surface",
            orientation="RAS",
            x_in_mm=3.2,
            y_in_mm=-1.5,
            z_in_mm=-6.0,
            roll_in_deg=0.0,
            pitch_in_deg=0.0,
            yaw_in_deg=0.0,
        ),
        viral_vector=virus,
        volume_in_uL=0.45,
        injection_date="1970-01-01T00:00:00+00:00",
    )
    optogenetic_virus_injections = OptogeneticVirusInjections(viral_vector_injections=[virus_injection])

    effector = Effector(
        name="effector",
        description="Excitatory opsin",
        label="hChR2-EYFP",
        viral_vector_injection=virus_injection,
    )
    optogenetic_effectors = OptogeneticEffectors(effectors=[effector])

    # Create OptogeneticSitesTable
    optogenetic_sites_table = OptogeneticSitesTable(description="Information about the optogenetic stimulation sites.")
    optogenetic_sites_table.add_row(
        excitation_source=excitation_source,
        optical_fiber=optical_fiber,
        effector=effector,
    )

    # Create experiment metadata container
    optogenetic_experiment_metadata = OptogeneticExperimentMetadata(
        optogenetic_sites_table=optogenetic_sites_table,
        optogenetic_viruses=optogenetic_viruses,
        optogenetic_virus_injections=optogenetic_virus_injections,
        optogenetic_effectors=optogenetic_effectors,
        stimulation_software="FSGUI 2.0",
    )
    nwbfile.add_lab_meta_data(optogenetic_experiment_metadata)

    # Create stimulation epochs table
    opto_epochs_table = OptogeneticEpochsTable(
        name="optogenetic_epochs",
        description="Metadata about optogenetic stimulation parameters per epoch",
        target_tables={"optogenetic_sites": optogenetic_sites_table},
    )
    opto_epochs_table.add_row(
        start_time=0.0,
        stop_time=100.0,
        stimulation_on=True,
        pulse_length_in_ms=40.0,
        period_in_ms=250.0,
        number_pulses_per_pulse_train=100,
        number_trains=1,
        intertrain_interval_in_ms=float("nan"),  # not applicable with a single train
        power_in_mW=77.0,
        wavelength_in_nm=488.0,
        optogenetic_sites=[0],
    )
    nwbfile.add_time_intervals(opto_epochs_table)

    # Create stimulation pulses table
    opto_pulses_table = OptogeneticPulsesTable(
        name="optogenetic_pulses",
        description="Metadata about optogenetic stimulation per pulse",
        target_tables={"optogenetic_sites": optogenetic_sites_table},
    )
    opto_pulses_table.add_row(
        start_time=10.0,
        stop_time=10.04,
        power_in_mW=77.0,
        wavelength_in_nm=488.0,
        optogenetic_sites=[0],
    )
    nwbfile.add_time_intervals(opto_pulses_table)

    # Write the file
    path = tmp_path / "test_optogenetics.nwb"
    with NWBHDF5IO(path, mode="w") as io:
        io.write(nwbfile)

    # Read the NWBFile from disk and check the values
    with NWBHDF5IO(path, mode="r", load_namespaces=True) as io:
        read_nwbfile = io.read()

        read_excitation_source_model = read_nwbfile.device_models["Omicron LuxX+ 488-100 Model"]
        assert type(read_excitation_source_model) is ExcitationSourceModel
        assert read_excitation_source_model.name == "Omicron LuxX+ 488-100 Model"
        assert read_excitation_source_model.description == "Laser for optogenetic stimulation."
        assert read_excitation_source_model.manufacturer == "Omicron"
        assert read_excitation_source_model.source_type == "laser"
        assert read_excitation_source_model.excitation_mode == "one-photon"
        assert all(read_excitation_source_model.wavelength_range_in_nm == [488.0, 488.0])

        read_excitation_source = read_nwbfile.devices["Omicron LuxX+ 488-100"]
        assert type(read_excitation_source) is ExcitationSource
        assert read_excitation_source.name == "Omicron LuxX+ 488-100"
        assert read_excitation_source.model is read_excitation_source_model
        assert read_excitation_source.power_in_W == 0.077
        assert read_excitation_source.intensity_in_W_per_m2 == 2.45e6

        read_optical_fiber_model = read_nwbfile.device_models["Lambda Model"]
        assert type(read_optical_fiber_model) is OpticalFiberModel
        assert read_optical_fiber_model.name == "Lambda Model"
        assert read_optical_fiber_model.description == "Lambda fiber (tapered fiber) from Optogenix."
        assert read_optical_fiber_model.model_number == "lambda_b5"
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
        assert read_optical_fiber.description == "Lambda fiber implanted into right GPe."
        assert read_optical_fiber.serial_number == "123456"

        read_fiber_insertion = read_optical_fiber.fiber_insertion
        assert type(read_fiber_insertion) is StereotacticPosition
        assert read_fiber_insertion.name == "fiber_insertion"
        assert read_fiber_insertion.anatomical_target == "GPe"
        assert read_fiber_insertion.origin == "Bregma at the cortical surface"
        assert read_fiber_insertion.orientation == "RAS"
        assert read_fiber_insertion.x_in_mm == 3.2
        assert read_fiber_insertion.y_in_mm == -1.5
        assert read_fiber_insertion.z_in_mm == -5.8
        assert read_fiber_insertion.pitch_in_deg == 0.0

        read_optogenetic_experiment_metadata = read_nwbfile.lab_meta_data["optogenetic_experiment_metadata"]
        assert type(read_optogenetic_experiment_metadata) is OptogeneticExperimentMetadata
        assert read_optogenetic_experiment_metadata.stimulation_software == "FSGUI 2.0"

        read_optogenetic_sites_table = read_optogenetic_experiment_metadata.optogenetic_sites_table
        assert type(read_optogenetic_sites_table) is OptogeneticSitesTable
        assert read_optogenetic_sites_table.description == "Information about the optogenetic stimulation sites."

        assert len(read_optogenetic_sites_table) == 1
        assert read_optogenetic_sites_table[0, "excitation_source"] is read_nwbfile.devices["Omicron LuxX+ 488-100"]
        assert read_optogenetic_sites_table[0, "optical_fiber"] is read_nwbfile.devices["Lambda"]
        assert (
            read_optogenetic_sites_table[0, "effector"]
            is read_optogenetic_experiment_metadata.optogenetic_effectors.effectors["effector"]
        )

        assert len(read_optogenetic_experiment_metadata.optogenetic_viruses.viral_vectors) == 1
        read_virus = read_optogenetic_experiment_metadata.optogenetic_viruses.viral_vectors[
            "AAV-EF1a-DIO-hChR2(H134R)-EYFP"
        ]
        assert read_virus.name == "AAV-EF1a-DIO-hChR2(H134R)-EYFP"
        assert read_virus.construct_name == "AAV-EF1a-DIO-hChR2(H134R)-EYFP"
        assert read_virus.description == "Excitatory optogenetic construct for ChR2-EYFP expression"
        assert read_virus.manufacturer == "UNC Vector Core"
        assert read_virus.titer_in_vg_per_ml == int(1.0e12)

        assert len(read_optogenetic_experiment_metadata.optogenetic_virus_injections.viral_vector_injections) == 1
        read_virus_injection = (
            read_optogenetic_experiment_metadata.optogenetic_virus_injections.viral_vector_injections[
                "AAV-EF1a-DIO-hChR2(H134R)-EYFP Injection"
            ]
        )
        assert read_virus_injection.name == "AAV-EF1a-DIO-hChR2(H134R)-EYFP Injection"
        assert read_virus_injection.description == "AAV-EF1a-DIO-hChR2(H134R)-EYFP injection into GPe."
        read_injection_coordinates = read_virus_injection.viral_injection_coordinates
        assert type(read_injection_coordinates) is StereotacticPosition
        assert read_injection_coordinates.name == "viral_injection_coordinates"
        assert read_injection_coordinates.anatomical_target == "GPe"
        assert read_injection_coordinates.origin == "Bregma at the cortical surface"
        assert read_injection_coordinates.orientation == "RAS"
        assert read_injection_coordinates.x_in_mm == 3.2
        assert read_injection_coordinates.y_in_mm == -1.5
        assert read_injection_coordinates.z_in_mm == -6.0
        assert read_injection_coordinates.roll_in_deg == 0.0
        assert read_injection_coordinates.pitch_in_deg == 0.0
        assert read_injection_coordinates.yaw_in_deg == 0.0
        assert read_virus_injection.viral_vector is read_virus
        assert read_virus_injection.volume_in_uL == 0.45

        assert len(read_optogenetic_experiment_metadata.optogenetic_effectors.effectors) == 1
        read_effector = read_optogenetic_experiment_metadata.optogenetic_effectors.effectors["effector"]
        assert read_effector.name == "effector"
        assert read_effector.description == "Excitatory opsin"
        assert read_effector.label == "hChR2-EYFP"
        assert read_effector.viral_vector_injection is read_virus_injection

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
        assert math.isnan(read_optogenetic_epochs_table[0, "intertrain_interval_in_ms"])
        assert read_optogenetic_epochs_table[0, "power_in_mW"] == 77.0
        assert read_optogenetic_epochs_table[0, "wavelength_in_nm"] == 488.0
        assert read_optogenetic_epochs_table.optogenetic_sites_index.data[:].tolist() == [1]
        assert read_optogenetic_epochs_table.optogenetic_sites.table is read_optogenetic_sites_table
        assert read_optogenetic_epochs_table[0, "optogenetic_sites"].equals(
            read_optogenetic_sites_table.to_dataframe()[0:1]
        )

        read_optogenetic_pulses_table = read_nwbfile.intervals["optogenetic_pulses"]
        assert type(read_optogenetic_pulses_table) is OptogeneticPulsesTable
        assert read_optogenetic_pulses_table.name == "optogenetic_pulses"
        assert read_optogenetic_pulses_table.description == "Metadata about optogenetic stimulation per pulse"
        assert len(read_optogenetic_pulses_table) == 1
        assert read_optogenetic_pulses_table[0, "start_time"] == 10.0
        assert read_optogenetic_pulses_table[0, "stop_time"] == 10.04
        assert read_optogenetic_pulses_table[0, "power_in_mW"] == 77.0
        assert read_optogenetic_pulses_table[0, "wavelength_in_nm"] == 488.0
        assert read_optogenetic_pulses_table.optogenetic_sites_index.data[:].tolist() == [1]
        assert read_optogenetic_pulses_table.optogenetic_sites.table is read_optogenetic_sites_table
        assert read_optogenetic_pulses_table[0, "optogenetic_sites"].equals(
            read_optogenetic_sites_table.to_dataframe()[0:1]
        )
