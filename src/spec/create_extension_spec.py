# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import (
    NWBNamespaceBuilder,
    export_spec,
    NWBGroupSpec,
    NWBAttributeSpec,
    NWBLinkSpec,
    NWBDatasetSpec,
    NWBRefSpec,
)

from ndx_ophys_devices import (
    ViralVector,
    ViralVectorInjection,
    Effector,
    FiberInsertion,
    OpticalFiberModel,
    ExcitationSourceModel,
    OpticalFiber,
    ExcitationSource,
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
            "uni@chymera.eu",
            "ben.dichter@catalystneuro.com",
        ],
    )
    ns_builder.include_namespace("core")
    ns_builder.include_namespace("ndx-ophys-devices")

    # NOTE: These columns could all be properties of OpticalFiber, or the optical fiber model and serial number
    # from OpticalFiber and the excitation source model and serial number from ExcitationSource could be moved into
    # this table. This split representation is more consistent with how device instances and device locations are
    # represented in other extensions.
    optical_fiber_locations_table = NWBGroupSpec(
        neurodata_type_def="OpticalFiberLocationsTable",
        neurodata_type_inc="DynamicTable",
        doc=(
            "Information about the targeted stereotactic coordinates of the tip of the implanted optical fiber "
            "and the angles of the optical fiber in the brain."
        ),
        default_name="optical_fiber_locations_table",
        datasets=[
            NWBDatasetSpec(
                name="implanted_fiber_description",
                neurodata_type_inc="VectorData",
                doc=("Description of the implanted optical fiber, e.g., 'Lambda fiber implanted into right GPe'."),
                dtype="text",
            ),
            NWBDatasetSpec(
                name="location",
                neurodata_type_inc="VectorData",
                doc=("Name of the targeted location of the tip of the optical fiber in the brain."),
                dtype="text",
            ),
            NWBDatasetSpec(
                name="hemisphere",
                neurodata_type_inc="VectorData",
                doc=(
                    'The hemisphere ("left" or "right") of the targeted location of the tip of the optical fiber. '
                    "Should be consistent with `ml_in_mm` coordinate."
                ),
                dtype="text",
            ),
            NWBDatasetSpec(
                name="ap_in_mm",
                neurodata_type_inc="VectorData",
                doc=(
                    "Anteroposterior coordinate in mm of the targeted location of the tip of the optical fiber "
                    "(+ is anterior), with reference to `reference`."
                ),
                dtype="float",
            ),
            NWBDatasetSpec(
                name="ml_in_mm",
                neurodata_type_inc="VectorData",
                doc=(
                    "Mediolateral coordinate in mm of the targeted location of the tip of the optical fiber "
                    "(+ is right), with reference to `reference`."
                ),
                dtype="float",
            ),
            NWBDatasetSpec(
                name="dv_in_mm",
                neurodata_type_inc="VectorData",
                doc=(
                    "Dorsoventral coordinate in mm of the targeted location of the tip of the optical fiber "
                    "(+ is dorsal/above the brain), with reference to `reference`."
                ),
                dtype="float",
            ),
            NWBDatasetSpec(
                name="pitch_in_deg",
                neurodata_type_inc="VectorData",
                doc=(
                    "Pitch angle in degrees of the implanted optical fiber (rotation around left-right axis, "
                    "+ is rotating the nose upward)."
                ),
                dtype="float",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="yaw_in_deg",
                neurodata_type_inc="VectorData",
                doc=(
                    "Yaw angle in degrees of the implanted optical fiber (rotation around dorsal-ventral axis, "
                    "+ is rotating the nose rightward)."
                ),
                dtype="float",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="roll_in_deg",
                neurodata_type_inc="VectorData",
                doc=(
                    "Roll angle in degrees of the implanted optical fiber (rotation around anterior-posterior axis, "
                    "+ is rotating the right side downward)."
                ),
                dtype="float",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="stereotactic_rotation_in_deg",
                neurodata_type_inc="VectorData",
                doc=("TODO"),
                dtype="float",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="stereotactic_tilt_in_deg",
                neurodata_type_inc="VectorData",
                doc=("TODO"),
                dtype="float",
                quantity="?",
            ),
            NWBDatasetSpec(
                # TODO: make this optional here and in OptogeneticStimulusSite
                # for cases when the fiber is implanted but the excitation source was not turned on
                name="excitation_source",
                neurodata_type_inc="VectorData",
                doc="The excitation source device connected to the optical fiber.",
                dtype=NWBRefSpec(
                    target_type="ExcitationSource",
                    reftype="object",
                ),
                quantity="?",
            ),
            NWBDatasetSpec(
                name="optical_fiber",
                neurodata_type_inc="VectorData",
                doc="The optical fiber device.",
                dtype=NWBRefSpec(
                    target_type="OpticalFiber",
                    reftype="object",
                ),
            ),
        ],
        attributes=[
            NWBAttributeSpec(
                name="reference",
                doc=(
                    "Zero point for `ap_in_mm`, `ml_in_mm`, and `dv_in_mm` coordinates, e.g., "
                    '"Bregma at the cortical surface".'
                ),
                dtype="text",
            ),
            # Set a fixed value for the description attribute to override the description in DynamicTable
            # TODO this does not work as expected
            # NWBAttributeSpec(
            #     name="description",
            #     doc=("Description of what is in this dynamic table."),
            #     dtype="text",
            #     value=("Information about the targeted stereotactic coordinates of the tip of the implanted optical "
            #            "fiber and the angles of the optical fiber in the brain."),
            # ),
        ],
    )
    optogenetic_viruses = NWBGroupSpec(
        name="optogenetic_viruses",  # use fixed name, for use in OptogeneticExperimentMetadata
        neurodata_type_def="OptogeneticViruses",
        neurodata_type_inc="NWBContainer",
        doc=(
            "Group containing one or more ViralVector objects, to be used within an "
            "OptogeneticExperimentMetadata object."
        ),
        groups=[
            NWBGroupSpec(
                neurodata_type_inc="ViralVector",
                doc="ViralVector object(s).",
                quantity="+",
            ),
        ],
    )

    optogenetic_virus_injections = NWBGroupSpec(
        name="optogenetic_virus_injections",  # use fixed name, for use in OptogeneticExperimentMetadata
        neurodata_type_def="OptogeneticVirusInjections",
        neurodata_type_inc="NWBContainer",
        doc=(
            "Group containing one or more ViralVectorInjection objects, to be used within an "
            "OptogeneticExperimentMetadata object."
        ),
        groups=[
            NWBGroupSpec(
                neurodata_type_inc="ViralVectorInjection",
                doc="ViralVectorInjection object(s).",
                quantity="+",
            ),
        ],
    )

    optogenetic_effectors = NWBGroupSpec(
        name="optogenetic_effectors",  # use fixed name, for use in OptogeneticExperimentMetadata
        neurodata_type_def="OptogeneticEffectors",
        neurodata_type_inc="NWBContainer",
        doc=(
            "Group containing one or more Effector objects, to be used within an "
            "OptogeneticExperimentMetadata object."
        ),
        groups=[
            NWBGroupSpec(
                neurodata_type_inc="Effector",
                doc="Effector object(s).",
                quantity="+",
            ),
        ],
    )

    optogenetic_experiment_metadata = NWBGroupSpec(
        neurodata_type_def="OptogeneticExperimentMetadata",
        neurodata_type_inc="LabMetaData",
        doc="General metadata about the optogenetic stimulation.",
        name="optogenetic_experiment_metadata",
        attributes=[
            NWBAttributeSpec(
                name="stimulation_software",
                doc=("Name of the software used to deliver optogenetic stimulation."),
                dtype="text",
            ),
        ],
        groups=[
            NWBGroupSpec(
                name="optical_fiber_locations_table",
                neurodata_type_inc="OpticalFiberLocationsTable",
                doc=(
                    "Information about the targeted stereotactic coordinates of the tip of the implanted optical "
                    "fiber and the angles of the optical fiber in the brain."
                ),
            ),
            NWBGroupSpec(
                name="optogenetic_viruses",
                neurodata_type_inc="OptogeneticViruses",
                doc="Group containing of one or more OptogeneticVirus objects.",
                quantity="?",
            ),
            NWBGroupSpec(
                name="optogenetic_virus_injections",
                neurodata_type_inc="OptogeneticVirusInjections",
                doc="Group containing one or more OptogeneticVirusInjection objects.",
                quantity="?",
            ),
            NWBGroupSpec(
                name="optogenetic_effectors",
                neurodata_type_inc="OptogeneticEffectors",
                doc="Group containing one or more OptogeneticEffector objects.",
            ),
        ],
    )

    optogenetic_epochs_table = NWBGroupSpec(
        neurodata_type_def="OptogeneticEpochsTable",
        neurodata_type_inc="TimeIntervals",
        doc=(
            "General metadata about the optogenetic stimulation that may change per epoch. Some epochs have no "
            "stimulation and are used as control epochs. If the stimulation is on, then the epoch is a stimulation."
        ),
        datasets=[
            NWBDatasetSpec(
                name="stimulation_on",
                neurodata_type_inc="VectorData",
                doc=(
                    "Whether optogenetic stimulation was used at any time during this epoch. If False, then "
                    "all other metadata values should be 0."
                ),
                dtype="bool",
            ),
            NWBDatasetSpec(
                name="pulse_length_in_ms",
                neurodata_type_inc="VectorData",
                doc=("Duration of one pulse, in ms. Use NaN if stimulation was off."),
                dtype="float",
            ),
            NWBDatasetSpec(
                name="period_in_ms",
                neurodata_type_inc="VectorData",
                doc=(
                    "Duration between the starts of two pulses, in ms. Use NaN if stimulation was off."
                    "Note that the interpulse interval = `period_ms` - `pulse_length_ms`"
                ),
                dtype="float",
            ),
            NWBDatasetSpec(
                name="number_pulses_per_pulse_train",
                neurodata_type_inc="VectorData",
                doc=(
                    "Number of pulses in one pulse train. After this number of pulses, no more stimulation "
                    "occurs until the next train begins (see `intertrain_interval_ms`). "
                    "Use -1 if stimulation was off."
                ),
                dtype="int",
            ),
            NWBDatasetSpec(
                name="number_trains",
                neurodata_type_inc="VectorData",
                doc=(
                    "Number of trains per stimulus. After this number of trains, no more stimulation "
                    "occurs until stimulation is re-triggered. Use -1 if stimulation was off."
                ),
                dtype="int",
            ),
            NWBDatasetSpec(
                name="intertrain_interval_in_ms",
                neurodata_type_inc="VectorData",
                doc=(
                    "Duration between the starts of two consecutive pulse trains, in ms. "
                    "Determines the frequency of stimulation. Use NaN if stimulation was off."
                ),
                dtype="float",
            ),
            # TODO allow time series representing changing power of excitation source over time
            NWBDatasetSpec(
                name="power_in_mW",
                neurodata_type_inc="VectorData",
                doc="Constant power of excitation source throughout the epoch, in mW, e.g., 77 mW.",
                dtype="float",
            ),
            NWBDatasetSpec(
                name="optical_fiber_locations_index",
                doc="Index to allow reference to multiple rows of the OpticalFiberLocationsTable.",
                neurodata_type_inc="VectorIndex",
            ),
            NWBDatasetSpec(
                name="optical_fiber_locations",
                doc="References row(s) of OpticalFiberLocationsTable.",
                neurodata_type_inc="DynamicTableRegion",
            ),
        ],
    )

    new_data_types = [
        optical_fiber_locations_table,
        optogenetic_viruses,
        optogenetic_virus_injections,
        optogenetic_effectors,
        optogenetic_experiment_metadata,
        optogenetic_epochs_table,
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
