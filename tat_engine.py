"""
tat_engine.py
=============
Turnaround Time (TAT) Calculation and High-DPI Visual Report Generator.

Rules & Invariants:
1. Four reports:
   - ADL Broadband Team Leader TAT Report
   - ADTv Digital TV Team Leader TAT Report
   - ADL Broadband Center TAT Report
   - ADTv Digital TV Center TAT Report
2. Data Filtering:
   - ADL: Region matching softcode_region from region.json, Complaint Type == 'Network',
          Problem Type in ('Network Complaint', 'Network Complaints', 'Onsite Visit').
   - ADTv: Region matching softcode_region from region.json, Complaint Type == 'Network'.
   - Date: Month-to-Date (MTD: 1st of month to current date).
3. Formulas:
   - 4 Hrs TAT %: count(TATHOURS <= 4) / Total Resolved * 100
   - 1 Day TAT %: count(TAT <= 1) / Total Resolved * 100
   - Standard rounding to nearest whole integer (no decimals).
4. Sorting:
   - Ascending by 4 Hrs TAT % (lowest at the top, highest at the bottom).
5. Overall / Region Summary:
   - Team Leader Reports: NO summary row.
   - Center Reports: Summary row placed at the bottom, labeled '{Region} Region' (dynamically from region.json).
6. Visual Styling:
   - Title Banner: Rust / Dark Brown (#974706) with bold white text (#FFFFFF).
   - Column Headers: Ice Blue (#C5D9F1) with bold black text (#000000).
   - Data Rows: White (#FFFFFF) with bold black text (#000000), right-aligned whole numbers without '%' in cells.
   - Summary Row: Light Blue (#DCE6F1) with bold black text (#000000).
   - Borders: 1px solid black (#000000) on all cells.
"""
from __future__ import annotations

import html
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
import pandas as pd
from playwright.sync_api import sync_playwright

from config import (
    DEFAULT_REGION_ID,
    OUTPUT_DIR,
    TAT_ADL_CENTER_IMAGE_PATH,
    TAT_ADL_TL_IMAGE_PATH,
    TAT_ADTV_CENTER_IMAGE_PATH,
    TAT_ADTV_TL_IMAGE_PATH,
    TAT_EXCEL_REPORT_PATH,
)
from report_layout import get_layout_for_region


def calculate_tat_metric(subset: pd.DataFrame) -> Tuple[Optional[int], Optional[int]]:
    """Calculates whole-number (standard rounded) 4-hour and 1-day TAT percentages."""
    if len(subset) == 0:
        return None, None
    tot = len(subset)
    c4 = (pd.to_numeric(subset["TATHOURS"], errors="coerce") <= 4).sum()
    c1 = (pd.to_numeric(subset["TAT"], errors="coerce") <= 1).sum()
    p4 = round(c4 / tot * 100)
    p1 = round(c1 / tot * 100)
    return p4, p1


