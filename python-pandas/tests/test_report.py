import pytest

from report import SALES, build_report, column_types, save, summary_by_region


@pytest.fixture
def report():
    return build_report(SALES)


def test_build_report_adds_revenue(report):
    assert len(report) == 4
    assert list(report["revenue"]) == [30.0, 28.0, 12.0, 22.5]
    assert list(report["region"]) == ["North", "South", "North", "East"]


def test_summary_averages_numbers_per_region(report):
    summary = summary_by_region(report)
    assert sorted(summary.index) == ["East", "North", "South"]
    assert summary.loc["North", "units"] == 7.5
    assert summary.loc["North", "revenue"] == 21.0
    assert "product" not in summary.columns  # text columns are left out of the averages


def test_column_types(report):
    types = column_types(report)
    assert set(types) == {"region", "product", "units", "price", "revenue"}
    assert types["price"] == "float64" and types["revenue"] == "float64"


def test_save_writes_csv(report, tmp_path):
    path = tmp_path / "out.csv"
    save(report, path)
    raw = path.read_bytes()
    assert b"\r\n" not in raw
    lines = raw.decode().splitlines()
    assert lines[0] == "region,product,units,price,revenue"
    assert lines[1] == "North,Widget,12,2.5,30.0"
