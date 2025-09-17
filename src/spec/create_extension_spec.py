# -*- coding: utf-8 -*-
from pathlib import Path

from pynwb.spec import (
    NWBNamespaceBuilder,
    export_spec,
    NWBGroupSpec,
    NWBAttributeSpec,
    NWBDatasetSpec,
    NWBRefSpec,
)


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-optogenetics""",
        version="""0.3.0""",
        doc="""NWB extension to improve support for optogenetics data and metadata""",
        author=[
            "Ryan Ly",
            "Horea Christian",
            "Ben Dichter",
            "Paul Adkisson",
        ],
        contact=[
            "rly@lbl.gov",
            "uni@chymera.eu",
            "ben.dichter@catalystneuro.com",
            "paul.adkisson@catalystneuro.com",
        ],
    )
    ns_builder.include_namespace("core")
    ns_builder.include_namespace("ndx-ophys-devices")

    optogenetic_sites_table = NWBGroupSpec(
        neurodata_type_def="OptogeneticSitesTable",
        neurodata_type_inc="DynamicTable",
        doc=(
            "This table contains information about the optogenetic stimulation sites, including the excitation source, "
            "the optical fiber, and targeted effector."
        ),
        default_name="optogenetic_sites_table",
        datasets=[
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
            NWBDatasetSpec(
                name="effector",
                neurodata_type_inc="VectorData",
                doc="The effector protein, e.g., ChR2.",
                dtype=NWBRefSpec(
                    target_type="Effector",
                    reftype="object",
                ),
            ),
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
                name="optogenetic_sites_table",
                neurodata_type_inc="OptogeneticSitesTable",
                doc=(
                    "This table contains information about the optogenetic stimulation sites, "
                    "including the excitation source, the optical fiber, and targeted effector."
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
                name="wavelength_in_nm",
                neurodata_type_inc="VectorData",
                doc="Wavelength of the excitation source, in nm.",
                dtype="float",
            ),
            NWBDatasetSpec(
                name="optogenetic_sites_index",
                doc="Index to allow reference to multiple rows of the OptogeneticSitesTable.",
                neurodata_type_inc="VectorIndex",
            ),
            NWBDatasetSpec(
                name="optogenetic_sites",
                doc="References row(s) of OptogeneticSitesTable.",
                neurodata_type_inc="DynamicTableRegion",
            ),
        ],
    )

    new_data_types = [
        optogenetic_sites_table,
        optogenetic_viruses,
        optogenetic_virus_injections,
        optogenetic_effectors,
        optogenetic_experiment_metadata,
        optogenetic_epochs_table,
    ]

    # export the spec to yaml files in the root spec folder
    output_dir = str((Path(__file__).parent.parent.parent / "spec").absolute())
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