def compute_tat_reports(
    region_id: str,
    df_adl_raw: pd.DataFrame,
    df_adtv_raw: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Computes all 4 TAT reports for the target region and date window.
    """
    tls, acsos = get_layout_for_region(region_id)

    # Determine region config
    region_json_path = Path("region.json")
    reg_name = region_id.title()
    softcode_reg = region_id.title()
    if region_json_path.exists():
        try:
            rdata = json.loads(region_json_path.read_text(encoding="utf-8"))
            if rdata.get("region_id", "").lower() == region_id.lower():
                reg_name = rdata.get("region_name", reg_name)
                softcode_reg = rdata.get("softcode_region", softcode_reg)
        except Exception:
            pass

    # Date range default: 1st of current month to today 23:59:59
    now = datetime.now()
    if not start_date:
        start_date = now.strftime("%Y-%m-01")
    if not end_date:
        end_date = now.strftime("%Y-%m-%d 23:59:59")

    # 1. Filter ADL Broadband
    df_adl = df_adl_raw.copy()
    if "REGION" in df_adl.columns:
        df_adl = df_adl[df_adl["REGION"].astype(str).str.strip().str.lower() == softcode_reg.lower()]
    if "COMPLAINTTYPE" in df_adl.columns:
        df_adl = df_adl[df_adl["COMPLAINTTYPE"].astype(str).str.strip().str.lower() == "network"]
    if "PROBLEMTYPE" in df_adl.columns:
        df_adl = df_adl[
            df_adl["PROBLEMTYPE"].astype(str).str.strip().str.lower().isin(
                ["network complaint", "network complaints", "onsite visit"]
            )
        ]
    if "LOGINTIME" in df_adl.columns:
        df_adl["LOGIN_DT"] = pd.to_datetime(df_adl["LOGINTIME"], errors="coerce")
        df_adl = df_adl[(df_adl["LOGIN_DT"] >= start_date) & (df_adl["LOGIN_DT"] <= end_date)]

    # 2. Filter ADTv Digital TV
    df_adtv = df_adtv_raw.copy()
    if "REGION" in df_adtv.columns:
        df_adtv = df_adtv[df_adtv["REGION"].astype(str).str.strip().str.lower() == softcode_reg.lower()]
    if "COMPLAINTTYPE" in df_adtv.columns:
        df_adtv = df_adtv[df_adtv["COMPLAINTTYPE"].astype(str).str.strip().str.lower() == "network"]
    if "LOGINTIME" in df_adtv.columns:
        df_adtv["LOGIN_DT"] = pd.to_datetime(df_adtv["LOGINTIME"], errors="coerce")
        df_adtv = df_adtv[(df_adtv["LOGIN_DT"] >= start_date) & (df_adtv["LOGIN_DT"] <= end_date)]

    # Prepare lookup columns
    df_adl["TL_CLEAN"] = df_adl["TEAMLEADERNAME"].astype(str).str.strip().str.lower() if "TEAMLEADERNAME" in df_adl.columns else ""
    df_adl["AREA_CLEAN"] = df_adl["AREA"].astype(str).str.strip().str.lower() if "AREA" in df_adl.columns else ""
    df_adtv["TL_CLEAN"] = df_adtv["TEAMLEADERNAME"].astype(str).str.strip().str.lower() if "TEAMLEADERNAME" in df_adtv.columns else ""
    df_adtv["AMO_CLEAN"] = df_adtv["SERVICEAMO"].astype(str).str.strip().str.lower() if "SERVICEAMO" in df_adtv.columns else ""

    # REPORT 1: ADL Team Leader
    adl_tl = []
    for t in tls:
        k = (t.pd_adl_name_key or "").strip().lower()
        sub = df_adl[df_adl["TL_CLEAN"] == k]
        p4, p1 = calculate_tat_metric(sub)
        adl_tl.append({
            "center": t.adl_center,
            "name": t.adl_name,
            "p4": p4 if p4 is not None else 999,
            "p1": p1 if p1 is not None else 0,
            "total_tickets": len(sub),
        })
    adl_tl.sort(key=lambda x: x["p4"])

    # REPORT 2: ADTv Team Leader
    adtv_tl = []
    for t in tls:
        k = (t.pd_adtv_name_key or "").strip().lower()
        sub = df_adtv[df_adtv["TL_CLEAN"] == k]
        p4, p1 = calculate_tat_metric(sub)
        adtv_tl.append({
            "center": t.adtv_center,
            "name": t.adtv_name,
            "p4": p4 if p4 is not None else 999,
            "p1": p1 if p1 is not None else 0,
            "total_tickets": len(sub),
        })
    adtv_tl.sort(key=lambda x: x["p4"])

    # REPORT 3: ADL Center
    adl_center = []
    for a in acsos:
        k = (a.pd_adl_center_key or "").strip().lower()
        sub = df_adl[df_adl["AREA_CLEAN"] == k]
        p4, p1 = calculate_tat_metric(sub)
        adl_center.append({
            "center": a.adl_center,
            "acso": a.adl_acso,
            "p4": p4 if p4 is not None else 999,
            "p1": p1 if p1 is not None else 0,
            "total_tickets": len(sub),
        })
    adl_center.sort(key=lambda x: x["p4"])
    reg_p4_adl, reg_p1_adl = calculate_tat_metric(df_adl)
    adl_center_summary = {
        "center": f"{reg_name} Region",
        "p4": reg_p4_adl if reg_p4_adl is not None else 0,
        "p1": reg_p1_adl if reg_p1_adl is not None else 0,
        "total_tickets": len(df_adl),
    }

    # REPORT 4: ADTv Center
    adtv_center = []
    for a in acsos:
        k = (a.pd_adtv_center_key or "").strip().lower()
        sub = df_adtv[df_adtv["AMO_CLEAN"] == k]
        p4, p1 = calculate_tat_metric(sub)
        adtv_center.append({
            "center": a.adtv_center,
            "acso": a.adtv_acso,
            "p4": p4 if p4 is not None else 999,
            "p1": p1 if p1 is not None else 0,
            "total_tickets": len(sub),
        })
    adtv_center.sort(key=lambda x: x["p4"])
    reg_p4_adtv, reg_p1_adtv = calculate_tat_metric(df_adtv)
    adtv_center_summary = {
        "center": f"{reg_name} Region",
        "p4": reg_p4_adtv if reg_p4_adtv is not None else 0,
        "p1": reg_p1_adtv if reg_p1_adtv is not None else 0,
        "total_tickets": len(df_adtv),
    }

    return {
        "region_id": region_id,
        "region_name": reg_name,
        "date_window": f"{start_date} to {end_date.split()[0]}",
        "adl_tl": adl_tl,
        "adtv_tl": adtv_tl,
        "adl_center": adl_center,
        "adl_center_summary": adl_center_summary,
        "adtv_center": adtv_center,
        "adtv_center_summary": adtv_center_summary,
    }


def generate_tat_html(
    title: str,
    col2_name: str,
    rows: List[Dict[str, Any]],
    summary_row: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Generates pixel-perfect HTML table styled exactly like the user's Excel sample:
    - Banner: #974706 (Dark Brown) with white bold text
    - Header: #C5D9F1 (Ice Blue) with black bold text
    - Data: #FFFFFF with black bold text and solid 1px black borders
    - Summary: #DCE6F1 with black bold text
    """
    rows_tr = []
    for r in rows:
        c_val = html.escape(str(r["center"]))
        n_val = html.escape(str(r.get("name") or r.get("acso") or ""))
        p4_str = str(r["p4"]) if r["p4"] != 999 else "—"
        p1_str = str(r["p1"]) if r["p4"] != 999 else "—"
        rows_tr.append(f"""
        <tr>
            <td class="col-center">{c_val}</td>
            <td class="col-name">{n_val}</td>
            <td class="col-num">{p4_str}</td>
            <td class="col-num">{p1_str}</td>
        </tr>""")

    summary_tr = ""
    if summary_row:
        c_val = html.escape(str(summary_row["center"]))
        p4_s = str(summary_row["p4"])
        p1_s = str(summary_row["p1"])
        summary_tr = f"""
        <tr class="row-summary">
            <td class="col-center">{c_val}</td>
            <td class="col-name"></td>
            <td class="col-num">{p4_s}</td>
            <td class="col-num">{p1_s}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
        background: #ffffff;
        font-family: Calibri, 'Segoe UI', Arial, sans-serif;
        display: inline-block;
        padding: 4px;
        -webkit-font-smoothing: antialiased;
    }}
    .table-container {{
        border: 2px solid #000000;
        display: inline-block;
        background: #ffffff;
    }}
    table {{
        border-collapse: collapse;
        color: #000000;
        font-size: 19px;
    }}
    .banner-row th {{
        background-color: #974706;
        color: #ffffff;
        font-size: 21px;
        font-weight: bold;
        text-align: left;
        padding: 6px 12px;
        border: 1px solid #000000;
        height: 36px;
        white-space: nowrap;
    }}
    .header-row th {{
        background-color: #c5d9f1;
        color: #000000;
        font-size: 19px;
        font-weight: bold;
        padding: 6px 12px;
        border: 1px solid #000000;
        height: 34px;
        white-space: nowrap;
    }}
    td {{
        border: 1px solid #000000;
        padding: 4px 12px;
        height: 30px;
        white-space: nowrap;
        font-weight: bold;
        font-size: 19px;
    }}
    .col-center {{ text-align: left; width: 220px; min-width: 220px; }}
    .col-name {{ text-align: left; width: 240px; min-width: 240px; }}
    .col-num {{ text-align: right; width: 140px; min-width: 140px; padding-right: 14px; }}
    .row-summary td {{
        background-color: #dce6f1;
        font-weight: bold;
    }}
</style>
</head>
<body>
    <div class="table-container">
        <table>
            <thead>
                <tr class="banner-row">
                    <th colspan="4">{html.escape(title)}</th>
                </tr>
                <tr class="header-row">
                    <th style="text-align: left;">CENTER</th>
                    <th style="text-align: left;">{html.escape(col2_name)}</th>
                    <th style="text-align: right; padding-right: 14px;">4 HrsTAT%</th>
                    <th style="text-align: right; padding-right: 14px;">1DAY TAT%</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows_tr)}
                {summary_tr}
            </tbody>
        </table>
    </div>
</body>
</html>"""


def render_tat_report_images(tat_data: Dict[str, Any], output_dir: Path = OUTPUT_DIR) -> Dict[str, Path]:
    """
    Renders high-DPI images for all 4 TAT reports via Playwright.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    h_adl_c = generate_tat_html(
        "ADL Postpaid", "ACSO", tat_data["adl_center"], tat_data["adl_center_summary"]
    )
    h_adl_tl = generate_tat_html(
        "ADL Postpaid", "TeamLeaderName", tat_data["adl_tl"]
    )
    h_adtv_c = generate_tat_html(
        "ADTv Postpaid", "ACSO", tat_data["adtv_center"], tat_data["adtv_center_summary"]
    )
    h_adtv_tl = generate_tat_html(
        "ADTv Postpaid", "TeamLeaderName", tat_data["adtv_tl"]
    )

    targets = {
        "adl_center": (TAT_ADL_CENTER_IMAGE_PATH, h_adl_c),
        "adl_tl": (TAT_ADL_TL_IMAGE_PATH, h_adl_tl),
        "adtv_center": (TAT_ADTV_CENTER_IMAGE_PATH, h_adtv_c),
        "adtv_tl": (TAT_ADTV_TL_IMAGE_PATH, h_adtv_tl),
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(device_scale_factor=2)
        for key, (path, html_content) in targets.items():
            page.set_content(html_content)
            elem = page.query_selector(".table-container")
            if elem:
                elem.screenshot(path=str(path))
        browser.close()

    return {key: path for key, (path, _) in targets.items()}


def export_tat_excel(tat_data: Dict[str, Any], output_file: Path = TAT_EXCEL_REPORT_PATH) -> Path:
    """
    Exports all 4 TAT reports into a beautifully styled multi-tab Excel workbook matching sample styles.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    banner_fill = PatternFill(start_color="974706", end_color="974706", fill_type="solid")
    header_fill = PatternFill(start_color="C5D9F1", end_color="C5D9F1", fill_type="solid")
    summary_fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")

    font_banner = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=11, bold=True, color="000000")

    thin_border = Border(
        left=Side(style="thin", color="000000"),
        right=Side(style="thin", color="000000"),
        top=Side(style="thin", color="000000"),
        bottom=Side(style="thin", color="000000"),
    )

    sheets_config = [
        ("ADL Center TAT", "ADL Postpaid", "ACSO", tat_data["adl_center"], tat_data["adl_center_summary"]),
        ("ADL TL TAT", "ADL Postpaid", "TeamLeaderName", tat_data["adl_tl"], None),
        ("ADTv Center TAT", "ADTv Postpaid", "ACSO", tat_data["adtv_center"], tat_data["adtv_center_summary"]),
        ("ADTv TL TAT", "ADTv Postpaid", "TeamLeaderName", tat_data["adtv_tl"], None),
    ]

    for title_tab, title_banner, col2_name, rows, summary_row in sheets_config:
        ws = wb.create_sheet(title=title_tab)

        # Row 1: Banner
        ws.merge_cells("A1:D1")
        cell_banner = ws["A1"]
        cell_banner.value = title_banner
        cell_banner.fill = banner_fill
        cell_banner.font = font_banner
        cell_banner.alignment = Alignment(horizontal="left", vertical="center")
        for col in ["A", "B", "C", "D"]:
            ws[f"{col}1"].border = thin_border
            ws[f"{col}1"].fill = banner_fill

        # Row 2: Headers
        headers = ["CENTER", col2_name, "4 HrsTAT%", "1DAY TAT%"]
        for col_idx, h_text in enumerate(headers, 1):
            cell = ws.cell(row=2, column=col_idx, value=h_text)
            cell.fill = header_fill
            cell.font = font_bold
            cell.border = thin_border
            cell.alignment = Alignment(
                horizontal="right" if col_idx in (3, 4) else "left", vertical="center"
            )

        # Data Rows
        current_row = 3
        for r in rows:
            c_val = r["center"]
            n_val = r.get("name") or r.get("acso") or ""
            p4_val = r["p4"] if r["p4"] != 999 else ""
            p1_val = r["p1"] if r["p4"] != 999 else ""

            row_vals = [c_val, n_val, p4_val, p1_val]
            for col_idx, val in enumerate(row_vals, 1):
                cell = ws.cell(row=current_row, column=col_idx, value=val)
                cell.font = font_bold
                cell.border = thin_border
                cell.alignment = Alignment(
                    horizontal="right" if col_idx in (3, 4) else "left", vertical="center"
                )
            current_row += 1

        # Summary Row (if present)
        if summary_row:
            sum_vals = [summary_row["center"], "", summary_row["p4"], summary_row["p1"]]
            for col_idx, val in enumerate(sum_vals, 1):
                cell = ws.cell(row=current_row, column=col_idx, value=val)
                cell.fill = summary_fill
                cell.font = font_bold
                cell.border = thin_border
                cell.alignment = Alignment(
                    horizontal="right" if col_idx in (3, 4) else "left", vertical="center"
                )

        # Set column widths
        ws.column_dimensions["A"].width = 24
        ws.column_dimensions["B"].width = 28
        ws.column_dimensions["C"].width = 16
        ws.column_dimensions["D"].width = 16

    wb.save(output_file)
    return output_file


