"""Test that MeaningsTables on the optogenetic tables survive a write/read round trip."""

from datetime import datetime, timezone

import pytest
from pynwb import NWBFile, NWBHDF5IO

from ndx_optogenetics import OptogeneticEpochsTable, OptogeneticPulsesTable, OptogeneticSitesTable

hdmf_common = pytest.importorskip("hdmf.common")
if not hasattr(hdmf_common, "MeaningsTable"):
    pytest.skip("this version of hdmf does not support MeaningsTable", allow_module_level=True)
MeaningsTable = hdmf_common.MeaningsTable

EPOCH_ROW = dict(
    stimulation_on=True,
    pulse_length_in_ms=40.0,
    period_in_ms=250.0,
    number_pulses_per_pulse_train=100,
    number_trains=1,
    intertrain_interval_in_ms=0.0,
)


@pytest.mark.parametrize("table_cls", [OptogeneticEpochsTable, OptogeneticPulsesTable])
def test_meanings_tables_roundtrip(tmp_path, table_cls):
    nwbfile = NWBFile(
        session_description="session_description",
        identifier="identifier",
        session_start_time=datetime.now(timezone.utc),
    )
    sites_table = OptogeneticSitesTable(description="Information about the optogenetic stimulation sites.")
    nwbfile.create_processing_module(name="optogenetics", description="optogenetics").add(sites_table)

    table = table_cls(
        name="optogenetic_table",
        description="optogenetic table with a MeaningsTable",
        target_tables={"optogenetic_sites": sites_table},
    )
    table.add_column(name="condition", description="stimulation condition")
    row = dict(start_time=0.0, stop_time=1.0, power_in_mW=77.0, wavelength_in_nm=488.0, optogenetic_sites=[])
    if table_cls is OptogeneticEpochsTable:
        row.update(EPOCH_ROW)
    table.add_row(condition="a", **row)
    meanings = MeaningsTable(target=table["condition"])
    meanings.add_row(value="a", meaning="condition a")
    table.add_meanings_table(meanings)
    nwbfile.add_time_intervals(table)

    path = tmp_path / "test_meanings.nwb"
    with NWBHDF5IO(path, mode="w") as io:
        io.write(nwbfile)

    with NWBHDF5IO(path, mode="r") as io:
        read_table = io.read().intervals["optogenetic_table"]
        assert type(read_table) is table_cls
        assert list(read_table.meanings_tables) == ["condition_meanings"]
        read_meanings = read_table.get_meanings_for_column("condition")
        assert list(read_meanings["value"].data[:]) == ["a"]
        assert list(read_meanings["meaning"].data[:]) == ["condition a"]
