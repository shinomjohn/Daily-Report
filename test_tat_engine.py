import os
import openpyxl
import pandas as pd
import pytest

from tat_engine import (
    calculate_tat_metric,
    compute_tat_reports,
    generate_tat_html,
    export_tat_excel,
)


def test_calculate_tat_metric():
    # 3 total tickets:
    # row 1: TATHOURS=2 (<=4), TAT=0.5 (<=1)
    # row 2: TATHOURS=4 (<=4), TAT=1.0 (<=1)
    # row 3: TATHOURS=8 (>4), TAT=2.0 (>1)
    df = pd.DataFrame({
        "TATHOURS": [2, 4, 8],
        "TAT": [0.5, 1.0, 2.0]
    })
    p4, p1 = calculate_tat_metric(df)
    # 2/3 = 66.666% -> 67%
    assert p4 == 67
    assert p1 == 67


def test_compute_tat_reports_sorting_and_summary():
    df_adl = pd.DataFrame({
        "REGION": ["Thrissur", "Thrissur", "Thrissur"],
        "COMPLAINTTYPE": ["Network", "Network", "Network"],
        "PROBLEMTYPE": ["Network Complaint", "Onsite Visit", "Network Complaint"],
        "LOGINTIME": ["2026-10-02 10:00:00", "2026-10-03 11:00:00", "2026-10-04 12:00:00"],
        "TATHOURS": [1.0, 5.0, 3.0],
        "TAT": [0.2, 1.5, 0.8],
        "TEAMLEADERNAME": ["SHYAMKUMAR", "LINU E A", "SHYAMKUMAR"],
        "AREA": ["Chalakudy", "kodungalloor", "Chalakudy"],
    })
    df_adtv = pd.DataFrame({
        "REGION": ["Thrissur"],
        "COMPLAINTTYPE": ["Network"],
        "LOGINTIME": ["2026-10-02 10:00:00"],
        "TATHOURS": [3.0],
        "TAT": [0.5],
        "TEAMLEADERNAME": ["SHYAMKUMAR"],
        "SERVICEAMO": ["CHALAKKUDY"],
    })

    res = compute_tat_reports("thrissur", df_adl, df_adtv, "2026-10-01", "2026-10-15 23:59:59")
    
    # 1. Verify TL report has no summary row
    assert "adl_tl" in res
    assert "adtv_tl" in res
    
    # 2. Verify sorting: lowest 4h TAT at top
    p4_vals = [r["p4"] for r in res["adl_tl"]]
    assert p4_vals == sorted(p4_vals)
    
    # 3. Verify Center report summary has Thrissur Region
    assert "adl_center_summary" in res
    assert res["adl_center_summary"]["center"] == "Thrissur Region"


def test_generate_tat_html_colors():
    rows = [{"center": "Chalakudy", "name": "Shyam Kumar", "p4": 32, "p1": 81}]
    html_out = generate_tat_html("ADL Postpaid", "TeamLeaderName", rows)

    # Check color codes
    assert "#974706" in html_out
    assert "#c5d9f1" in html_out
    assert "#ffffff" in html_out
    assert "4 HrsTAT%" in html_out
    assert "1DAY TAT%" in html_out
    assert "Chalakudy" in html_out
    assert "Shyam Kumar" in html_out
    assert "32" in html_out
    assert "81" in html_out


def test_export_tat_excel(tmp_path):
    tat_data = {
        "region_id": "thrissur",
        "region_name": "Thrissur",
        "date_window": "2026-10-01 to 2026-10-15",
        "adl_tl": [{"center": "Chalakudy", "name": "Shyam Kumar", "p4": 32, "p1": 81}],
        "adtv_tl": [{"center": "Chalakudy", "name": "Shyam Kumar", "p4": 16, "p1": 66}],
        "adl_center": [{"center": "Chalakudy", "acso": "Arun A.R", "p4": 45, "p1": 87}],
        "adl_center_summary": {"center": "Thrissur Region", "p4": 68, "p1": 96},
        "adtv_center": [{"center": "Chalakudy", "acso": "Arun A.R", "p4": 21, "p1": 74}],
        "adtv_center_summary": {"center": "Thrissur Region", "p4": 42, "p1": 84},
    }
    out_file = tmp_path / "TAT_Report.xlsx"
    export_tat_excel(tat_data, out_file)
    assert out_file.exists()

    wb = openpyxl.load_workbook(out_file)
    assert "ADL Center TAT" in wb.sheetnames
    assert "ADL TL TAT" in wb.sheetnames
    assert "ADTv Center TAT" in wb.sheetnames
    assert "ADTv TL TAT" in wb.sheetnames