def get_latest_resolved_files(region_id: str = DEFAULT_REGION_ID) -> Tuple[Optional[Path], Optional[Path]]:
    """
    Finds the latest Broadband and DTv resolved ticket workbooks from data/ and Downloads/.
    Prefers files explicitly matching the target region if multiple exist.
    """
    from config import DATA_DIR, DOWNLOADS_DIR

    search_dirs = [DATA_DIR, DOWNLOADS_DIR, Path.home() / "Downloads"]
    adl_candidates: List[Path] = []
    adtv_candidates: List[Path] = []

    for d in search_dirs:
        if d.exists():
            adl_candidates.extend(list(d.glob("Resolved Tickets Broadband*.xlsx")))
            adtv_candidates.extend(list(d.glob("Resolved Tickets DTv*.xlsx")))

    adl_candidates.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    adtv_candidates.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    reg_clean = region_id.lower().strip()

    best_adl: Optional[Path] = None
    for f in adl_candidates:
        if f.stat().st_size > 1000:
            best_adl = f
            break

    best_adtv: Optional[Path] = None
    for f in adtv_candidates:
        if f.stat().st_size > 50000:
            try:
                wb = openpyxl.load_workbook(f, read_only=True)
                ws = wb.active
                row2 = next(ws.iter_rows(min_row=2, max_row=2, values_only=True), None)
                if row2 and len(row2) > 29 and str(row2[29]).strip().lower() == reg_clean:
                    best_adtv = f
                    break
            except Exception:
                pass
            if not best_adtv:
                best_adtv = f

    if not best_adtv and adtv_candidates:
        best_adtv = adtv_candidates[0]

    return best_adl, best_adtv


