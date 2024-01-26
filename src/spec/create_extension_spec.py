# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import (
    NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec, NWBLinkSpec, NWBDatasetSpec, NWBRefSpec
)


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-optogenetics""",
        version="""0.2.0""",
        doc="""NWB extension to improve support for optogenetics data and metadata""",
        author=[
            "Ryan Ly",
            "Horea Christian",
            "Ben Dichter",
        ],
        contact=[
            "rly@lbl.gov",
            "rly@lbl.gov",  # TODO add Horea's email address
            "ben.dichter@catalystneuro.com",
        ],
    )
    ns_builder.include_namespace("core")

    laser = NWBGroupSpec(
        neurodata_type_def="Laser",
        neurodata_type_inc="Device",
        doc="Laser device. Currently there are no additional attributes.",
    )

    optic_fiber = NWBGroupSpec(
        neurodata_type_def="OpticFiber",
        neurodata_type_inc="Device",
        doc="Optical fiber device.",
        # refs:
        # - https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=6742
        # - https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=6313
        # - https://www.optogenix.com/product/lambda-fiber-stubs-one-5-pack/
        attributes=[
            NWBAttributeSpec(
                name="description",
                doc="Description of the optic fiber and ferrule equipment, including cleave type or tapering.",
                dtype="text",
                required=False,
            ),
            NWBAttributeSpec(
                name="fiber_name",
                doc="Name of the optic fiber.",
                dtype="text",
            ),
            NWBAttributeSpec(
                name="fiber_manufacturer_code",
                doc="Code / product ID of the optic fiber from the manufacturer.",
                dtype="text",
                required=False,
            ),
            NWBAttributeSpec(
                name="manufacturer",
                doc="Manufacturer of the optic fiber and ferrule.",
                dtype="text",
                # NOTE it is assumed that the fiber and ferrule are from the same manufacturer
            ),
            NWBAttributeSpec(
                name="numerical_aperture",
                doc="Numerical aperture, e.g., 0.39 NA.",
                dtype="float",
            ),
            NWBAttributeSpec(
                name="cannula_core_diameter",  # TODO is cladding diameter important?
                doc="Cannula diameter in mm, e.g., 0.2 mm (200 um).",
                dtype="float",
            ),
            NWBAttributeSpec(
                name="active_length",
                doc=(
                    "Active length for a tapered fiber, e.g., Optogenix Lambda fiber. "
                    "See https://www.optogenix.com/lambda-fibers/ for details of one example."
                ),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="ferrule_name",
                doc="Product name of the ferrule.",
                dtype="text",
                required=False,
            ),
            NWBAttributeSpec(
                name="ferrule_manufacturer_code",
                doc="Code / product ID of the ferrule from the manufacturer.",
                dtype="text",
                required=False,
            ),
            NWBAttributeSpec(  # TODO is this important to store? what about ferrule material? manufacturer?
                name="ferrule_diameter",
                doc="Ferrule diameter in mm, e.g., 1.25 mm (LC) or 2.5 mm (FC).",
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(  # TODO what is this?
                name="transmittance",
                doc="Transmittance.",
                dtype="float",
                required=False,
            ),
        ],
    )

    optic_fiber_implant_site = NWBGroupSpec(
        neurodata_type_def="OpticFiberImplantSite",
        neurodata_type_inc="OptogeneticStimulusSite",
        doc=("Information about the orthogonal stereotactic coordinates and angles of the optic fiber implant site"
             "site (e.g., tip of the optic fiber in the brain) and excitation wavelength."),
        attributes=[
            NWBAttributeSpec(
                name="reference",
                doc=("Reference point for `ap`, `ml`, and `dv` coordinates, e.g., bregma at the cortical surface."),
                dtype="text",
            ),
            NWBAttributeSpec(
                name="ap",
                doc=("Anteroposterior coordinate in mm of the optogenetic stimulus site (+ is anterior), "
                     "with reference to `reference`."),
                dtype="float",
            ),
            NWBAttributeSpec(
                name="ml",
                doc=("Mediolateral coordinate in mm of the optogenetic stimulus site (+ is right), "
                     "with reference to `reference`."),
                dtype="float",
            ),
            NWBAttributeSpec(
                name="dv",
                doc=("Dorsoventral coordinate in mm of the optogenetic stimulus site "
                     "(+ is dorsal/above the brain), with reference to `reference`."),
                dtype="float",
            ),
            NWBAttributeSpec(
                name="pitch",
                doc="Pitch angle in degrees (rotation around left-right axis).",
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="yaw",
                doc="Yaw angle in degrees (rotation around dorsal-ventral axis).",
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="roll",
                doc="Roll angle in degrees (rotation around anterior-posterior axis).",
                dtype="float",
                required=False,
            ),
            # TODO allow time series representing changing power of laser over time
            NWBAttributeSpec(
                name="power",
                doc=("Constant power of laser, in watts, e.g., 0.077 W (77 mW)."),
                dtype="float",
            ),
        ],
        links = [
            NWBLinkSpec(
                name="device",  # override existing "device" link
                doc="Link to the laser device.",
                target_type="Laser",  # TODO test this
            ),
            NWBLinkSpec(
                name="optic_fiber",
                doc="Link to the optic fiber device.",
                target_type="OpticFiber",
            )
        ],
    )

    optogenetic_virus = NWBGroupSpec(
        neurodata_type_def="OptogeneticVirus",
        neurodata_type_inc="NWBContainer",
        doc="Metadata about the optogenetic virus.",
        attributes=[
            NWBAttributeSpec(
                name="construct_name",
                doc=('Name of the virus construct/vector, e.g., "AAV-EF1a-DIO-hChR2(H134R)-EYFP".'),
                dtype="text",
            ),
            NWBAttributeSpec(
                name="description",
                doc=("Description of the optogenetic virus."),
                dtype="text",
                required=False,
            ),
            NWBAttributeSpec(
                name="manufacturer",
                doc=("Manufacturer of the optogenetic virus."),
                dtype="text",
            ),
            NWBAttributeSpec(
                name="titer",
                doc=("Titer of the optogenetic virus, in vg/ml, e.g., 1x10^12 vg/ml."),
                dtype="int",
            )
        ],
    )

    optogenetic_virus_injection = NWBGroupSpec(
        neurodata_type_def="OptogeneticVirusInjection",
        neurodata_type_inc="NWBContainer",
        doc=("Information about the injection of a virus for optogenetic experiments. "
             'The name should be the virus name, e.g., "AAV-EF1a-DIO-hChR2(H134R)-EYFP". '
             "Use two OptogeneticVirusInjection objects for a bilateral injection, one per hemisphere. "
             "If exact coordinates or injection volume is not known, please elaborate in the description field."),
        attributes=[
            NWBAttributeSpec(
                name="description",
                doc=("Description of the optogenetic virus injection."),
                dtype="text",
                required=False,
            ),
            NWBAttributeSpec(
                name="location",
                doc=("Name of the targeted location of the optogenetic virus injection."),
                dtype="text",
            ),
            NWBAttributeSpec(
                name="reference",
                doc=("Reference point for `ap`, `ml`, and `dv` coordinates, e.g., bregma at the cortical surface."),
                dtype="text",
            ),
            NWBAttributeSpec(
                name="ap",
                doc=("Anteroposterior coordinate in mm of the optogenetic virus injection site (+ is anterior), "
                     "with reference to `reference`."),
                dtype="float",
            ),
            NWBAttributeSpec(
                name="ml",
                doc=("Mediolateral coordinate in mm of the optogenetic virus injection site (+ is right), "
                     "with reference to `reference`."),
                dtype="float",
            ),
            NWBAttributeSpec(
                name="dv",
                doc=("Dorsoventral coordinate in mm of the optogenetic virus injection site "
                     "(+ is dorsal/above the brain), with reference to `reference`."),
                dtype="float",
            ),
            # NWBAttributeSpec(
            #     name="pitch",
            #     doc="Pitch angle in degrees (rotation around left-right axis).",
            #     dtype="float",
            #     required=False,
            # ),
            # NWBAttributeSpec(
            #     name="yaw",
            #     doc="Yaw angle in degrees (rotation around dorsal-ventral axis).",
            #     dtype="float",
            #     required=False,
            # ),
            # NWBAttributeSpec(
            #     name="roll",
            #     doc="Roll angle in degrees (rotation around anterior-posterior axis).",
            #     dtype="float",
            #     required=False,
            # ),
            NWBAttributeSpec(
                name="volume",
                doc=("Volume of injection, in uL., e.g., 0.45 uL (450 nL)"),
                dtype="float",
            ),
            NWBAttributeSpec(
                name="injection_date",
                doc=("Date of injection."),
                dtype="isodatetime",
                required=False,
            ),
        ],
        links=[
            NWBLinkSpec(
                name="virus",
                doc=("Link to OptogeneticVirus object with metadata about the name, manufacturer, and titer."),
                target_type="OptogeneticVirus",
            )
        ]
    )

    optogenetic_viruses = NWBGroupSpec(
        name="optogenetic_viruses",  # use fixed name, for use in OptogeneticExperimentMetadata
        neurodata_type_def="OptogeneticViruses",
        neurodata_type_inc="NWBContainer",
        doc=(
            "Group containing one or more OptogeneticVirus objects, to be used within an "
            "OptogeneticExperimentMetadata object."
        ),
        groups=[
            NWBGroupSpec(
                neurodata_type_inc="OptogeneticVirus",
                doc="OptogeneticVirus object(s).",
                quantity="+",
            ),
        ],
    )

    optogenetic_virus_injections = NWBGroupSpec(
        name="optogenetic_virus_injections",  # use fixed name, for use in OptogeneticExperimentMetadata
        neurodata_type_def="OptogeneticVirusInjections",
        neurodata_type_inc="NWBContainer",
        doc=(
            "Group containing one or more OptogeneticVirusInjection objects, to be used within an "
            "OptogeneticExperimentMetadata object."
        ),
        groups=[
            NWBGroupSpec(
                neurodata_type_inc="OptogeneticVirusInjection",
                doc="OptogeneticVirusInjection object(s).",
                quantity="+",
            ),
        ],
    )

    optogenetic_experiment_metadata = NWBGroupSpec(
        neurodata_type_def="OptogeneticExperimentMetadata",
        neurodata_type_inc="LabMetaData",
        doc="General metadata about the optogenetic stimulation.",
        name="optogenetics_metadata",
        attributes=[
            NWBAttributeSpec(
                name="stimulation_software",
                doc=("Name of the software used to deliver optogenetic stimulation."),
                dtype="text",
            ),
        ],
        groups=[
            NWBGroupSpec(
                name="optogenetic_viruses",
                neurodata_type_inc="OptogeneticViruses",
                doc="Group containing of one or more OptogeneticVirus objects.",
            ),
            NWBGroupSpec(
                name="optogenetic_virus_injections",
                neurodata_type_inc="OptogeneticVirusInjections",
                doc="Group containing one or more OptogeneticVirusInjection objects.",
            ),
        ]
    )

    optogenetic_epochs = NWBGroupSpec(
        neurodata_type_def="OptogeneticEpochs",
        neurodata_type_inc="TimeIntervals",
        doc="General metadata about the optogenetic stimulation that may change per epoch.",
        datasets=[
            NWBDatasetSpec(
                name="stimulation_on",
                neurodata_type_inc="VectorData",
                doc=("Whether optogenetic stimulation was used at any time during this epoch. If False, then "
                     "all other metadata values should be 0."),
                dtype="bool",
            ),
            NWBDatasetSpec(
                name="pulse_length_ms",
                neurodata_type_inc="VectorData",
                doc=("Duration of one pulse, in ms."),
                dtype="int",
            ),
            NWBDatasetSpec(
                name="period_ms",
                neurodata_type_inc="VectorData",
                doc=("Duration between the starts of two pulses, in ms. "
                     "Note that the interpulse interval = `period_ms` - `pulse_length_ms`"),
                dtype="int",
            ),
            NWBDatasetSpec(
                name="number_pulses_per_pulse_train",
                neurodata_type_inc="VectorData",
                doc=("Number of pulses in one pulse train. After this number of pulses, no more stimulation "
                     "occurs until the next train begins (see `intertrain_interval_ms`)"),
                dtype="int",
            ),
            NWBDatasetSpec(
                name="number_trains",
                neurodata_type_inc="VectorData",
                doc=("Number of trains per stimulus. After this number of trains, no more stimulation "
                     "occurs until stimulation is re-triggered, e.g., after the animal leaves the spatial filter "
                     "and returns."),
                dtype="int",
            ),
            NWBDatasetSpec(
                name="intertrain_interval_ms",
                neurodata_type_inc="VectorData",
                doc=("Duration between the starts of two consecutive pulse trains, in ms. "
                     "Determines the frequency of stimulation."),
                dtype="int",
            ),
        ],
    )
    frank_lab_optogenetic_epochs = NWBGroupSpec(
        neurodata_type_def="FrankLabOptogeneticEpochs",
        neurodata_type_inc="OptogeneticEpochs",
        doc=("General metadata about the optogenetic stimulation that may change per epoch, with fields "
             "specific to Loren Frank Lab experiments. If the spatial filter is ON, then the experimenter "
             "can stimulate in either open (frequency-based) or closed loop (theta-based), only when animal is in "
             "a particular position. If the spatial filter is OFF, then ignore the position "
             "(this is not common / doesn't happen). If the spatial filter is ON and the experimeter is "
             "stimulating in open loop mode and the animal enters the spatial filter rectangle, then "
             "immediately apply one and only one stimulation bout. If stimulating in closed loop mode and the animal "
             "enters the rectangle, then every time the particular theta phase is detected, "
             "immediately apply one stimulation bout (accounting for the lockout period)."),
        # TODO some lab members have other filters. Add those parameters below.
        datasets=[
            NWBDatasetSpec(
                name="epoch_name",
                neurodata_type_inc="VectorData",
                doc=("Name of the epoch."),
                dtype="text",
            ),
            NWBDatasetSpec(
                name="convenience_code",
                neurodata_type_inc="VectorData",
                doc=("Convenience code of the epoch."),
                dtype="text",
            ),
            NWBDatasetSpec(
                name="theta_filter_on",
                neurodata_type_inc="VectorData",
                doc=("Whether the theta filter was on. A theta filter is closed-loop stimulation - read one "
                     "tetrode and calculate the phase. Depending on the phase of theta, apply stimulation "
                     "immediately. "
                     "If this column is not present, then the theta filter was not used."),
                dtype="bool",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="theta_filter_lockout_period_samples",
                neurodata_type_inc="VectorData",
                doc=("If the theta filter was used, lockout period in the number of samples (based on the "
                     "clock of the SpikeGadgets hardware). minimum number of samples needed between stimulations. start to start."),
                dtype="uint",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="theta_filter_phase_degrees",
                neurodata_type_inc="VectorData",
                doc=("If the theta filter was used, phase in degrees during closed-loop theta phase-specific "
                     "stimulation experiments. 0 is defined as the trough. 90 is ascending phase. Options are: "
                     "0, 90, 180, 270, 360"),  # TODO validate this in API
                dtype="uint",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="theta_filter_reference_ntrode",
                neurodata_type_inc="VectorData",
                doc=("If the theta filter was used, reference electrode that used used for theta phase-specific "
                     "stimulation. ntrode is related to SpikeGadgets. ntrodes are specified in the electrode groups. "
                     "(note that ntrodes are 1-indexed.) mapping from ntrode to electrode ID is in the electrode "
                     "metadata files."),
                dtype="uint",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="spatial_filter_on",
                neurodata_type_inc="VectorData",
                doc=("Whether the spatial filter was on. Closed-loop stimulation based on whether the position of "
                     "the animal is within a specified rectangular region of the video. "
                     "If this column is not present, then the spatial filter was not used."),
                dtype="bool",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="spatial_filter_lockout_period_samples",
                neurodata_type_inc="VectorData",
                doc=("If the spatial filter was used, lockout period in the number of samples. "
                     "Uses trodes time (samplecount)."),
                dtype="uint",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="spatial_filter_bottom_left_coord",
                neurodata_type_inc="VectorData",
                doc=("If the spatial filter was used, the (x, y) coordinate of the bottom-left corner pixel of the "
                     "rectangular region of the video that was used for space-specific stimulation. "
                     "(0,0) is the bottom-left corner of the video."),
                dtype="uint",
                shape=(2, ),
                dims=("x y", ),
                quantity="?",
            ),
            NWBDatasetSpec(
                name="spatial_filter_top_right_coord",
                neurodata_type_inc="VectorData",
                doc=("If the spatial filter was used, the (x, y) coordinate of the top-right corner pixel of the "
                     "rectangular region of the video that was used for space-specific stimulation. "
                     "(0,0) is the bottom-left corner of the video."),
                dtype="uint",
                shape=(2, ),
                dims=("x y", ),
                quantity="?",
            ),
            NWBDatasetSpec(
                name="ripple_filter_on",
                neurodata_type_inc="VectorData",
                doc=("Whether the ripple filter was on. Closed-loop stimulation based on whether a ripple was "
                     "detected - whether N tetrodes have their signal cross the standard deviation threshold. "
                     "If this column is not present, then the ripple filter was not used."),
                dtype="bool",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="ripple_filter_lockout_period_samples",
                neurodata_type_inc="VectorData",
                doc=("If the ripple filter was used, lockout period in the number of samples. "
                     "Uses trodes time (samplecount)."),
                dtype="uint",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="ripple_filter_threshold_sd",
                neurodata_type_inc="VectorData",
                doc=("If the ripple filter was used, the threshold for detecting a ripple, in number of "
                     "standard deviations."),
                dtype="float",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="ripple_filter_num_above_threshold",
                neurodata_type_inc="VectorData",
                doc=("If the ripple filter was used, the number of tetrodes that have their signal cross "
                     "the standard deviation threshold."),
                dtype="uint",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="spatial_filter_cameras_index",
                neurodata_type_inc="VectorIndex",
                doc=("Index column for `spatial_filter_cameras`."),
                quantity="?",
            ),
            NWBDatasetSpec(
                name="spatial_filter_cameras",
                neurodata_type_inc="VectorData",
                doc=("If the ripple filter was used, the number of tetrodes that have their signal cross "
                     "the standard deviation threshold."),
                dtype=NWBRefSpec(
                    target_type="Device",
                    reftype="object",
                ),
                quantity="?",
            ),
        ],
    )

    new_data_types = [
        laser,
        optic_fiber,
        optic_fiber_implant_site,
        optogenetic_virus,
        optogenetic_virus_injection,
        optogenetic_viruses,
        optogenetic_virus_injections,
        optogenetic_experiment_metadata,
        optogenetic_epochs,
        frank_lab_optogenetic_epochs,
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
