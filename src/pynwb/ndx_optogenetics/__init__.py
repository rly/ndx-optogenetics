from importlib.resources import files
from pynwb import load_namespaces, get_class

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = files(__name__)
__spec_path = __location_of_this_file / "spec" / "ndx-optogenetics.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not __spec_path.exists():
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / "ndx-optogenetics.namespace.yaml"

# Load the namespace
# ndx-optogenetics depends on ndx-ophys-devices,
# so importing it here prevents namespace errors when users import this package directly
import ndx_ophys_devices  # noqa: F401

load_namespaces(str(__spec_path))

ExcitationSourceModel = get_class("ExcitationSourceModel", "ndx-optogenetics")
ExcitationSource = get_class("ExcitationSource", "ndx-optogenetics")
OpticalFiberModel = get_class("OpticalFiberModel", "ndx-optogenetics")
OpticalFiber = get_class("OpticalFiber", "ndx-optogenetics")
OptogeneticSitesTable = get_class("OptogeneticSitesTable", "ndx-optogenetics")
OptogeneticViruses = get_class("OptogeneticViruses", "ndx-optogenetics")
OptogeneticVirusInjections = get_class("OptogeneticVirusInjections", "ndx-optogenetics")
OptogeneticEffectors = get_class("OptogeneticEffectors", "ndx-optogenetics")
OptogeneticExperimentMetadata = get_class("OptogeneticExperimentMetadata", "ndx-optogenetics")

from .optogenetics import OptogeneticEpochsTable

__all__ = [
    "ExcitationSourceModel",
    "ExcitationSource",
    "OpticalFiberModel",
    "OpticalFiber",
    "OptogeneticSitesTable",
    "OptogeneticViruses",
    "OptogeneticVirusInjections",
    "OptogeneticEffectors",
    "OptogeneticExperimentMetadata",
    "OptogeneticEpochsTable",
]

# Remove these functions/modules from the package
del load_namespaces, get_class, files, __location_of_this_file, __spec_path
