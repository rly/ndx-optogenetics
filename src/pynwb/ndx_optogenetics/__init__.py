from importlib.resources import files
import os
from pynwb import load_namespaces, get_class

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = files(__name__)
__spec_path = __location_of_this_file / "spec" / "ndx-optogenetics.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not os.path.exists(__spec_path):
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / "ndx-optogenetics.namespace.yaml"

# Load the namespace
load_namespaces(str(__spec_path))

ExcitationSourceModel = get_class("ExcitationSourceModel", "ndx-optogenetics")
ExcitationSource = get_class("ExcitationSource", "ndx-optogenetics")
OpticalFiberModel = get_class("OpticalFiberModel", "ndx-optogenetics")
OpticalFiber = get_class("OpticalFiber", "ndx-optogenetics")
OpticalFiberLocationsTable = get_class("OpticalFiberLocationsTable", "ndx-optogenetics")
OptogeneticVirus = get_class("OptogeneticVirus", "ndx-optogenetics")
OptogeneticVirusInjection = get_class("OptogeneticVirusInjection", "ndx-optogenetics")
OptogeneticViruses = get_class("OptogeneticViruses", "ndx-optogenetics")
OptogeneticVirusInjections = get_class("OptogeneticVirusInjections", "ndx-optogenetics")
OptogeneticExperimentMetadata = get_class("OptogeneticExperimentMetadata", "ndx-optogenetics")

from .optogenetics import OptogeneticEpochsTable

__all__ = [
    "ExcitationSourceModel",
    "ExcitationSource",
    "OpticalFiberModel",
    "OpticalFiber",
    "OpticalFiberLocationsTable",
    "OptogeneticVirus",
    "OptogeneticVirusInjection",
    "OptogeneticViruses",
    "OptogeneticVirusInjections",
    "OptogeneticExperimentMetadata",
    "OptogeneticEpochsTable",
]

# Remove these functions/modules from the package
del load_namespaces, get_class, files, os, __location_of_this_file, __spec_path
