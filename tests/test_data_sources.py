from desk import data_sources

# A tiny XBRL instance with the traps found on the first real run: the same fact in GBP and USD,
# Diageo's own "deo:" tag for net sales, and a dimension-qualified fact that must be ignored.
XBRL = b"""<?xml version="1.0"?>
<xbrl xmlns="http://www.xbrl.org/2003/instance" xmlns:deo="http://diageo.com/20240630"
      xmlns:ifrs-full="https://xbrl.ifrs.org/taxonomy/2023-03-23/ifrs-full" xmlns:xbrldi="http://xbrl.org/2006/xbrldi">
  <context id="FY24"><entity><identifier scheme="x">1</identifier></entity>
    <period><startDate>2023-07-01</startDate><endDate>2024-06-30</endDate></period></context>
  <context id="H2"><entity><identifier scheme="x">1</identifier></entity>
    <period><startDate>2024-01-01</startDate><endDate>2024-06-30</endDate></period></context>
  <context id="FY24_NA"><entity><identifier scheme="x">1</identifier>
    <segment><xbrldi:explicitMember dimension="ifrs-full:SegmentsAxis">deo:NorthAmericaMember</xbrldi:explicitMember></segment></entity>
    <period><startDate>2023-07-01</startDate><endDate>2024-06-30</endDate></period></context>
  <deo:NetSales contextRef="FY24" unitRef="usd" decimals="-6">20269000000</deo:NetSales>
  <deo:NetSales contextRef="FY24" unitRef="gbp" decimals="-6">16000000000</deo:NetSales>
  <deo:NetSales contextRef="H2" unitRef="usd" decimals="-6">9000000000</deo:NetSales>
  <deo:NetSales contextRef="FY24_NA" unitRef="usd" decimals="-6">8000000000</deo:NetSales>
  <ifrs-full:Revenue contextRef="FY24" unitRef="usd" decimals="-6">27891000000</ifrs-full:Revenue>
</xbrl>"""


def test_parse_instance_keeps_prefixes_units_and_dimensions():
    facts = data_sources.parse_instance(XBRL)
    assert set(facts["tag"]) == {"deo:NetSales", "ifrs-full:Revenue"}
    assert (facts["dims"] != "").sum() == 1


def test_pick_uses_full_year_usd_group_figure_only():
    facts = data_sources.parse_instance(XBRL)
    # not the GBP figure, not the half year, not the North America segment
    assert data_sources._pick(facts, "deo:NetSales", "2024-06-30") == 20269e6
    assert data_sources._pick(facts, "deo:NetSales", "2024-06-30", unit="gbp") == 16000e6
    assert data_sources._pick(facts, "deo:NetSales", "2023-06-30") is None


def test_net_sales_is_not_revenue_including_excise():
    assert data_sources.TAGS["net_sales"] == ["deo:NetSales"]
    assert "ifrs-full:Revenue" not in data_sources.TAGS["net_sales"]