def execute_tat_pipeline(
    region_id: str = DEFAULT_REGION_ID,
    adl_file: Optional[Path | str] = None,
    adtv_file: Optional[Path | str] = None,
    render_images: bool = True,
    export_excel: bool = True,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    headless: bool = True,
    **kwargs,
) -> Dict[str, Any]:
    """
    Full automated execution pipeline for TAT reports:
    1. Loads resolved tickets.
    2. Computes the 4 reports.
    3. Renders high-DPI images with exact colors.
    4. Exports multi-tab Excel workbook.
    """
    if not adl_file or not adtv_file:
        auto_adl, auto_adtv = get_latest_resolved_files(region_id)
        adl_file = adl_file or auto_adl
        adtv_file = adtv_file or auto_adtv

    if not adl_file or not Path(adl_file).exists():
        raise FileNotFoundError("Missing Broadband Resolved Tickets workbook (Resolved Tickets Broadband*.xlsx)")
    if not adtv_file or not Path(adtv_file).exists():
        raise FileNotFoundError("Missing Digital TV Resolved Tickets workbook (Resolved Tickets DTv*.xlsx)")

    df_adl = pd.read_excel(adl_file)
    df_adtv = pd.read_excel(adtv_file)

    tat_data = compute_tat_reports(region_id, df_adl, df_adtv, start_date=start_date, end_date=end_date)

    if render_images:
        img_paths = render_tat_report_images(tat_data)
        tat_data["images"] = {k: str(v) for k, v in img_paths.items()}

    if export_excel:
        xl_path = export_tat_excel(tat_data)
        tat_data["excel_path"] = str(xl_path)

    return tat_data


