from hdmf.common import DynamicTable
from hdmf.utils import docval, get_docval, AllowPositional

from pynwb import register_class
from pynwb.base import TimeSeriesReferenceVectorData
from pynwb.epoch import TimeIntervals


@register_class("OptogeneticEpochsTable", "ndx-optogenetics")
class OptogeneticEpochsTable(TimeIntervals):
    """
    General metadata about the optogenetic stimulation that may change per epoch. Some epochs have no
    stimulation and are used as control epochs. If the stimulation is on, then the epoch is a stimulation.
    """

    __columns__ = (
        {"name": "start_time", "description": "Start time of epoch, in seconds", "required": True},
        {"name": "stop_time", "description": "Stop time of epoch, in seconds", "required": True},
        {"name": "tags", "description": "user-defined tags", "index": True},
        {
            "name": "timeseries",
            "description": "index into a TimeSeries object",
            "index": True,
            "class": TimeSeriesReferenceVectorData,
        },
        {
            "name": "stimulation_on",
            "description": (
                "Whether optogenetic stimulation was used at any time during this epoch. If False, then all other "
                "metadata values should be 0."
            ),
            "required": True,
        },
        {
            "name": "pulse_length_in_ms",
            "description": "Duration of one pulse, in ms. Use NaN if stimulation was off.",
            "required": True,
        },
        {
            "name": "period_in_ms",
            "description": (
                "Duration between the starts of two pulses, in ms. Use NaN if stimulation was off. Note that the "
                "interpulse interval = `period_ms` - `pulse_length_ms`"
            ),
            "required": True,
        },
        {
            "name": "number_pulses_per_pulse_train",
            "description": (
                "Number of pulses in one pulse train. After this number of pulses, no more stimulation occurs until "
                "the next train begins (see `intertrain_interval_ms`). Use -1 if stimulation was off."
            ),
            "required": True,
        },
        {
            "name": "number_trains",
            "description": (
                "Number of trains per stimulus. After this number of trains, no more stimulation occurs until "
                "stimulation is re-triggered. Use -1 if stimulation was off."
            ),
            "required": True,
        },
        {
            "name": "intertrain_interval_in_ms",
            "description": (
                "Duration between the starts of two consecutive pulse trains, in ms. Determines the frequency of "
                "stimulation. Use NaN if stimulation was off."
            ),
            "required": True,
        },
        {
            "name": "power_in_mW",
            "description": "Constant power of excitation source throughout the epoch, in mW, e.g., 77 mW.",
            "required": True,
        },
        {
            "name": "wavelength_in_nm",
            "description": "Wavelength of the excitation source, in nm, e.g., 488 nm.",
            "required": True,
        },
        {
            "name": "optogenetic_sites",
            "description": "References row(s) of OptogeneticSitesTable.",
            "required": True,
            "table": True,
            "index": True,
        },
    )

    @docval(
        {"name": "name", "type": str, "doc": "name of this OptogeneticEpochsTable"},
        {"name": "description", "type": str, "doc": "Description of this OptogeneticEpochsTable"},
        *get_docval(DynamicTable.__init__, "id", "columns", "colnames", "target_tables"),
        allow_positional=AllowPositional.WARNING,
    )
    def __init__(self, **kwargs):
        DynamicTable.__init__(self, **kwargs)
