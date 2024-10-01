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
                # NOTE it is assumed that the fiber and ferrule are from the same manufacturer.
                # Device has only one manufacturer attribute
            ),
            NWBAttributeSpec(
                name="numerical_aperture",
                doc="Numerical aperture, e.g., 0.39 NA.",
                dtype="float",
            ),
            NWBAttributeSpec(
                name="cannula_core_diameter_in_mm",  # TODO is cladding diameter important?
                doc="Cannula diameter in mm, e.g., 0.2 mm (200 um).",
                dtype="float",
            ),
            NWBAttributeSpec(
                name="active_length_in_mm",
                doc=(
                    "Active length in mm for a tapered fiber, e.g., Optogenix Lambda fiber. "
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
                name="ferrule_diameter_in_mm",
                doc="Ferrule diameter in mm, e.g., 1.25 mm (LC) or 2.5 mm (FC).",
                dtype="float",
                required=False,
            ),
            # NWBAttributeSpec(  # TODO what is this? property of the tissue or of the fiber? measured where?
            #     name="transmittance",
            #     doc="",
            #     dtype="float",
            #     required=False,
            # ),
        ],
    )

    optic_fiber_implant_site = NWBGroupSpec(
        neurodata_type_def="OpticFiberImplantSite",
        neurodata_type_inc="OptogeneticStimulusSite",
        doc=("Information about the orthogonal stereotactic coordinates and angles of the optic fiber implant site "
             "(e.g., tip of the optic fiber in the brain) and excitation wavelength."),
        attributes=[
            NWBAttributeSpec(
                name="reference",
                doc=('Reference point for `ap_in_mm`, `ml_in_mm`, and `dv_in_mm` coordinates, e.g., '
                     '"bregma at the cortical surface".'),
                dtype="text",
            ),
            NWBAttributeSpec(
                name="hemisphere",
                doc=('The hemisphere ("left" or "right") of the targeted location of the optogenetic stimulus '
                     'site. Should be consistent with `ml_in_mm` coordinate.'),
                dtype="text",
            ),
            NWBAttributeSpec(
                name="ap_in_mm",
                doc=("Anteroposterior coordinate in mm of the optogenetic stimulus site (+ is anterior), "
                     "with reference to `reference`."),
                dtype="float",
            ),
            NWBAttributeSpec(
                name="ml_in_mm",
                doc=("Mediolateral coordinate in mm of the optogenetic stimulus site (+ is right), "
                     "with reference to `reference`."),
                dtype="float",
            ),
            NWBAttributeSpec(
                name="dv_in_mm",
                doc=("Dorsoventral coordinate in mm of the optogenetic stimulus site "
                     "(+ is dorsal/above the brain), with reference to `reference`."),
                dtype="float",
            ),
            NWBAttributeSpec(
                name="pitch_in_deg",
                doc=("Pitch angle in degrees of the optic fiber implant (rotation around left-right axis, "
                    "+ is rotating the nose upward)."),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="yaw_in_deg",
                doc=("Yaw angle in degrees of the optic fiber implant (rotation around dorsal-ventral axis, "
                     "+ is rotating the nose rightward)."),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="roll_in_deg",
                doc=("Roll angle in degrees of the optic fiber implant (rotation around anterior-posterior axis, "
                     "+ is rotating the right side downward)."),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="stereotactic_rotation_in_deg",
                doc=("TODO"),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="stereotactic_tilt_in_deg",
                doc=("TODO"),
                dtype="float",
                required=False,
            ),
            # NWBAttributeSpec(  # TODO not sure if this is necessary
            #     name="intensity_in_mW_per_mm2",
            #     doc=("Laser light intensity, in mW/mm^2, e.g., 0.5 mW/mm^2."),
            #     dtype="float",
            # ),
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
                name="titer_in_vg_per_ml",
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
             "Use two OptogeneticVirusInjection objects for a bilateral injection, one per hemisphere."),
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
                name="hemisphere",
                doc=('The hemisphere ("left" or "right") of the targeted location of the optogenetic virus '
                     'injection. Should be consistent with `ml_in_mm` coordinate.'),
                dtype="text",
            ),
            NWBAttributeSpec(
                name="reference",
                doc=('Reference point for `ap_in_mm`, `ml_in_mm`, and `dv_in_mm` coordinates, e.g., '
                     '"bregma at the cortical surface".'),
                dtype="text",
            ),
            NWBAttributeSpec(
                name="ap_in_mm",
                doc=("Anteroposterior coordinate in mm of the optogenetic virus injection site (+ is anterior), "
                     "with reference to `reference`."),
                dtype="float",
            ),
            NWBAttributeSpec(
                name="ml_in_mm",
                doc=("Mediolateral coordinate in mm of the optogenetic virus injection site (+ is right), "
                     "with reference to `reference`."),
                dtype="float",
            ),
            NWBAttributeSpec(
                name="dv_in_mm",
                doc=("Dorsoventral coordinate in mm of the optogenetic virus injection site "
                     "(+ is dorsal/above the brain), with reference to `reference`."),
                dtype="float",
            ),
            NWBAttributeSpec(
                name="pitch_in_deg",
                doc=("Pitch angle in degrees of the optogenetic virus injection (rotation around left-right axis, "
                    "+ is rotating the nose upward)."),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="yaw_in_deg",
                doc=("Yaw angle in degrees of the optogenetic virus injection (rotation around dorsal-ventral axis, "
                     "+ is rotating the nose clockwise)."),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="roll_in_deg",
                doc=("Roll angle in degrees of the optogenetic virus injection (rotation around anterior-posterior "
                     "axis, + is rotating the right side down)."),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="stereotactic_rotation_in_deg",
                doc=("TODO"),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="stereotactic_tilt_in_deg",
                doc=("TODO"),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="volume_in_uL",
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
        name="optogenetic_experiment_metadata",  # this goes against best practices but is consistent with core schema naming
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

    optogenetic_epochs_table = NWBGroupSpec(
        neurodata_type_def="OptogeneticEpochsTable",
        neurodata_type_inc="TimeIntervals",
        doc=("General metadata about the optogenetic stimulation that may change per epoch. Some epochs have no "
             "stimulation and are used as control epochs. If the stimulation is on, then the epoch is a stimulation."),
        datasets=[
            NWBDatasetSpec(
                name="stimulation_on",
                neurodata_type_inc="VectorData",
                doc=("Whether optogenetic stimulation was used at any time during this epoch. If False, then "
                     "all other metadata values should be 0."),
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
                doc=("Duration between the starts of two pulses, in ms. Use NaN if stimulation was off."
                     "Note that the interpulse interval = `period_ms` - `pulse_length_ms`"),
                dtype="float",
            ),
            NWBDatasetSpec(
                name="number_pulses_per_pulse_train",
                neurodata_type_inc="VectorData",
                doc=("Number of pulses in one pulse train. After this number of pulses, no more stimulation "
                     "occurs until the next train begins (see `intertrain_interval_ms`). "
                     "Use -1 if stimulation was off."),
                dtype="int",
            ),
            NWBDatasetSpec(
                name="number_trains",
                neurodata_type_inc="VectorData",
                doc=("Number of trains per stimulus. After this number of trains, no more stimulation "
                     "occurs until stimulation is re-triggered, e.g., after the animal leaves the spatial filter "
                     "and returns. Use -1 if stimulation was off."),
                dtype="int",
            ),
            NWBDatasetSpec(
                name="intertrain_interval_in_ms",
                neurodata_type_inc="VectorData",
                doc=("Duration between the starts of two consecutive pulse trains, in ms. "
                     "Determines the frequency of stimulation. Use NaN if stimulation was off."),
                dtype="float",
            ),
            # TODO allow time series representing changing power of laser over time
            NWBDatasetSpec(
                name="power_in_mW",
                neurodata_type_inc="VectorData",
                doc="Constant power of laser, in mW, e.g., 77 mW.",
                dtype="float",
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
        optogenetic_epochs_table,
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