def dispatch_tat_reports(
    target_recipients: List[str],
    report_type: str = "tat_all",
    region_id: str = DEFAULT_REGION_ID,
) -> bool:
    """
    Renders and dispatches TAT report cards via WhatsApp to specified recipients.
    """
    from whatsapp_sender import flash_report_image

    execute_tat_pipeline(region_id=region_id, render_images=True, export_excel=False)

    r_type = report_type.lower().strip()
    if r_type in ("tat_adl_center", "adl_center"):
        images_to_send = [TAT_ADL_CENTER_IMAGE_PATH]
    elif r_type in ("tat_adl_tl", "adl_tl"):
        images_to_send = [TAT_ADL_TL_IMAGE_PATH]
    elif r_type in ("tat_adtv_center", "adtv_center"):
        images_to_send = [TAT_ADTV_CENTER_IMAGE_PATH]
    elif r_type in ("tat_adtv_tl", "adtv_tl"):
        images_to_send = [TAT_ADTV_TL_IMAGE_PATH]
    elif r_type in ("tat_centers", "centers"):
        images_to_send = [TAT_ADL_CENTER_IMAGE_PATH, TAT_ADTV_CENTER_IMAGE_PATH]
    elif r_type in ("tat_tls", "tls"):
        images_to_send = [TAT_ADL_TL_IMAGE_PATH, TAT_ADTV_TL_IMAGE_PATH]
    else:  # tat_all
        images_to_send = [
            TAT_ADL_CENTER_IMAGE_PATH,
            TAT_ADL_TL_IMAGE_PATH,
            TAT_ADTV_CENTER_IMAGE_PATH,
            TAT_ADTV_TL_IMAGE_PATH,
        ]

    return flash_report_image(images_to_send, target_recipients=target_recipients)
