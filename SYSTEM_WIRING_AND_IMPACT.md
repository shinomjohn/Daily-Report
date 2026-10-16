# Master Codebase Wiring, Architecture & Ripple-Impact Blueprint

> **Auto-Generated Verification Document**  
> **Last Code Synchronization**: `2026-10-16 07:03:25`  
> **Analyzed Modules**: `45 Python Files` | `450 Symbols` | `69 REST Endpoints`  

---

## 1. System High-Level Topology & Data Pipelines

The repository operates across 5 decoupled operational layers:

```mermaid
flowchart TD
    subgraph Ingestion["1. Ingestion Layer"]
        CRM["crm_downloader.py (Softcode/Prepaid CRM)"]
        RawUpload["web_server.py /api/complaints/upload-raw"]
        SRUpload["web_server.py /api/service-request/upload-raw"]
    end

    subgraph Core["2. Data Processing & Computation Engine"]
        Filter["data_processor.py (Filter rules)"]
        Calc["report_engine.py (Complaint Math Parity)"]
        SRCalc["service_request_engine.py (SR Math Engine)"]
        Layout["report_layout.py (Row & Area Keys)"]
    end

    subgraph Graphics["3. Graphic Rendering Layer (High-DPI)"]
        Playwright["Playwright Chromium Browser (Scale 2.5x)"]
        ReportGen["report_image_generator.py (Complaint Retina Cards)"]
        SRReportGen["service_request_engine.py (SR Retina Cards)"]
    end

    subgraph Delivery["4. Notification & Dispatch Layer"]
        WA["whatsapp_sender.py (WhatsApp Web Automation)"]
        TG["telegram_bot.py (Telegram Remote Ops Bot)"]
    end

    subgraph Persistence["5. Storage, State & Scheduling Layer"]
        DB["db_manager.py (SQLite: regions.db)"]
        Sched["scheduler_utils.py / main.py (24/7 Scheduler)"]
        Log["logger_setup.py (3-Day Rotating Logs)"]
    end

    CRM --> Filter --> Calc --> ReportGen --> WA
    CRM --> SRCalc --> SRReportGen --> WA
    RawUpload --> Calc
    SRUpload --> SRCalc
    TG --> DB
    Sched --> CRM
    ReportGen --> Log
    WA --> Log
```

---

## 2. Core Modules: Detailed Line-by-Line Wiring & Call Mapping

### `config.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`_load_region_config`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/config.py#L12-L35) | function | `L12-L35` | Load the installation-specific region configuration from JSON. | `13` callee(s) | 0 (Entrypoint) |
| [`get_adl_export_query`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/config.py#L131-L147) | function | `L131-L147` | Generates the Softcode CRMS SQL export query for ADL Broadband for a specific region. | `2` callee(s) | `3` caller(s) |
| [`get_adl_service_request_export_query`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/config.py#L166-L184) | function | `L166-L184` | Return the ADL Service Request export defined by the operations team. | `2` callee(s) | `1` caller(s) |
| [`get_adtv_export_query`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/config.py#L149-L163) | function | `L149-L163` | Generates the Softcode CRMS SQL export query for ADTv Digital TV for a specific region. | `2` callee(s) | `3` caller(s) |
| [`get_adtv_service_request_export_query`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/config.py#L187-L202) | function | `L187-L202` | Return the ADTv Service Request export defined by the operations team. | `2` callee(s) | `1` caller(s) |
| [`resolve_target_excel_path`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/config.py#L63-L105) | function | `L63-L105` | Robustly resolves a valid, existing Excel master workbook path. | `9` callee(s) | `7` caller(s) |

### `crm_downloader.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`_read_prepaid_export`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/crm_downloader.py#L398-L404) | function | `L398-L404` | Read the SMS export whether its server labels it CSV or Excel. | `4` callee(s) | `1` caller(s) |
| [`cleanup_old_download_files`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/crm_downloader.py#L43-L79) | function | `L43-L79` | Cleans up raw downloaded Excel / CSV files older than `hours` (default 24h). | `10` callee(s) | `1` caller(s) |
| [`download_from_crm`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/crm_downloader.py#L499-L575) | function | `L499-L575` | Unified entrypoint: | `10` callee(s) | `5` caller(s) |
| [`download_resolved_tickets_from_crm`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/crm_downloader.py#L578-L694) | function | `L578-L694` | Downloads fresh Resolved Tickets workbooks for Broadband (RFCRM019) | `23` callee(s) | `1` caller(s) |
| [`download_service_requests_from_crm`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/crm_downloader.py#L407-L496) | function | `L407-L496` | Download the three current Service Request sources and save one private, | `18` callee(s) | `7` caller(s) |
| [`download_via_http_session`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/crm_downloader.py#L110-L260) | function | `L110-L260` | Direct, ultra-fast headless HTTP session downloader for Softcode and Prepaid portals. | `15` callee(s) | `2` caller(s) |
| [`download_via_playwright`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/crm_downloader.py#L263-L395) | function | `L263-L395` | Playwright browser automation fallback. | `23` callee(s) | `2` caller(s) |
| [`find_latest_file`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/crm_downloader.py#L82-L87) | function | `L82-L87` | Finds the most recently modified file matching pattern in directory. | `4` callee(s) | `1` caller(s) |
| [`get_latest_local_downloads`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/crm_downloader.py#L90-L104) | function | `L90-L104` | Checks data and downloads directories for existing latest pending complaint files. | `2` callee(s) | `2` caller(s) |

### `data_processor.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`_casefold_eq`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/data_processor.py#L41-L42) | function | `L41-L42` | — | `3` callee(s) | `3` caller(s) |
| [`_casefold_in`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/data_processor.py#L60-L62) | function | `L60-L62` | — | `5` callee(s) | `1` caller(s) |
| [`_filter_configured_centers`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/data_processor.py#L65-L123) | function | `L65-L123` | Keep only source keys explicitly mapped to the selected region. | `14` callee(s) | `3` caller(s) |
| [`_find_column`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/data_processor.py#L54-L57) | function | `L54-L57` | Find a portal column despite harmless header case/space differences. | `4` callee(s) | `3` caller(s) |
| [`compute_all_sections`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/data_processor.py#L185-L189) | function | `L185-L189` | Backward-compatible wrapper: final 'Post Paid & Prepaid' tables as DataFrames. | `3` callee(s) | `1` caller(s) |
| [`compute_report_result`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/data_processor.py#L173-L182) | function | `L173-L182` | Validate inputs, then compute all three report sheets exactly like the Excel workbook. | `6` callee(s) | `1` caller(s) |
| [`ensure_region_directory_ready`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/data_processor.py#L45-L51) | function | `L45-L51` | Fail before rendering if report layout and Employee Directory disagree. | `3` callee(s) | `19` caller(s) |
| [`filter_adl`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/data_processor.py#L126-L140) | function | `L126-L140` | — | `5` callee(s) | `10` caller(s) |
| [`filter_adtv`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/data_processor.py#L143-L154) | function | `L143-L154` | — | `4` callee(s) | `11` caller(s) |
| [`filter_prepaid`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/data_processor.py#L157-L168) | function | `L157-L168` | — | `4` callee(s) | `11` caller(s) |
| [`update_excel_file`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/data_processor.py#L254-L256) | function | `L254-L256` | Deprecated name kept for compatibility - now ONLY writes a dated working copy. | `1` callee(s) | `1` caller(s) |
| [`write_working_copy`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/data_processor.py#L194-L251) | function | `L194-L251` | Copies the golden template to output/Daily Complint Tracker_<timestamp>.xls, pastes the | `33` callee(s) | `4` caller(s) |

### `db_manager.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`_normalize_pending_followup_settings`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L902-L919) | function | `L902-L919` | Validate optional WhatsApp follow-up text settings without touching reports. | `10` callee(s) | `2` caller(s) |
| [`_pending_followup_setting_key`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L898-L899) | function | `L898-L899` | — | `3` callee(s) | `2` caller(s) |
| [`add_acso`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L415-L443) | function | `L415-L443` | — | `10` callee(s) | `2` caller(s) |
| [`add_center`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L513-L531) | function | `L513-L531` | — | `9` callee(s) | `1` caller(s) |
| [`add_dispatch_rule`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L720-L740) | function | `L720-L740` | — | `9` callee(s) | `2` caller(s) |
| [`add_employee`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L644-L663) | function | `L644-L663` | — | `9` callee(s) | `2` caller(s) |
| [`add_region`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L289-L303) | function | `L289-L303` | — | `9` callee(s) | `2` caller(s) |
| [`add_schedule_time`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L811-L822) | function | `L811-L822` | — | `8` callee(s) | `1` caller(s) |
| [`add_team_leader`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L326-L351) | function | `L326-L351` | — | `10` callee(s) | `2` caller(s) |
| [`add_unified_directory_row`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L1396-L1480) | function | `L1396-L1480` | Adds a single employee directory row. | `10` callee(s) | `1` caller(s) |
| [`auto_sync_directory_from_disk`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L1678-L1764) | function | `L1678-L1764` | Automatically synchronizes Employee Directory between disk JSON and SQLite without fail. | `20` callee(s) | `4` caller(s) |
| [`bulk_delete_unified_directory`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L1597-L1639) | function | `L1597-L1639` | Bulk deletes multiple employee directory rows and keeps JSON synced. | `11` callee(s) | `1` caller(s) |
| [`delete_acso`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L490-L499) | function | `L490-L499` | — | `5` callee(s) | `1` caller(s) |
| [`delete_center`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L558-L564) | function | `L558-L564` | — | `5` callee(s) | 0 (Entrypoint) |
| [`delete_dispatch_rule`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L770-L776) | function | `L770-L776` | — | `5` callee(s) | `2` caller(s) |
| [`delete_employee`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L694-L703) | function | `L694-L703` | — | `5` callee(s) | `1` caller(s) |
| [`delete_region`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L306-L312) | function | `L306-L312` | — | `5` callee(s) | `2` caller(s) |
| [`delete_schedule_time`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L850-L856) | function | `L850-L856` | — | `5` callee(s) | `1` caller(s) |
| [`delete_team_leader`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L392-L401) | function | `L392-L401` | — | `5` callee(s) | `1` caller(s) |
| [`delete_unified_directory_row`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L1564-L1594) | function | `L1564-L1594` | Deletes an employee directory row and keeps JSON synced. | `9` callee(s) | `1` caller(s) |
| [`ensure_region_exists`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L243-L258) | function | `L243-L258` | Ensures a region exists in the database, automatically creating it if necessary. | `11` callee(s) | `7` caller(s) |
| [`export_backup`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L978-L1014) | function | `L978-L1014` | Exports full database or specific region configuration to a serializable dictionary. | `9` callee(s) | `1` caller(s) |
| [`get_acsos`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L406-L412) | function | `L406-L412` | — | `6` callee(s) | `7` caller(s) |
| [`get_all_regions`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L261-L277) | function | `L261-L277` | — | `6` callee(s) | `5` caller(s) |
| [`get_centers`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L504-L510) | function | `L504-L510` | — | `6` callee(s) | `4` caller(s) |
| [`get_connection`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L35-L40) | function | `L35-L40` | — | `5` callee(s) | `43` caller(s) |
| [`get_dispatch_rules`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L708-L717) | function | `L708-L717` | — | `6` callee(s) | `6` caller(s) |
| [`get_employees`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L569-L575) | function | `L569-L575` | — | `6` callee(s) | `3` caller(s) |
| [`get_pending_followup_settings`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L922-L929) | function | `L922-L929` | Return the selected region's WhatsApp follow-up text preferences. | `4` callee(s) | `5` caller(s) |
| [`get_region_by_id`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L280-L286) | function | `L280-L286` | — | `6` callee(s) | `10` caller(s) |
| [`get_schedule_times`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L790-L808) | function | `L790-L808` | — | `8` callee(s) | `2` caller(s) |
| [`get_setting`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L880-L886) | function | `L880-L886` | — | `6` callee(s) | `8` caller(s) |
| [`get_team_leaders`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L317-L323) | function | `L317-L323` | — | `6` callee(s) | `4` caller(s) |
| [`get_telegram_alert_recipients`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L939-L956) | function | `L939-L956` | Returns all configured or recorded Telegram chat IDs for alert broadcasts. | `8` callee(s) | `2` caller(s) |
| [`get_unified_directory`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L1106-L1184) | function | `L1106-L1184` | Returns employee directory in unified format with Position matching user template. | `10` callee(s) | `3` caller(s) |
| [`import_unified_directory`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L1187-L1393) | function | `L1187-L1393` | Imports complete employee directory for a region from uploaded template data. | `16` callee(s) | `5` caller(s) |
| [`init_db`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L43-L238) | function | `L43-L238` | Initializes schema and ensures the configured default region exists. | `8` callee(s) | `1` caller(s) |
| [`load_directory_from_json`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L1659-L1675) | function | `L1659-L1675` | Imports and synchronizes the employee directory for a region from a standalone JSON file. | `11` callee(s) | 0 (Entrypoint) |
| [`load_sample_preset`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L1095-L1101) | function | `L1095-L1101` | Loads a sample configuration preset into the specified region. | `3` callee(s) | 0 (Entrypoint) |
| [`register_telegram_alert_recipient`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L959-L969) | function | `L959-L969` | Registers a chat ID as an authorized alert recipient. | `10` callee(s) | `2` caller(s) |
| [`restore_backup`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L1017-L1082) | function | `L1017-L1082` | Restores database tables from a backup dictionary. | `12` callee(s) | `3` caller(s) |
| [`restore_from_file`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L1085-L1092) | function | `L1085-L1092` | Reads a JSON backup file and restores it into the database. | `7` callee(s) | `1` caller(s) |
| [`set_pending_followup_settings`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L932-L936) | function | `L932-L936` | Persist validated WhatsApp follow-up text preferences for one region. | `4` callee(s) | `2` caller(s) |
| [`set_setting`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L889-L895) | function | `L889-L895` | — | `6` callee(s) | `9` caller(s) |
| [`sync_directory_to_json`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L1642-L1656) | function | `L1642-L1656` | Saves the entire Employee Directory for a region into a standalone, human-readable JSON file. | `9` callee(s) | `8` caller(s) |
| [`toggle_dispatch_rule`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L779-L785) | function | `L779-L785` | — | `5` callee(s) | `1` caller(s) |
| [`toggle_schedule_time`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L859-L865) | function | `L859-L865` | — | `5` callee(s) | `1` caller(s) |
| [`update_acso`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L446-L487) | function | `L446-L487` | — | `9` callee(s) | `2` caller(s) |
| [`update_center`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L534-L555) | function | `L534-L555` | — | `8` callee(s) | 0 (Entrypoint) |
| [`update_dispatch_rule`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L743-L767) | function | `L743-L767` | — | `9` callee(s) | `1` caller(s) |
| [`update_employee`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L666-L691) | function | `L666-L691` | — | `8` callee(s) | `1` caller(s) |
| [`update_last_run`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L868-L875) | function | `L868-L875` | — | `7` callee(s) | 0 (Entrypoint) |
| [`update_schedule_time`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L825-L847) | function | `L825-L847` | — | `6` callee(s) | `1` caller(s) |
| [`update_team_leader`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L354-L389) | function | `L354-L389` | — | `9` callee(s) | `2` caller(s) |
| [`update_unified_directory_row`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L1483-L1560) | function | `L1483-L1560` | Updates an existing employee directory row (TL or ACSO). | `11` callee(s) | `1` caller(s) |
| [`validate_region_report_directory`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/db_manager.py#L578-L641) | function | `L578-L641` | Return actionable layout issues before a region report is generated. | `10` callee(s) | `7` caller(s) |

### `generate_wiring_docs.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`CodeSymbol`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L45-L62) | class | `L45-L62` | — | 0 | `2` caller(s) |
| [`CodeSymbol.__init__`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L46-L58) | method | `L46-L58` | — | `1` callee(s) | 0 (Entrypoint) |
| [`CodeSymbol.qualified_name`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L61-L62) | method | `L61-L62` | — | 0 | 0 (Entrypoint) |
| [`CodebaseAnalyzer`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L65-L266) | class | `L65-L266` | — | 0 | `1` caller(s) |
| [`CodebaseAnalyzer.__init__`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L66-L71) | method | `L66-L71` | — | `2` callee(s) | 0 (Entrypoint) |
| [`CodebaseAnalyzer._collect_python_files`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L73-L80) | method | `L73-L80` | — | `7` callee(s) | 0 (Entrypoint) |
| [`CodebaseAnalyzer._parse_file_pass1`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L100-L133) | method | `L100-L133` | — | `7` callee(s) | 0 (Entrypoint) |
| [`CodebaseAnalyzer._parse_file_pass2`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L158-L233) | method | `L158-L233` | — | `16` callee(s) | 0 (Entrypoint) |
| [`CodebaseAnalyzer._record_func`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L135-L156) | method | `L135-L156` | — | `5` callee(s) | 0 (Entrypoint) |
| [`CodebaseAnalyzer._resolve_callee`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L235-L246) | method | `L235-L246` | — | `2` callee(s) | 0 (Entrypoint) |
| [`CodebaseAnalyzer.analyze`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L82-L98) | method | `L82-L98` | — | `5` callee(s) | 0 (Entrypoint) |
| [`CodebaseAnalyzer.compute_blast_radius`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L248-L266) | method | `L248-L266` | Calculates upstream dependents (who is affected if this symbol changes). | `5` callee(s) | 0 (Entrypoint) |
| [`generate_markdown`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L269-L456) | function | `L269-L456` | — | `17` callee(s) | `1` caller(s) |
| [`install_git_hook`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L459-L472) | function | `L459-L472` | — | `3` callee(s) | `1` caller(s) |
| [`main`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/generate_wiring_docs.py#L475-L494) | function | `L475-L494` | — | `7` callee(s) | 0 (Entrypoint) |

### `logger_setup.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`DualLogStream`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/logger_setup.py#L84-L152) | class | `L84-L152` | Stream interceptor that writes output to original console stream | 0 | `1` caller(s) |
| [`DualLogStream.__init__`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/logger_setup.py#L89-L92) | method | `L89-L92` | — | 0 | 0 (Entrypoint) |
| [`DualLogStream.flush`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/logger_setup.py#L148-L152) | method | `L148-L152` | — | `1` callee(s) | 0 (Entrypoint) |
| [`DualLogStream.write`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/logger_setup.py#L94-L146) | method | `L94-L146` | — | `13` callee(s) | 0 (Entrypoint) |
| [`analyze_system_logs`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/logger_setup.py#L267-L403) | function | `L267-L403` | Scans running and error log files for the last N days (default 3), | `23` callee(s) | `1` caller(s) |
| [`cleanup_old_logs`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/logger_setup.py#L38-L81) | function | `L38-L81` | Scans LOGS_DIR and deletes log files older than retention_days (default 3 days). | `13` callee(s) | `4` caller(s) |
| [`get_log_files`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/logger_setup.py#L200-L219) | function | `L200-L219` | Returns list of all available log files in logs/ folder with metadata. | `11` callee(s) | `1` caller(s) |
| [`get_today_log_path`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/logger_setup.py#L31-L35) | function | `L31-L35` | Returns the Path for today's running or error log file. | `2` callee(s) | `3` caller(s) |
| [`init_logging`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/logger_setup.py#L155-L197) | function | `L155-L197` | Initializes central logging system: | `13` callee(s) | 0 (Entrypoint) |
| [`read_log_file`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/logger_setup.py#L222-L264) | function | `L222-L264` | Reads the most recent lines of a specified log file or today's default log file. | `10` callee(s) | `1` caller(s) |

### `login_whatsapp.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`log`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/login_whatsapp.py#L22-L23) | function | `L22-L23` | — | `1` callee(s) | 0 (Entrypoint) |

### `main.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`execute_cycle`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/main.py#L44-L128) | function | `L44-L128` | Executes the complete operational pipeline. | `21` callee(s) | `2` caller(s) |
| [`main`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/main.py#L159-L192) | function | `L159-L192` | — | `8` callee(s) | 0 (Entrypoint) |
| [`run_scheduler_loop`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/main.py#L131-L156) | function | `L131-L156` | Runs a 24/7 background scheduler monitoring 8:00 AM and 3:00 PM triggers. | `8` callee(s) | `1` caller(s) |

### `render_retina_test.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`build_table_data`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/render_retina_test.py#L11-L35) | function | `L11-L35` | — | `6` callee(s) | 0 (Entrypoint) |
| [`render_html`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/render_retina_test.py#L37-L168) | function | `L37-L168` | — | `6` callee(s) | 0 (Entrypoint) |

### `render_ultra_hd.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`make_html`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/render_ultra_hd.py#L42-L166) | function | `L42-L166` | — | `3` callee(s) | 0 (Entrypoint) |

### `report_engine.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`ReportResult`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L140-L143) | class | `L140-L143` | — | `1` callee(s) | `1` caller(s) |
| [`ReportRow`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L116-L125) | class | `L116-L125` | — | 0 | `5` caller(s) |
| [`ReportRow.as_dict`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L122-L125) | method | `L122-L125` | — | `3` callee(s) | 0 (Entrypoint) |
| [`Table`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L129-L136) | class | `L129-L136` | — | 0 | `3` caller(s) |
| [`Table.to_frame`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L134-L136) | method | `L134-L136` | — | `2` callee(s) | 0 (Entrypoint) |
| [`_add`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L279-L281) | function | `L279-L281` | — | `2` callee(s) | `1` caller(s) |
| [`_alphabetical_rows`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L284-L289) | function | `L284-L289` | Display all report centers A-Z, with staff names as a stable tie-breaker. | `4` callee(s) | `2` caller(s) |
| [`_column`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L260-L268) | function | `L260-L268` | Get a column by its row-1 header (case/space-insensitive header lookup). | `6` callee(s) | `3` caller(s) |
| [`_is_blank`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L43-L44) | function | `L43-L44` | — | `2` callee(s) | `4` caller(s) |
| [`_postpaid_row`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L295-L300) | function | `L295-L300` | — | `2` callee(s) | `1` caller(s) |
| [`_prepaid_row`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L337-L342) | function | `L337-L342` | — | `2` callee(s) | `1` caller(s) |
| [`_share`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L440-L442) | function | `L440-L442` | — | `4` callee(s) | `1` caller(s) |
| [`_sum_rows`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L271-L276) | function | `L271-L276` | — | `4` callee(s) | `2` caller(s) |
| [`_to_number`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L47-L56) | function | `L47-L56` | Numeric value of a cell, or None. Text that looks like a number counts (as COUNTIF does). | `5` callee(s) | `2` caller(s) |
| [`_wildcard_regex`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L59-L68) | function | `L59-L68` | Excel wildcards: * any run, ? one char, ~ escapes. Case-insensitive, whole-cell match. | `5` callee(s) | `1` caller(s) |
| [`build_pending_followup_message`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L167-L244) | function | `L167-L244` | Build the optional WhatsApp complaint follow-up after report images. | `22` callee(s) | `4` caller(s) |
| [`build_pending_followup_messages`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L247-L254) | function | `L247-L254` | Build one optional WhatsApp text per complaint image, in image order. | `2` callee(s) | `4` caller(s) |
| [`complaint_followup_section_keys`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L146-L164) | function | `L146-L164` | Return complaint sections in the same order as their report images. | `3` callee(s) | `2` caller(s) |
| [`compute_pending_days`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L303-L331) | function | `L303-L331` | — | `5` callee(s) | `1` caller(s) |
| [`compute_prepaid_pending`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L345-L372) | function | `L345-L372` | — | `5` callee(s) | `1` caller(s) |
| [`compute_report`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L378-L414) | function | `L378-L414` | — | `10` callee(s) | `9` caller(s) |
| [`countifs`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L104-L109) | function | `L104-L109` | countifs(col1, crit1, col2, crit2, ...) over equal-length python lists. | `7` callee(s) | `2` caller(s) |
| [`load_inputs_from_workbook`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L420-L434) | function | `L420-L434` | Read 'ADL P', 'ADTv P', 'Prepaid' exactly as stored (no stripping, no type coercion). | `6` callee(s) | `6` caller(s) |
| [`make_matcher`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L71-L101) | function | `L71-L101` | Return f(cell)->bool that behaves like one COUNTIFS criterion. | `11` callee(s) | `1` caller(s) |
| [`validate_inputs`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_engine.py#L445-L483) | function | `L445-L483` | Return human-readable warnings. Empty list = inputs look correctly aligned. | `9` callee(s) | `2` caller(s) |

### `report_image_generator.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`extract_acso_table_data_from_dataframe`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_image_generator.py#L304-L336) | function | `L304-L336` | Extracts ACSO table data and Grand Total row directly from computed DataFrame. | `14` callee(s) | `1` caller(s) |
| [`extract_acso_table_data_from_excel`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_image_generator.py#L339-L377) | function | `L339-L377` | Extracts ACSO table data from Excel workbook sheet 'Post Paid & Prepaid' (Rows 33-45 plus Row 46 Grand Total). | `13` callee(s) | `1` caller(s) |
| [`extract_table_data_from_dataframe`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_image_generator.py#L24-L47) | function | `L24-L47` | Extracts table data directly from computed DataFrame without requiring Excel file read. | `10` callee(s) | `1` caller(s) |
| [`extract_table_data_from_excel`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_image_generator.py#L50-L83) | function | `L50-L83` | Extracts table data from Excel workbook and dynamically detects active pending day columns. | `13` callee(s) | `1` caller(s) |
| [`generate_acso_report_images`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_image_generator.py#L592-L652) | function | `L592-L652` | Renders high-definition Retina ACSO report images (1600px+ width) using Playwright. | `16` callee(s) | `8` caller(s) |
| [`generate_acso_table_html`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_image_generator.py#L380-L589) | function | `L380-L589` | Generates pixel-perfect HTML table for ACSO report including the bottom Grand Total row. | `7` callee(s) | `1` caller(s) |
| [`generate_all_report_images`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_image_generator.py#L655-L659) | function | `L655-L659` | Generates both Team Leader and ACSO report images. | `2` callee(s) | 0 (Entrypoint) |
| [`generate_report_images`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_image_generator.py#L230-L301) | function | `L230-L301` | Renders high-definition Retina report images (1600px+ width) using Playwright. | `20` callee(s) | `8` caller(s) |
| [`generate_table_html`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_image_generator.py#L86-L227) | function | `L86-L227` | Generates pixel-perfect HTML table styled exactly like the user's manual report. | `7` callee(s) | `1` caller(s) |

### `report_layout.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`AcsoRow`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_layout.py#L60-L73) | class | `L60-L73` | One ACSO / Center row. Intermediate sheets rows 33-45 -> final sheet rows 34-46. | `1` callee(s) | `1` caller(s) |
| [`TeamLeaderRow`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_layout.py#L44-L56) | class | `L44-L56` | One Team Leader row (Excel rows 4-26 in all three report sheets). | `1` callee(s) | `1` caller(s) |
| [`get_layout_for_region`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/report_layout.py#L84-L125) | function | `L84-L125` | Loads the selected region's layout from SQLite without cross-region fallback. | `9` callee(s) | `7` caller(s) |

### `run_latest_cycle.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`run`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/run_latest_cycle.py#L37-L135) | function | `L37-L135` | — | `22` callee(s) | `3` caller(s) |

### `scheduler_utils.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`schedule_slot_is_due`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/scheduler_utils.py#L6-L23) | function | `L6-L23` | Return whether an enabled schedule should run now, including a safe late-start window. | `8` callee(s) | `2` caller(s) |

### `service_request_engine.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`_get_excel_column_name`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L534-L540) | function | `L534-L540` | — | `2` callee(s) | `1` caller(s) |
| [`_safe_region_id`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L235-L240) | function | `L235-L240` | Validate a region ID before using it in an on-disk path. | `5` callee(s) | `3` caller(s) |
| [`build_pending_report`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L202-L230) | function | `L202-L230` | Builds pivot table grouped by CENTER and Service Request Type. | `8` callee(s) | `2` caller(s) |
| [`calculate_sr_pending_reports`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L513-L523) | function | `L513-L523` | Convenience wrapper returning computed records dictionary. | `2` callee(s) | `1` caller(s) |
| [`compute_service_request_reports`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L288-L510) | function | `L288-L510` | Reads the raw Excel workbook (ADL Postpaid, ADTv, Prepaid) and returns | `30` callee(s) | `18` caller(s) |
| [`create_excel_output`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L543-L764) | function | `L543-L764` | Renders styled Excel workbook matching the exact Streamlit xlsxwriter logic. | `17` callee(s) | `3` caller(s) |
| [`execute_automated_sr_cycle`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L1048-L1160) | function | `L1048-L1160` | Complete end-to-end automated cycle for Service Requests: | `26` callee(s) | `2` caller(s) |
| [`filter_prepaid_service_request_source`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L123-L149) | function | `L123-L149` | Keep only the two operations-approved Prepaid SR complaint values. | `8` callee(s) | `3` caller(s) |
| [`find_service_request_raw_file`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L250-L280) | function | `L250-L280` | Find a Service Request workbook only for the selected region. | `11` callee(s) | `1` caller(s) |
| [`generate_sr_excel_report`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L526-L529) | function | `L526-L529` | Convenience wrapper computing and generating the formatted Excel workbook. | `2` callee(s) | 0 (Entrypoint) |
| [`generate_sr_table_html`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L769-L975) | function | `L769-L975` | Generates pixel-perfect HTML table for Playwright Retina snapshot rendering. | `5` callee(s) | `1` caller(s) |
| [`is_excluded_service`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L152-L165) | function | `L152-L165` | Returns True if the ticket should be excluded from report generation. | `4` callee(s) | `1` caller(s) |
| [`is_sr_report_type`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L71-L81) | function | `L71-L81` | Returns True if the given report type string is any variant of Service Request reports. | `5` callee(s) | `6` caller(s) |
| [`normalize_service`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L107-L120) | function | `L107-L120` | Standardizes disparate CRM complaint and problem text into uniform categories. | `4` callee(s) | 0 (Entrypoint) |
| [`pending_bucket`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L87-L104) | function | `L87-L104` | Classifies elapsed days into institutional pending buckets. | `3` callee(s) | 0 (Entrypoint) |
| [`prepare_source`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L168-L199) | function | `L168-L199` | Prepares and cleans raw CRM tickets for pivoting. | `8` callee(s) | `2` caller(s) |
| [`render_sr_report_images`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L978-L1043) | function | `L978-L1043` | Renders high-definition Retina report images (1600px+ width) using Playwright. | `19` callee(s) | `8` caller(s) |
| [`sr_output_path`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L283-L285) | function | `L283-L285` | Keep output isolated by validated region ID, including for concurrent regions. | `1` callee(s) | `7` caller(s) |
| [`sr_raw_path`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/service_request_engine.py#L243-L247) | function | `L243-L247` | Return the private, region-isolated Service Request workbook path. | `2` callee(s) | `4` caller(s) |

### `tat_engine.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`calculate_tat_metric`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/tat_engine.py#L59-L68) | function | `L59-L68` | Calculates whole-number (standard rounded) 4-hour and 1-day TAT percentages. | `4` callee(s) | `2` caller(s) |
| [`compute_tat_reports`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/tat_engine.py#L71-L219) | function | `L71-L219` | Computes all 4 TAT reports for the target region and date window. | `20` callee(s) | `2` caller(s) |
| [`dispatch_tat_reports`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/tat_engine.py#L589-L622) | function | `L589-L622` | Renders and dispatches TAT report cards via WhatsApp to specified recipients. | `4` callee(s) | `2` caller(s) |
| [`execute_tat_pipeline`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/tat_engine.py#L530-L586) | function | `L530-L586` | Full automated execution pipeline for TAT reports: | `13` callee(s) | `11` caller(s) |
| [`export_tat_excel`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/tat_engine.py#L386-L478) | function | `L386-L478` | Exports all 4 TAT reports into a beautifully styled multi-tab Excel workbook matching sample styles. | `14` callee(s) | `2` caller(s) |
| [`generate_tat_html`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/tat_engine.py#L222-L344) | function | `L222-L344` | Generates pixel-perfect HTML table styled exactly like the user's Excel sample: | `5` callee(s) | `2` caller(s) |
| [`get_latest_resolved_files`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/tat_engine.py#L481-L527) | function | `L481-L527` | Finds the latest Broadband and DTv resolved ticket workbooks from data/ and Downloads/. | `14` callee(s) | `2` caller(s) |
| [`render_tat_report_images`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/tat_engine.py#L347-L383) | function | `L347-L383` | Renders high-DPI images for all 4 TAT reports via Playwright. | `11` callee(s) | `1` caller(s) |

### `telegram_bot.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`TelegramAPI`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L87-L238) | class | `L87-L238` | — | 0 | `3` caller(s) |
| [`TelegramAPI.__init__`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L88-L90) | method | `L88-L90` | — | `1` callee(s) | 0 (Entrypoint) |
| [`TelegramAPI.answer_callback_query`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L164-L180) | method | `L164-L180` | — | `4` callee(s) | 0 (Entrypoint) |
| [`TelegramAPI.delete_message`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L147-L162) | method | `L147-L162` | — | `4` callee(s) | 0 (Entrypoint) |
| [`TelegramAPI.download_file`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L214-L224) | method | `L214-L224` | — | `4` callee(s) | 0 (Entrypoint) |
| [`TelegramAPI.edit_message_text`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L122-L145) | method | `L122-L145` | — | `4` callee(s) | 0 (Entrypoint) |
| [`TelegramAPI.get_file`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L205-L212) | method | `L205-L212` | — | `4` callee(s) | 0 (Entrypoint) |
| [`TelegramAPI.get_me`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L95-L97) | method | `L95-L97` | — | `2` callee(s) | 0 (Entrypoint) |
| [`TelegramAPI.get_updates`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L226-L238) | method | `L226-L238` | — | `3` callee(s) | 0 (Entrypoint) |
| [`TelegramAPI.is_configured`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L92-L93) | method | `L92-L93` | — | `2` callee(s) | 0 (Entrypoint) |
| [`TelegramAPI.send_message`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L99-L120) | method | `L99-L120` | — | `4` callee(s) | 0 (Entrypoint) |
| [`TelegramAPI.send_photo`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L182-L203) | method | `L182-L203` | — | `7` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L874-L1876) | class | `L874-L1876` | — | 0 | `1` caller(s) |
| [`TelegramBotRunner.__init__`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L875-L878) | method | `L875-L878` | — | 0 | 0 (Entrypoint) |
| [`TelegramBotRunner.execute_complaint_group_dispatch_async`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1611-L1641) | method | `L1611-L1641` | — | `6` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.execute_group_dispatch_async`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1860-L1861) | method | `L1860-L1861` | — | `1` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.execute_send_telegram_reports_async`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1815-L1857) | method | `L1815-L1857` | — | `8` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.execute_sr_dispatch_async`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1869-L1870) | method | `L1869-L1870` | — | `1` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.execute_sr_group_dispatch_async`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1643-L1673) | method | `L1643-L1673` | — | `6` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.execute_sr_test_delivery_async`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1872-L1873) | method | `L1872-L1873` | — | `1` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.execute_tat_group_dispatch_async`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1747-L1777) | method | `L1747-L1777` | — | `6` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.execute_test_complaint_async`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1675-L1709) | method | `L1675-L1709` | — | `11` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.execute_test_delivery_async`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1863-L1864) | method | `L1863-L1864` | — | `1` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.execute_test_sr_async`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1711-L1745) | method | `L1711-L1745` | — | `11` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.execute_test_tat_async`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1779-L1813) | method | `L1779-L1813` | — | `11` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.handle_callback`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1218-L1577) | method | `L1218-L1577` | — | `31` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.handle_document`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L958-L1024) | method | `L958-L1024` | — | `8` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.handle_message`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1026-L1191) | method | `L1026-L1191` | — | `12` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.handle_service_action`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1581-L1609) | method | `L1581-L1609` | — | `11` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.process_update`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L912-L956) | method | `L912-L956` | — | `8` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.send_control_menu`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1201-L1208) | method | `L1201-L1208` | — | `5` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.send_main_menu`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1193-L1199) | method | `L1193-L1199` | — | `4` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.send_render_send_menu`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1210-L1216) | method | `L1210-L1216` | — | `4` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.send_report_photos_async`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1866-L1867) | method | `L1866-L1867` | — | `1` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.send_sr_report_photos_async`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1875-L1876) | method | `L1875-L1876` | — | `1` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.start`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L880-L907) | method | `L880-L907` | — | `7` callee(s) | 0 (Entrypoint) |
| [`TelegramBotRunner.stop`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L909-L910) | method | `L909-L910` | — | 0 | 0 (Entrypoint) |
| [`_exec_service_command`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L308-L341) | function | `L308-L341` | — | `5` callee(s) | `4` caller(s) |
| [`_service_unit_name`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L76-L78) | function | `L76-L78` | Return the explicit unit name required by the restricted sudoers rule. | `1` callee(s) | `3` caller(s) |
| [`_web_api_headers`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L81-L82) | function | `L81-L82` | — | 0 | `7` caller(s) |
| [`add_preconfigured_test_number`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L502-L509) | function | `L502-L509` | Adds a test number to persistent list. | `4` callee(s) | `2` caller(s) |
| [`broadcast_telegram_alert`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L835-L869) | function | `L835-L869` | Broadcasts a high-priority system alert to all authorized Telegram chat IDs. | `5` callee(s) | `4` caller(s) |
| [`format_automated_error_alert`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L757-L814) | function | `L757-L814` | Formats an urgent Telegram error notification with diagnostics and actionable recovery steps. | `9` callee(s) | `4` caller(s) |
| [`format_control_menu_message`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L710-L711) | function | `L710-L711` | — | `1` callee(s) | `3` caller(s) |
| [`format_main_menu_message`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L688-L689) | function | `L688-L689` | — | 0 | `1` caller(s) |
| [`format_render_send_menu_message`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L714-L726) | function | `L714-L726` | — | 0 | `2` caller(s) |
| [`format_status_message`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L692-L707) | function | `L692-L707` | — | `1` callee(s) | `2` caller(s) |
| [`format_test_numbers_manager_message`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L729-L738) | function | `L729-L738` | — | `1` callee(s) | `1` caller(s) |
| [`get_alert_retry_keyboard`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L817-L832) | function | `L817-L832` | Generates quick retry buttons for automated error alerts. | `2` callee(s) | `4` caller(s) |
| [`get_confirmation_keyboard`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L663-L672) | function | `L663-L672` | Standard Confirm & Cancel confirmation modal keyboard. | 0 | `3` caller(s) |
| [`get_control_menu_keyboard`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L557-L578) | function | `L557-L578` | Sub Menu: Control Buttons | 0 | `4` caller(s) |
| [`get_main_menu_keyboard`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L535-L554) | function | `L535-L554` | Main Menu: | 0 | `2` caller(s) |
| [`get_phone_selection_keyboard`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L680-L683) | function | `L680-L683` | Legacy helper maintained for backward compatibility. | `1` callee(s) | 0 (Entrypoint) |
| [`get_preconfigured_test_numbers`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L469-L489) | function | `L469-L489` | Retrieves list of preconfigured test numbers from persistent SQLite settings. | `7` callee(s) | `11` caller(s) |
| [`get_remove_test_numbers_keyboard`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L653-L660) | function | `L653-L660` | Keyboard listing test numbers to delete. | `2` callee(s) | `1` caller(s) |
| [`get_render_send_menu_keyboard`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L581-L624) | function | `L581-L624` | Sub Menu: Render and Send | 0 | `12` caller(s) |
| [`get_service_status`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L257-L305) | function | `L257-L305` | Queries systemd service state and checks web scheduler settings. | `7` callee(s) | `6` caller(s) |
| [`get_sr_menu_keyboard`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L675-L677) | function | `L675-L677` | Legacy helper maintained for backward compatibility. | `1` callee(s) | `1` caller(s) |
| [`get_test_numbers_manager_keyboard`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L640-L650) | function | `L640-L650` | Keyboard for managing preconfigured test numbers. | `2` callee(s) | `1` caller(s) |
| [`get_test_selection_keyboard`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L627-L637) | function | `L627-L637` | Displays selection of preconfigured test numbers or enter custom number. | `3` callee(s) | `3` caller(s) |
| [`is_user_authorized`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L743-L752) | function | `L743-L752` | — | `2` callee(s) | `2` caller(s) |
| [`main`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L1881-L1914) | function | `L1881-L1914` | — | `14` callee(s) | 0 (Entrypoint) |
| [`remove_preconfigured_test_number`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L512-L519) | function | `L512-L519` | Removes a test number from persistent list. | `4` callee(s) | `2` caller(s) |
| [`reset_preconfigured_test_numbers`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L522-L530) | function | `L522-L530` | Resets test numbers back to system defaults. | `3` callee(s) | `1` caller(s) |
| [`restart_system_service`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L352-L353) | function | `L352-L353` | — | `1` callee(s) | `1` caller(s) |
| [`run_shell_command`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L243-L254) | function | `L243-L254` | — | `3` callee(s) | `2` caller(s) |
| [`set_preconfigured_test_numbers`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L492-L499) | function | `L492-L499` | Saves list of test numbers to SQLite system_settings. | `5` callee(s) | `3` caller(s) |
| [`start_system_service`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L344-L345) | function | `L344-L345` | — | `1` callee(s) | `1` caller(s) |
| [`stop_system_service`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L348-L349) | function | `L348-L349` | — | `1` callee(s) | `1` caller(s) |
| [`trigger_group_dispatch`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L358-L373) | function | `L358-L373` | Calls web server endpoint to run automated Complaint cycle and dispatch to groups. | `4` callee(s) | `2` caller(s) |
| [`trigger_sr_dispatch`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L394-L409) | function | `L394-L409` | Calls web server endpoint to run automated Service Request cycle and dispatch. | `4` callee(s) | `2` caller(s) |
| [`trigger_sr_test_delivery`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L412-L427) | function | `L412-L427` | Generates Service Request reports and delivers them to a specific phone number. | `5` callee(s) | `1` caller(s) |
| [`trigger_tat_dispatch`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L430-L445) | function | `L430-L445` | Calls web server endpoint to run automated Turnaround Time (TAT) cycle and dispatch. | `4` callee(s) | `3` caller(s) |
| [`trigger_tat_test_delivery`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L448-L463) | function | `L448-L463` | Generates Turnaround Time (TAT) reports and delivers them to a specific phone number. | `5` callee(s) | `2` caller(s) |
| [`trigger_test_delivery`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/telegram_bot.py#L376-L391) | function | `L376-L391` | Generates High-DPI reports and delivers them to a specific phone number. | `5` callee(s) | `1` caller(s) |

### `test_center_display_name.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`CenterDisplayNameTests`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_center_display_name.py#L9-L40) | class | `L9-L40` | — | 0 | 0 (Entrypoint) |
| [`CenterDisplayNameTests.test_display_name_is_used_for_both_platform_report_centers`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_center_display_name.py#L10-L40) | method | `L10-L40` | — | `3` callee(s) | 0 (Entrypoint) |

### `test_center_isolation.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`ComplaintCenterIsolationTests`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_center_isolation.py#L10-L95) | class | `L10-L95` | — | 0 | 0 (Entrypoint) |
| [`ComplaintCenterIsolationTests.setUp`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_center_isolation.py#L11-L17) | method | `L11-L17` | — | 0 | 0 (Entrypoint) |
| [`ComplaintCenterIsolationTests.test_complaint_filters_are_exact_with_portal_style_headers`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_center_isolation.py#L46-L66) | method | `L46-L66` | — | `7` callee(s) | 0 (Entrypoint) |
| [`ComplaintCenterIsolationTests.test_report_specific_acso_keys_are_accepted_before_filtering`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_center_isolation.py#L70-L95) | method | `L70-L95` | — | `6` callee(s) | 0 (Entrypoint) |
| [`ComplaintCenterIsolationTests.test_similar_center_names_remain_region_isolated`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_center_isolation.py#L21-L42) | method | `L21-L42` | — | `7` callee(s) | 0 (Entrypoint) |

### `test_compact_retina.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`make_compact_html`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_compact_retina.py#L36-L164) | function | `L36-L164` | — | `3` callee(s) | 0 (Entrypoint) |

### `test_directory_preflight.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`DirectoryPreflightTests`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_directory_preflight.py#L8-L109) | class | `L8-L109` | — | 0 | 0 (Entrypoint) |
| [`DirectoryPreflightTests.setUp`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_directory_preflight.py#L9-L32) | method | `L9-L32` | — | 0 | 0 (Entrypoint) |
| [`DirectoryPreflightTests.test_center_reports_use_center_not_acso_personnel_fields`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_directory_preflight.py#L74-L79) | method | `L74-L79` | — | `3` callee(s) | 0 (Entrypoint) |
| [`DirectoryPreflightTests.test_custom_display_name_does_not_replace_postpaid_crm_name`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_directory_preflight.py#L97-L109) | method | `L97-L109` | — | `3` callee(s) | 0 (Entrypoint) |
| [`DirectoryPreflightTests.test_matching_directory_passes`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_directory_preflight.py#L38-L43) | method | `L38-L43` | — | `3` callee(s) | 0 (Entrypoint) |
| [`DirectoryPreflightTests.test_missing_crm_lookup_key_is_reported`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_directory_preflight.py#L61-L68) | method | `L61-L68` | — | `4` callee(s) | 0 (Entrypoint) |
| [`DirectoryPreflightTests.test_prepaid_code_not_in_directory_is_reported`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_directory_preflight.py#L49-L55) | method | `L49-L55` | — | `4` callee(s) | 0 (Entrypoint) |
| [`DirectoryPreflightTests.test_unlisted_report_center_is_reported`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_directory_preflight.py#L85-L91) | method | `L85-L91` | — | `4` callee(s) | 0 (Entrypoint) |

### `test_logger_lock_safety.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`LoggerLockSafetyTests`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_logger_lock_safety.py#L9-L38) | class | `L9-L38` | — | 0 | 0 (Entrypoint) |
| [`LoggerLockSafetyTests.test_retention_cleanup_completes_with_stdout_intercepted`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_logger_lock_safety.py#L10-L38) | method | `L10-L38` | Retention must not re-enter LOG_LOCK through DualLogStream.print(). | `4` callee(s) | 0 (Entrypoint) |

### `test_pairing_code.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`log`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_pairing_code.py#L14-L15) | function | `L14-L15` | — | `1` callee(s) | 0 (Entrypoint) |

### `test_pending_followup.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`PendingFollowupTests`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_pending_followup.py#L11-L91) | class | `L11-L91` | — | 0 | 0 (Entrypoint) |
| [`PendingFollowupTests.test_adl_two_day_text_can_be_enabled_independently_of_adtv`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_pending_followup.py#L44-L66) | method | `L44-L66` | — | `4` callee(s) | 0 (Entrypoint) |
| [`PendingFollowupTests.test_lists_only_three_day_and_older_tl_buckets`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_pending_followup.py#L12-L29) | method | `L12-L29` | — | `4` callee(s) | 0 (Entrypoint) |
| [`PendingFollowupTests.test_messages_are_built_in_the_same_order_as_complaint_images`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_pending_followup.py#L68-L84) | method | `L68-L84` | — | `5` callee(s) | 0 (Entrypoint) |
| [`PendingFollowupTests.test_schedule_catches_up_after_short_restart_but_not_old_slots`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_pending_followup.py#L86-L91) | method | `L86-L91` | — | `4` callee(s) | 0 (Entrypoint) |
| [`PendingFollowupTests.test_uses_only_the_dispatched_card_style`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_pending_followup.py#L31-L42) | method | `L31-L42` | — | `5` callee(s) | 0 (Entrypoint) |

### `test_pending_followup_settings.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`PendingFollowupSettingsTests`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_pending_followup_settings.py#L9-L34) | class | `L9-L34` | — | 0 | 0 (Entrypoint) |
| [`PendingFollowupSettingsTests.test_defaults_are_adl_two_days_and_adtv_three_days`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_pending_followup_settings.py#L10-L17) | method | `L10-L17` | — | `4` callee(s) | 0 (Entrypoint) |
| [`PendingFollowupSettingsTests.test_settings_are_normalized_and_stored_per_region`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_pending_followup_settings.py#L19-L34) | method | `L19-L34` | — | `5` callee(s) | 0 (Entrypoint) |

### `test_region_json_config.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`RegionJsonConfigTests`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_region_json_config.py#L11-L36) | class | `L11-L36` | — | 0 | 0 (Entrypoint) |
| [`RegionJsonConfigTests.test_json_overrides_conflicting_legacy_environment_values`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_region_json_config.py#L12-L36) | method | `L12-L36` | — | `10` callee(s) | 0 (Entrypoint) |

### `test_region_startup.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`RegionStartupTests`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_region_startup.py#L11-L40) | class | `L11-L40` | — | 0 | 0 (Entrypoint) |
| [`RegionStartupTests.test_deleted_thrissur_stays_deleted_after_restart_and_sync`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_region_startup.py#L12-L40) | method | `L12-L40` | — | `20` callee(s) | 0 (Entrypoint) |

### `test_report_sorting.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`ReportSortingTests`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_report_sorting.py#L7-L24) | class | `L7-L24` | — | 0 | 0 (Entrypoint) |
| [`ReportSortingTests.test_centers_sort_case_insensitively_then_by_staff_name`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_report_sorting.py#L8-L24) | method | `L8-L24` | — | `3` callee(s) | 0 (Entrypoint) |

### `test_scheduler_lifecycle.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`SchedulerLifecycleTests`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_scheduler_lifecycle.py#L7-L56) | class | `L7-L56` | — | 0 | 0 (Entrypoint) |
| [`SchedulerLifecycleTests.setUpClass`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_scheduler_lifecycle.py#L9-L11) | method | `L9-L11` | — | `4` callee(s) | 0 (Entrypoint) |
| [`SchedulerLifecycleTests.test_due_slot_tasks_are_retained_until_completion`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_scheduler_lifecycle.py#L41-L44) | method | `L41-L44` | — | `1` callee(s) | 0 (Entrypoint) |
| [`SchedulerLifecycleTests.test_retention_cleanup_cannot_block_due_slot_evaluation`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_scheduler_lifecycle.py#L30-L39) | method | `L30-L39` | — | `4` callee(s) | 0 (Entrypoint) |
| [`SchedulerLifecycleTests.test_scheduler_and_manual_dispatches_share_one_controller`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_scheduler_lifecycle.py#L50-L56) | method | `L50-L56` | — | `1` callee(s) | 0 (Entrypoint) |
| [`SchedulerLifecycleTests.test_shutdown_cancels_the_retained_scheduler_task`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_scheduler_lifecycle.py#L26-L28) | method | `L26-L28` | — | `1` callee(s) | 0 (Entrypoint) |
| [`SchedulerLifecycleTests.test_startup_retains_a_scheduler_supervisor_task`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_scheduler_lifecycle.py#L13-L16) | method | `L13-L16` | — | `1` callee(s) | 0 (Entrypoint) |
| [`SchedulerLifecycleTests.test_watchdog_knows_when_a_scheduled_dispatch_is_active`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_scheduler_lifecycle.py#L46-L48) | method | `L46-L48` | — | `1` callee(s) | 0 (Entrypoint) |
| [`SchedulerLifecycleTests.test_watchdog_restarts_stale_linux_scheduler_through_systemd`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_scheduler_lifecycle.py#L18-L24) | method | `L18-L24` | — | `1` callee(s) | 0 (Entrypoint) |

### `test_sr_regions.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`ServiceRequestRegionTests`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_sr_regions.py#L13-L241) | class | `L13-L241` | — | 0 | 0 (Entrypoint) |
| [`ServiceRequestRegionTests.setUp`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_sr_regions.py#L14-L31) | method | `L14-L31` | — | `8` callee(s) | 0 (Entrypoint) |
| [`ServiceRequestRegionTests.test_adtv_report_keeps_acso_crm_center_key`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_sr_regions.py#L93-L121) | method | `L93-L121` | — | `9` callee(s) | 0 (Entrypoint) |
| [`ServiceRequestRegionTests.test_missing_raw_workbook_names_the_selected_region`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_sr_regions.py#L41-L44) | method | `L41-L44` | — | `3` callee(s) | 0 (Entrypoint) |
| [`ServiceRequestRegionTests.test_mixed_workbook_filters_all_sheets_and_allows_single_region_exports`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_sr_regions.py#L46-L79) | method | `L46-L79` | — | `18` callee(s) | 0 (Entrypoint) |
| [`ServiceRequestRegionTests.test_prepaid_raw_filter_keeps_only_approved_sr_values`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_sr_regions.py#L200-L214) | method | `L200-L214` | — | `4` callee(s) | 0 (Entrypoint) |
| [`ServiceRequestRegionTests.test_region_paths_are_separate_and_reject_traversal`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_sr_regions.py#L33-L39) | method | `L33-L39` | — | `4` callee(s) | 0 (Entrypoint) |
| [`ServiceRequestRegionTests.test_renderer_writes_only_selected_region`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_sr_regions.py#L226-L241) | method | `L226-L241` | — | `14` callee(s) | 0 (Entrypoint) |
| [`ServiceRequestRegionTests.test_reports_use_center_display_name_for_all_service_request_sources`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_sr_regions.py#L123-L158) | method | `L123-L158` | — | `8` callee(s) | 0 (Entrypoint) |
| [`ServiceRequestRegionTests.test_service_request_centers_sort_case_insensitively`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_sr_regions.py#L216-L224) | method | `L216-L224` | — | `4` callee(s) | 0 (Entrypoint) |
| [`ServiceRequestRegionTests.test_shared_service_names_and_prepaid_service_request_filter`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_sr_regions.py#L160-L198) | method | `L160-L198` | — | `8` callee(s) | 0 (Entrypoint) |
| [`ServiceRequestRegionTests.test_unlabelled_export_is_rejected_when_multiple_regions_exist`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_sr_regions.py#L81-L91) | method | `L81-L91` | — | `8` callee(s) | 0 (Entrypoint) |

### `test_tat_engine.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`test_calculate_tat_metric`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_tat_engine.py#L14-L26) | function | `L14-L26` | — | `2` callee(s) | 0 (Entrypoint) |
| [`test_compute_tat_reports_sorting_and_summary`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_tat_engine.py#L29-L62) | function | `L29-L62` | — | `3` callee(s) | 0 (Entrypoint) |
| [`test_export_tat_excel`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_tat_engine.py#L81-L101) | function | `L81-L101` | — | `3` callee(s) | 0 (Entrypoint) |
| [`test_generate_tat_html_colors`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_tat_engine.py#L65-L78) | function | `L65-L78` | — | `1` callee(s) | 0 (Entrypoint) |

### `test_tat_web_and_telegram.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`test_get_images_for_tat_report_type`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_tat_web_and_telegram.py#L44-L62) | function | `L44-L62` | — | `2` callee(s) | 0 (Entrypoint) |
| [`test_html_template_tat_integration`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_tat_web_and_telegram.py#L150-L171) | function | `L150-L171` | — | `1` callee(s) | 0 (Entrypoint) |
| [`test_is_tat_report_type`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_tat_web_and_telegram.py#L34-L41) | function | `L34-L41` | — | `1` callee(s) | 0 (Entrypoint) |
| [`test_tat_api_download_excel`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_tat_web_and_telegram.py#L85-L89) | function | `L85-L89` | — | `2` callee(s) | 0 (Entrypoint) |
| [`test_tat_api_generate_and_send_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_tat_web_and_telegram.py#L92-L101) | function | `L92-L101` | — | `3` callee(s) | 0 (Entrypoint) |
| [`test_tat_api_render_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_tat_web_and_telegram.py#L76-L82) | function | `L76-L82` | — | `3` callee(s) | 0 (Entrypoint) |
| [`test_tat_api_reports_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_tat_web_and_telegram.py#L65-L73) | function | `L65-L73` | — | `2` callee(s) | 0 (Entrypoint) |
| [`test_tat_api_run_cycle_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_tat_web_and_telegram.py#L104-L112) | function | `L104-L112` | — | `3` callee(s) | 0 (Entrypoint) |
| [`test_telegram_bot_tat_controls`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_tat_web_and_telegram.py#L115-L147) | function | `L115-L147` | — | `9` callee(s) | 0 (Entrypoint) |

### `test_telegram_service_control.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`TelegramServiceControlTests`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_telegram_service_control.py#L8-L65) | class | `L8-L65` | — | 0 | 0 (Entrypoint) |
| [`TelegramServiceControlTests.test_complaint_dispatch_queues_instead_of_waiting_for_whatsapp`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_telegram_service_control.py#L23-L33) | method | `L23-L33` | — | `7` callee(s) | 0 (Entrypoint) |
| [`TelegramServiceControlTests.test_restart_fails_when_no_noninteractive_systemctl_permission`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_telegram_service_control.py#L9-L17) | method | `L9-L17` | — | `5` callee(s) | 0 (Entrypoint) |
| [`TelegramServiceControlTests.test_service_unit_is_explicit_for_the_restricted_sudoers_rule`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_telegram_service_control.py#L19-L20) | method | `L19-L20` | — | `3` callee(s) | 0 (Entrypoint) |
| [`TelegramServiceControlTests.test_sr_dispatch_queues_instead_of_waiting_for_whatsapp`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_telegram_service_control.py#L36-L46) | method | `L36-L46` | — | `7` callee(s) | 0 (Entrypoint) |
| [`TelegramServiceControlTests.test_tat_dispatch_queues_instead_of_waiting_for_whatsapp`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_telegram_service_control.py#L49-L59) | method | `L49-L59` | — | `7` callee(s) | 0 (Entrypoint) |
| [`TelegramServiceControlTests.test_tat_options_in_keyboard`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_telegram_service_control.py#L61-L65) | method | `L61-L65` | — | `2` callee(s) | 0 (Entrypoint) |

### `test_web_server.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`test_routes`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/test_web_server.py#L25-L890) | function | `L25-L890` | — | `64` callee(s) | 0 (Entrypoint) |

### `verify_engine.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`_num`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/verify_engine.py#L34-L35) | function | `L34-L35` | — | `3` callee(s) | 0 (Entrypoint) |
| [`verify`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/verify_engine.py#L38-L111) | function | `L38-L111` | — | `13` callee(s) | 0 (Entrypoint) |

### `web_server.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`AcsoPayload`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L234-L248) | class | `L234-L248` | — | 0 | 0 (Entrypoint) |
| [`ApiLoginPayload`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L316-L317) | class | `L316-L317` | — | 0 | 0 (Entrypoint) |
| [`BulkDeleteDirectoryPayload`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L273-L274) | class | `L273-L274` | — | 0 | 0 (Entrypoint) |
| [`CycleRunPayload`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L300-L303) | class | `L300-L303` | — | 0 | 0 (Entrypoint) |
| [`DirectoryRowPayload`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L259-L270) | class | `L259-L270` | — | 0 | 0 (Entrypoint) |
| [`DispatchRulePayload`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L277-L283) | class | `L277-L283` | — | 0 | 0 (Entrypoint) |
| [`EmployeePayload`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L251-L256) | class | `L251-L256` | — | 0 | 0 (Entrypoint) |
| [`GenerateAndSendPayload`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L295-L297) | class | `L295-L297` | — | 0 | 0 (Entrypoint) |
| [`PendingFollowupSettingsPayload`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L306-L313) | class | `L306-L313` | Settings for only the WhatsApp text after complaint report images. | 0 | 0 (Entrypoint) |
| [`RegionCreate`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L216-L220) | class | `L216-L220` | — | 0 | 0 (Entrypoint) |
| [`ScheduleTimePayload`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L286-L291) | class | `L286-L291` | — | 0 | 0 (Entrypoint) |
| [`TeamLeaderPayload`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L223-L231) | class | `L223-L231` | — | 0 | 0 (Entrypoint) |
| [`_clear_scheduler_slot_active`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L149-L155) | function | `L149-L155` | Clear active dispatch state only for the slot that created it. | 0 | 0 (Entrypoint) |
| [`_complaint_follow_ups`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1346-L1353) | function | `L1346-L1353` | Return image-aligned complaint text without changing reports or SR dispatch. | `2` callee(s) | `3` caller(s) |
| [`_complaint_follow_ups_from_workbook`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1356-L1362) | function | `L1356-L1362` | Build optional image-aligned complaint text without affecting image delivery on failure. | `3` callee(s) | `2` caller(s) |
| [`_compute_complaint_sections`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1331-L1343) | function | `L1331-L1343` | Rebuild complaint report sections from the active region's workbook data. | `7` callee(s) | `3` caller(s) |
| [`_get_report_dispatch_state`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1487-L1489) | function | `L1487-L1489` | — | `1` callee(s) | `1` caller(s) |
| [`_mark_scheduler_slot_active`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L141-L146) | function | `L141-L146` | Tell the watchdog that a valid, long-running dispatch is in progress. | `1` callee(s) | 0 (Entrypoint) |
| [`_queue_report_dispatch`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1565-L1603) | function | `L1565-L1603` | Start one manual report job without making Telegram wait for completion. | `9` callee(s) | `3` caller(s) |
| [`_run_report_dispatch`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1492-L1562) | function | `L1492-L1562` | Run one report job shared by the scheduler, web UI, and Telegram. | `9` callee(s) | `3` caller(s) |
| [`_run_scheduled_retention_cleanup`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2163-L2174) | function | `L2163-L2174` | Run non-essential retention cleanup without blocking schedule evaluation. | `2` callee(s) | `1` caller(s) |
| [`_scheduler_active_slot_snapshot`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L158-L160) | function | `L158-L160` | — | 0 | `1` caller(s) |
| [`_scheduler_watchdog_loop`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L163-L195) | function | `L163-L195` | Restart the systemd service if the scheduler stops progressing. | `6` callee(s) | 0 (Entrypoint) |
| [`_set_report_dispatch_state`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1481-L1484) | function | `L1481-L1484` | — | `3` callee(s) | `1` caller(s) |
| [`_start_scheduler_watchdog`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L198-L211) | function | `L198-L211` | Start one Linux-only scheduler watchdog for the running web process. | `5` callee(s) | `1` caller(s) |
| [`_touch_scheduler_heartbeat`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L134-L138) | function | `L134-L138` | Record that the scheduler event loop is still making progress. | `1` callee(s) | `2` caller(s) |
| [`add_directory_entry_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L525-L528) | endpoint | `L525-L528` | `POST /api/regions/{region_id}/directory` Adds a single employee directory entry. | `3` callee(s) | 0 (Entrypoint) |
| [`add_no_cache_api_headers`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L321-L334) | function | `L321-L334` | — | `8` callee(s) | 0 (Entrypoint) |
| [`api_analyze_logs`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2147-L2150) | endpoint | `L2147-L2150` | `GET /api/logs/analysis` Performs deep log diagnostic analysis, health score calculation, and issue categorization. | `4` callee(s) | 0 (Entrypoint) |
| [`api_cleanup_logs`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2154-L2158) | endpoint | `L2154-L2158` | `POST /api/logs/cleanup` Purges log files older than N days (default 3 days). | `5` callee(s) | 0 (Entrypoint) |
| [`api_get_log_files`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2134-L2136) | endpoint | `L2134-L2136` | `GET /api/logs/files` Returns list of all available running and error log files in logs/ directory. | `2` callee(s) | 0 (Entrypoint) |
| [`api_login`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L338-L342) | endpoint | `L338-L342` | `POST /api/auth/login` — | `5` callee(s) | 0 (Entrypoint) |
| [`api_view_log`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2140-L2143) | endpoint | `L2140-L2143` | `GET /api/logs/view` Returns tail content of a specific log file or today's default log. | `4` callee(s) | 0 (Entrypoint) |
| [`background_scheduler_loop`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2177-L2281) | function | `L2177-L2281` | — | `21` callee(s) | `1` caller(s) |
| [`bulk_delete_directory_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L546-L553) | endpoint | `L546-L553` | `POST /api/regions/{region_id}/directory/bulk-delete` Deletes multiple employee directory entries at once and synchronizes JSON. | `2` callee(s) | 0 (Entrypoint) |
| [`cancel_whatsapp_login`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2120-L2122) | endpoint | `L2120-L2122` | `POST /api/whatsapp/cancel-login` Cancels active QR scan browser session. | `2` callee(s) | 0 (Entrypoint) |
| [`clear_region_configuration_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2089-L2102) | endpoint | `L2089-L2102` | `POST /api/backup/clear` Clears all configured roster data for a region. | `8` callee(s) | 0 (Entrypoint) |
| [`create_acso`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L465-L476) | endpoint | `L465-L476` | `POST /api/regions/{region_id}/acsos` Adds a Center and ACSO Officer to the specified region. | `4` callee(s) | 0 (Entrypoint) |
| [`create_dispatch_rule`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1614-L1618) | endpoint | `L1614-L1618` | `POST /api/regions/{region_id}/dispatch-rules` — | `3` callee(s) | 0 (Entrypoint) |
| [`create_employee`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L496-L499) | endpoint | `L496-L499` | `POST /api/regions/{region_id}/employees` Registers an employee code and staff profile. | `3` callee(s) | 0 (Entrypoint) |
| [`create_region`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L372-L382) | endpoint | `L372-L382` | `POST /api/regions` Creates a new region. | `3` callee(s) | 0 (Entrypoint) |
| [`create_schedule_time`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1689-L1696) | endpoint | `L1689-L1696` | `POST /api/regions/{region_id}/schedule-times` — | `2` callee(s) | 0 (Entrypoint) |
| [`create_team_leader`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L442-L445) | endpoint | `L442-L445` | `POST /api/regions/{region_id}/team-leaders` Adds a new Team Leader to the specified region. | `3` callee(s) | 0 (Entrypoint) |
| [`delete_directory_entry_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L539-L542) | endpoint | `L539-L542` | `DELETE /api/regions/{region_id}/directory/{row_id}` Deletes an employee directory entry. | `2` callee(s) | 0 (Entrypoint) |
| [`delete_dispatch_rule_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1628-L1630) | endpoint | `L1628-L1630` | `DELETE /api/dispatch-rules/{rule_id}` — | `2` callee(s) | 0 (Entrypoint) |
| [`delete_schedule_time_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1712-L1714) | endpoint | `L1712-L1714` | `DELETE /api/schedule-times/{time_id}` — | `2` callee(s) | 0 (Entrypoint) |
| [`dispatch_whatsapp`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1107-L1172) | endpoint | `L1107-L1172` | `POST /api/regions/{region_id}/dispatch-whatsapp` Sends report cards directly to WhatsApp configured for this region based on active dispatch rules. | `24` callee(s) | 0 (Entrypoint) |
| [`download_directory_template_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L691-L757) | endpoint | `L691-L757` | `GET /api/employee-directory/download-template` Downloads a clean, blank formatted Excel template for uploading the Employee Directory. | `16` callee(s) | 0 (Entrypoint) |
| [`download_service_request_excel_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1810-L1826) | endpoint | `L1810-L1826` | `GET /api/service-request/download-excel` Downloads the generated Daily Service Request Pending Excel report. | `9` callee(s) | 0 (Entrypoint) |
| [`download_tat_excel_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1972-L1984) | endpoint | `L1972-L1984` | `GET /api/tat/download-excel` Downloads the generated TAT Turnaround Time Excel report. | `6` callee(s) | 0 (Entrypoint) |
| [`execute_automated_cycle`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1365-L1440) | function | `L1365-L1440` | Pulls fresh tickets from CRM, computes report, renders images, and dispatches per rules. | `35` callee(s) | `2` caller(s) |
| [`execute_automated_tat_cycle`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1443-L1478) | function | `L1443-L1478` | Computes TAT reports, renders images, and dispatches per rules. | `15` callee(s) | `1` caller(s) |
| [`export_configuration_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2055-L2065) | endpoint | `L2055-L2065` | `GET /api/backup/export` Exports configuration backup as JSON. | `6` callee(s) | 0 (Entrypoint) |
| [`export_directory_excel_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L568-L676) | endpoint | `L568-L676` | `GET /api/regions/{region_id}/directory/export-excel` Exports the complete populated Employee Directory for a region in the exact | `21` callee(s) | 0 (Entrypoint) |
| [`export_directory_json_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L557-L564) | endpoint | `L557-L564` | `GET /api/regions/{region_id}/directory/export-json` Exports and downloads the complete Employee Directory as a standalone JSON file. | `3` callee(s) | 0 (Entrypoint) |
| [`generate_and_send_now`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1176-L1262) | endpoint | `L1176-L1262` | `POST /api/regions/{region_id}/generate-and-send` Pulls fresh tickets from CRM, computes report, renders high-DPI cards, | `32` callee(s) | 0 (Entrypoint) |
| [`generate_reports`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1018-L1103) | endpoint | `L1018-L1103` | `POST /api/regions/{region_id}/generate-reports` Computes report for the region and renders high-definition Retina JPEG images. | `30` callee(s) | 0 (Entrypoint) |
| [`get_images_for_report_type`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1267-L1323) | function | `L1267-L1323` | — | `3` callee(s) | `6` caller(s) |
| [`get_pending_followup_settings_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L425-L428) | endpoint | `L425-L428` | `GET /api/regions/{region_id}/pending-followup-settings` — | `4` callee(s) | 0 (Entrypoint) |
| [`get_region_config`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L410-L421) | endpoint | `L410-L421` | `GET /api/regions/{region_id}/config` Fetches all Team Leaders, ACSOs, Centers, and Employees for a region. | `7` callee(s) | 0 (Entrypoint) |
| [`get_region_directory_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L519-L521) | endpoint | `L519-L521` | `GET /api/regions/{region_id}/directory` Fetches the unified employee directory in the 7-column schema. | `2` callee(s) | 0 (Entrypoint) |
| [`get_service_request_reports_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1774-L1790) | endpoint | `L1774-L1790` | `GET /api/service-request/reports` Returns preview tables for ADL and ADTv Service Request Pending. | `7` callee(s) | 0 (Entrypoint) |
| [`get_system_settings`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1726-L1735) | endpoint | `L1726-L1735` | `GET /api/system/settings` — | `3` callee(s) | 0 (Entrypoint) |
| [`get_tat_reports_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1930-L1951) | endpoint | `L1930-L1951` | `GET /api/tat/reports` Returns preview metrics and sorted records for all 4 TAT reports. | `5` callee(s) | 0 (Entrypoint) |
| [`get_whatsapp_auth_status`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2108-L2110) | endpoint | `L2108-L2110` | `GET /api/whatsapp/status` Returns current WhatsApp Web login and QR scan state. | `2` callee(s) | 0 (Entrypoint) |
| [`import_directory_json_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L680-L687) | endpoint | `L680-L687` | `POST /api/regions/{region_id}/directory/import-json` Directly updates the Employee Directory from a JSON array payload. | `3` callee(s) | 0 (Entrypoint) |
| [`is_tat_report_type`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1326-L1328) | function | `L1326-L1328` | — | `3` callee(s) | `6` caller(s) |
| [`list_dispatch_rules`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1609-L1610) | endpoint | `L1609-L1610` | `GET /api/regions/{region_id}/dispatch-rules` — | `2` callee(s) | 0 (Entrypoint) |
| [`list_regions`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L366-L368) | endpoint | `L366-L368` | `GET /api/regions` Returns all 14 Kerala regions with their operational counts. | `2` callee(s) | 0 (Entrypoint) |
| [`list_schedule_times`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1684-L1685) | endpoint | `L1684-L1685` | `GET /api/regions/{region_id}/schedule-times` — | `2` callee(s) | 0 (Entrypoint) |
| [`load_sample_preset_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2080-L2085) | endpoint | `L2080-L2085` | `POST /api/backup/load-sample` Legacy sample presets are disabled to prevent cross-region data imports. | `2` callee(s) | 0 (Entrypoint) |
| [`logout_whatsapp_session`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2126-L2128) | endpoint | `L2126-L2128` | `POST /api/whatsapp/logout` Wipes WhatsApp Web profile and session cache to allow pairing a new phone. | `2` callee(s) | 0 (Entrypoint) |
| [`modify_acso`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L480-L483) | endpoint | `L480-L483` | `PUT /api/regions/{region_id}/acsos/{acso_id}` Updates an existing ACSO Officer and Center mapping. | `3` callee(s) | 0 (Entrypoint) |
| [`modify_employee`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L503-L506) | endpoint | `L503-L506` | `PUT /api/regions/{region_id}/employees/{emp_id}` Updates an employee profile. | `3` callee(s) | 0 (Entrypoint) |
| [`modify_team_leader`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L449-L452) | endpoint | `L449-L452` | `PUT /api/regions/{region_id}/team-leaders/{tl_id}` Updates an existing Team Leader. | `3` callee(s) | 0 (Entrypoint) |
| [`remove_acso`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L487-L490) | endpoint | `L487-L490` | `DELETE /api/regions/{region_id}/acsos/{acso_id}` Removes an ACSO Officer and Center. | `2` callee(s) | 0 (Entrypoint) |
| [`remove_employee`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L510-L513) | endpoint | `L510-L513` | `DELETE /api/regions/{region_id}/employees/{emp_id}` Deletes an employee record. | `2` callee(s) | 0 (Entrypoint) |
| [`remove_region`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L386-L406) | endpoint | `L386-L406` | `DELETE /api/regions/{region_id}` Deletes an unused region, but never the configured default region. | `10` callee(s) | 0 (Entrypoint) |
| [`remove_team_leader`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L456-L459) | endpoint | `L456-L459` | `DELETE /api/regions/{region_id}/team-leaders/{tl_id}` Removes a Team Leader. | `2` callee(s) | 0 (Entrypoint) |
| [`render_tat_reports_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1955-L1968) | endpoint | `L1955-L1968` | `POST /api/tat/render` Generates high-definition Retina cards and Excel report for all 4 TAT reports. | `6` callee(s) | 0 (Entrypoint) |
| [`restore_configuration_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2069-L2076) | endpoint | `L2069-L2076` | `POST /api/backup/restore` Restores configuration from JSON payload. | `4` callee(s) | 0 (Entrypoint) |
| [`run_automated_cycle_now`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1747-L1768) | endpoint | `L1747-L1768` | `POST /api/system/run-automated-cycle-now` — | `6` callee(s) | 0 (Entrypoint) |
| [`run_service_request_cycle_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1794-L1806) | endpoint | `L1794-L1806` | `POST /api/service-request/run-cycle` Triggers the full automated cycle for Service Requests. | `5` callee(s) | 0 (Entrypoint) |
| [`run_tat_cycle_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2037-L2049) | endpoint | `L2037-L2049` | `POST /api/tat/run-cycle` Triggers automated TAT cycle and dispatches to configured recipients. | `5` callee(s) | 0 (Entrypoint) |
| [`scheduler_supervisor_loop`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2284-L2303) | function | `L2284-L2303` | Keep the scheduler alive and visibly recover an unexpected task exit. | `5` callee(s) | `1` caller(s) |
| [`send_service_request_to_phone_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1895-L1924) | endpoint | `L1895-L1924` | `POST /api/service-request/generate-and-send` Generates Service Request reports and dispatches to specific phone number or WhatsApp group. | `12` callee(s) | 0 (Entrypoint) |
| [`send_tat_to_phone_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2020-L2033) | endpoint | `L2020-L2033` | `POST /api/tat/generate-and-send` Generates TAT reports and dispatches to specific phone number or WhatsApp group. | `6` callee(s) | 0 (Entrypoint) |
| [`serve_dashboard`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L348-L360) | endpoint | `L348-L360` | `GET /` Renders the main operational management interface. | `4` callee(s) | 0 (Entrypoint) |
| [`start_scheduler_task`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2307-L2320) | function | `L2307-L2320` | — | `8` callee(s) | 0 (Entrypoint) |
| [`start_whatsapp_login`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2114-L2116) | endpoint | `L2114-L2116` | `POST /api/whatsapp/start-login` Launches background Chromium to fetch WhatsApp Web QR code. | `2` callee(s) | 0 (Entrypoint) |
| [`stop_scheduler_task`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2324-L2335) | function | `L2324-L2335` | Stop local scheduler resources cleanly during an intentional shutdown. | `4` callee(s) | 0 (Entrypoint) |
| [`test_calculation_engine`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L980-L1014) | endpoint | `L980-L1014` | `GET /api/regions/{region_id}/test-engine` Executes pure-Python mathematical computation using dynamic region configuration | `9` callee(s) | 0 (Entrypoint) |
| [`toggle_dispatch_rule_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1634-L1636) | endpoint | `L1634-L1636` | `POST /api/dispatch-rules/{rule_id}/toggle` — | `2` callee(s) | 0 (Entrypoint) |
| [`toggle_master_scheduler`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1739-L1743) | endpoint | `L1739-L1743` | `POST /api/system/scheduler-toggle` — | `3` callee(s) | 0 (Entrypoint) |
| [`toggle_schedule_time_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1718-L1720) | endpoint | `L1718-L1720` | `POST /api/schedule-times/{time_id}/toggle` — | `2` callee(s) | 0 (Entrypoint) |
| [`trigger_dispatch_rule_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1640-L1678) | endpoint | `L1640-L1678` | `POST /api/dispatch-rules/{rule_id}/trigger` — | `23` callee(s) | 0 (Entrypoint) |
| [`update_directory_entry_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L532-L535) | endpoint | `L532-L535` | `PUT /api/regions/{region_id}/directory/{row_id}` Updates a single employee directory entry. | `3` callee(s) | 0 (Entrypoint) |
| [`update_dispatch_rule_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1622-L1624) | endpoint | `L1622-L1624` | `PUT /api/dispatch-rules/{rule_id}` — | `3` callee(s) | 0 (Entrypoint) |
| [`update_pending_followup_settings_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L432-L436) | endpoint | `L432-L436` | `PUT /api/regions/{region_id}/pending-followup-settings` — | `5` callee(s) | 0 (Entrypoint) |
| [`update_schedule_time_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1700-L1708) | endpoint | `L1700-L1708` | `PUT /api/schedule-times/{time_id}` — | `2` callee(s) | 0 (Entrypoint) |
| [`upload_complaints_raw_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1830-L1865) | endpoint | `L1830-L1865` | `POST /api/complaints/upload-raw` Uploads a fresh raw Complaints Excel workbook and re-computes reports immediately. | `16` callee(s) | 0 (Entrypoint) |
| [`upload_directory_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L761-L972) | endpoint | `L761-L972` | `POST /api/regions/{region_id}/upload-directory` Uploads and imports Excel, CSV, or JSON file into the Employee Directory database. | `34` callee(s) | 0 (Entrypoint) |
| [`upload_service_request_raw_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1869-L1891) | endpoint | `L1869-L1891` | `POST /api/service-request/upload-raw` Uploads a fresh raw Excel file and re-computes the reports immediately. | `13` callee(s) | 0 (Entrypoint) |
| [`upload_tat_raw_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1988-L2016) | endpoint | `L1988-L2016` | `POST /api/tat/upload-raw` Uploads a fresh resolved tickets Excel file (Broadband or DTv) and re-computes immediately. | `10` callee(s) | 0 (Entrypoint) |

### `whatsapp_auth_manager.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`_run_playwright_login`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/whatsapp_auth_manager.py#L108-L233) | function | `L108-L233` | — | `26` callee(s) | 0 (Entrypoint) |
| [`cancel_login`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/whatsapp_auth_manager.py#L236-L249) | function | `L236-L249` | Cancels any active login flow and closes the background browser. | `2` callee(s) | `2` caller(s) |
| [`get_whatsapp_status`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/whatsapp_auth_manager.py#L46-L79) | function | `L46-L79` | Returns the current WhatsApp Web session and login status. | `10` callee(s) | `1` caller(s) |
| [`logout_session`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/whatsapp_auth_manager.py#L252-L281) | function | `L252-L281` | Wipes saved WhatsApp Web session completely to allow pairing with a new phone. | `7` callee(s) | `1` caller(s) |
| [`start_login_flow`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/whatsapp_auth_manager.py#L82-L105) | function | `L82-L105` | Starts the background Playwright task to navigate to WhatsApp Web and capture QR codes. | `6` callee(s) | `1` caller(s) |

### `whatsapp_sender.py`

| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`attach_and_prepare_photo`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/whatsapp_sender.py#L74-L124) | function | `L74-L124` | Attaches an image specifically as a full-resolution PHOTO message (never a sticker). | `13` callee(s) | `1` caller(s) |
| [`cleanup_stale_locks`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/whatsapp_sender.py#L41-L49) | function | `L41-L49` | Safely cleans up stale Chromium lockfiles if browser process is dead. | `3` callee(s) | `3` caller(s) |
| [`dismiss_active_dialogs`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/whatsapp_sender.py#L52-L71) | function | `L52-L71` | Safely closes popup dialogs only if an actual dialog overlay is present. | `7` callee(s) | `1` caller(s) |
| [`flash_report_image`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/whatsapp_sender.py#L383-L400) | function | `L383-L400` | Flashes report images with optional combined or image-paired WhatsApp text. | `2` callee(s) | `9` caller(s) |
| [`normalize_recipient`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/whatsapp_sender.py#L24-L38) | function | `L24-L38` | Detects if target is a phone number and formats it with country code if needed. | `6` callee(s) | `3` caller(s) |
| [`send_follow_up_text`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/whatsapp_sender.py#L127-L150) | function | `L127-L150` | Send a plain-text follow-up in the already-open WhatsApp conversation. | `12` callee(s) | `1` caller(s) |
| [`send_via_whatsapp_web`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/whatsapp_sender.py#L153-L380) | function | `L153-L380` | Sends report image(s) to phone numbers or group names via WhatsApp Web using Playwright. | `37` callee(s) | `1` caller(s) |

---

## 3. Ripple Effect & Blast Radius (What Happens if Code Changes?)

This section documents the upstream cascading impact if any core function or component signature is modified.

| Core Function / Component | Direct Impact (Hop 1) | Transitive Cascading Impact (Hop 2) | Critical Failure Risk & Invariants |
| :--- | :--- | :--- | :--- |
| `config.py::resolve_target_excel_path` | `test_routes`, `_compute_complaint_sections`, `execute_automated_cycle`, `generate_and_send_now`, `generate_reports` (+2 more) | `verify`, `_complaint_follow_ups_from_workbook`, `dispatch_whatsapp`, `trigger_dispatch_rule_endpoint`, `upload_complaints_raw_endpoint` (+1 more) | Signature mismatch breaks dependent calling workflows. |
| `db_manager.py::get_connection` | `add_region`, `delete_dispatch_rule`, `ensure_region_exists`, `restore_backup`, `toggle_dispatch_rule` (+38 more) | `download_from_crm`, `load_directory_from_json`, `compute_service_request_reports`, `execute_automated_cycle`, `remove_acso` (+57 more) | Deadlock / database locked if connection is uncommitted or unclosed. Must use PRAGMA foreign_keys = ON. |
| `db_manager.py::get_team_leaders` | `get_unified_directory`, `validate_region_report_directory`, `get_layout_for_region`, `get_region_config` | `sync_directory_to_json`, `compute_pending_days`, `compute_prepaid_pending`, `DirectoryPreflightTests.test_missing_crm_lookup_key_is_reported`, `get_region_directory_endpoint` (+12 more) | Signature mismatch breaks dependent calling workflows. |
| `db_manager.py::get_acsos` | `_filter_configured_centers`, `get_unified_directory`, `validate_region_report_directory`, `get_layout_for_region`, `compute_service_request_reports` (+2 more) | `compute_pending_days`, `compute_prepaid_pending`, `ServiceRequestRegionTests.test_adtv_report_keeps_acso_crm_center_key`, `ServiceRequestRegionTests.test_missing_raw_workbook_names_the_selected_region`, `export_directory_excel_endpoint` (+34 more) | Signature mismatch breaks dependent calling workflows. |
| `crm_downloader.py::download_from_crm` | `execute_cycle`, `run`, `execute_automated_cycle`, `generate_and_send_now`, `generate_reports` | `main`, `run_scheduler_loop`, `run_shell_command`, `LoggerLockSafetyTests.test_retention_cleanup_completes_with_stdout_intercepted`, `test_routes` (+2 more) | Stale dispatch risk if allow_stale policy is breached. Must enforce regional query filters. |
| `crm_downloader.py::download_service_requests_from_crm` | `execute_automated_sr_cycle`, `dispatch_whatsapp`, `generate_and_send_now`, `generate_reports`, `trigger_dispatch_rule_endpoint` (+2 more) | `test_routes`, `_run_report_dispatch` | Signature mismatch breaks dependent calling workflows. |
| `data_processor.py::filter_adl` | `ComplaintCenterIsolationTests.test_similar_center_names_remain_region_isolated`, `_compute_complaint_sections`, `execute_automated_cycle`, `generate_and_send_now`, `generate_reports` (+5 more) | `main`, `test_routes`, `_complaint_follow_ups_from_workbook`, `dispatch_whatsapp`, `trigger_dispatch_rule_endpoint` (+5 more) | Signature mismatch breaks dependent calling workflows. |
| `data_processor.py::filter_adtv` | `ComplaintCenterIsolationTests.test_report_specific_acso_keys_are_accepted_before_filtering`, `ComplaintCenterIsolationTests.test_similar_center_names_remain_region_isolated`, `execute_automated_cycle`, `generate_and_send_now`, `generate_reports` (+6 more) | `main`, `test_routes`, `_complaint_follow_ups_from_workbook`, `dispatch_whatsapp`, `trigger_dispatch_rule_endpoint` (+5 more) | Signature mismatch breaks dependent calling workflows. |
| `data_processor.py::filter_prepaid` | `ComplaintCenterIsolationTests.test_report_specific_acso_keys_are_accepted_before_filtering`, `ComplaintCenterIsolationTests.test_similar_center_names_remain_region_isolated`, `execute_automated_cycle`, `generate_and_send_now`, `generate_reports` (+6 more) | `main`, `test_routes`, `_complaint_follow_ups_from_workbook`, `dispatch_whatsapp`, `trigger_dispatch_rule_endpoint` (+5 more) | Signature mismatch breaks dependent calling workflows. |
| `data_processor.py::ensure_region_directory_ready` | `execute_cycle`, `execute_automated_cycle`, `execute_automated_tat_cycle`, `trigger_dispatch_rule_endpoint`, `upload_complaints_raw_endpoint` (+14 more) | `compute_all_sections`, `main`, `run_scheduler_loop`, `run_shell_command`, `test_routes` (+3 more) | Prevents invalid report rendering when employee codes don't match the database. |
| `report_engine.py::compute_report` | `verify`, `_compute_complaint_sections`, `execute_automated_cycle`, `generate_and_send_now`, `generate_reports` (+4 more) | `compute_all_sections`, `test_routes`, `_complaint_follow_ups_from_workbook`, `dispatch_whatsapp`, `trigger_dispatch_rule_endpoint` (+4 more) | Calculation divergence from gold-standard Excel parity. Breaks daily QoS metrics. |
| `report_layout.py::get_layout_for_region` | `compute_pending_days`, `compute_prepaid_pending`, `validate_inputs`, `compute_tat_reports`, `verify` (+2 more) | `test_compute_tat_reports_sorting_and_summary`, `_compute_complaint_sections`, `execute_automated_cycle`, `generate_and_send_now`, `generate_reports` (+5 more) | Breaks all TL / ACSO row alignments and Excel export formulas. |
| `service_request_engine.py::compute_service_request_reports` | `ServiceRequestRegionTests.test_missing_raw_workbook_names_the_selected_region`, `ServiceRequestRegionTests.test_mixed_workbook_filters_all_sheets_and_allows_single_region_exports`, `dispatch_whatsapp`, `generate_and_send_now`, `generate_reports` (+13 more) | `ServiceRequestRegionTests.test_renderer_writes_only_selected_region`, `test_routes`, `_run_report_dispatch` | Service Request report failure or wrong region filtering if region_id is omitted. |
| `service_request_engine.py::render_sr_report_images` | `execute_automated_sr_cycle`, `ServiceRequestRegionTests.test_renderer_writes_only_selected_region`, `dispatch_whatsapp`, `generate_and_send_now`, `generate_reports` (+3 more) | `test_routes`, `_run_report_dispatch` | Signature mismatch breaks dependent calling workflows. |
| `report_image_generator.py::generate_report_images` | `generate_all_report_images`, `dispatch_whatsapp`, `execute_automated_cycle`, `generate_and_send_now`, `generate_reports` (+3 more) | `main`, `run_scheduler_loop`, `run_shell_command`, `LoggerLockSafetyTests.test_retention_cleanup_completes_with_stdout_intercepted`, `test_routes` (+2 more) | Signature mismatch breaks dependent calling workflows. |
| `whatsapp_sender.py::flash_report_image` | `execute_automated_sr_cycle`, `dispatch_tat_reports`, `dispatch_whatsapp`, `execute_automated_cycle`, `generate_and_send_now` (+4 more) | `main`, `run_scheduler_loop`, `run_shell_command`, `test_routes`, `send_tat_to_phone_endpoint` (+4 more) | WhatsApp Web session crash, modal block, or duplicate message flooding. |
| `telegram_bot.py::TelegramBotRunner` | `main` | None | Signature mismatch breaks dependent calling workflows. |
| `web_server.py::upload_complaints_raw_endpoint` | None | None | Cross-region data pollution if region_id is not passed or defaults incorrectly. |
| `web_server.py::upload_service_request_raw_endpoint` | None | None | Signature mismatch breaks dependent calling workflows. |

---

## 4. REST API Endpoints Wiring Table

| Method | Endpoint Path | Handler Function | File | Line |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | [`serve_dashboard`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L348) | `web_server.py` | `L348` |
| `POST` | `/api/auth/login` | [`api_login`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L338) | `web_server.py` | `L338` |
| `POST` | `/api/backup/clear` | [`clear_region_configuration_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2089) | `web_server.py` | `L2089` |
| `GET` | `/api/backup/export` | [`export_configuration_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2055) | `web_server.py` | `L2055` |
| `POST` | `/api/backup/load-sample` | [`load_sample_preset_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2080) | `web_server.py` | `L2080` |
| `POST` | `/api/backup/restore` | [`restore_configuration_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2069) | `web_server.py` | `L2069` |
| `POST` | `/api/complaints/upload-raw` | [`upload_complaints_raw_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1830) | `web_server.py` | `L1830` |
| `DELETE` | `/api/dispatch-rules/{rule_id}` | [`delete_dispatch_rule_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1628) | `web_server.py` | `L1628` |
| `PUT` | `/api/dispatch-rules/{rule_id}` | [`update_dispatch_rule_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1622) | `web_server.py` | `L1622` |
| `POST` | `/api/dispatch-rules/{rule_id}/toggle` | [`toggle_dispatch_rule_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1634) | `web_server.py` | `L1634` |
| `POST` | `/api/dispatch-rules/{rule_id}/trigger` | [`trigger_dispatch_rule_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1640) | `web_server.py` | `L1640` |
| `GET` | `/api/employee-directory/download-template` | [`download_directory_template_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L691) | `web_server.py` | `L691` |
| `GET` | `/api/logs/analysis` | [`api_analyze_logs`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2147) | `web_server.py` | `L2147` |
| `POST` | `/api/logs/cleanup` | [`api_cleanup_logs`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2154) | `web_server.py` | `L2154` |
| `GET` | `/api/logs/files` | [`api_get_log_files`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2134) | `web_server.py` | `L2134` |
| `GET` | `/api/logs/view` | [`api_view_log`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2140) | `web_server.py` | `L2140` |
| `GET` | `/api/regions` | [`list_regions`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L366) | `web_server.py` | `L366` |
| `POST` | `/api/regions` | [`create_region`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L372) | `web_server.py` | `L372` |
| `DELETE` | `/api/regions/{region_id}` | [`remove_region`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L386) | `web_server.py` | `L386` |
| `POST` | `/api/regions/{region_id}/acsos` | [`create_acso`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L465) | `web_server.py` | `L465` |
| `DELETE` | `/api/regions/{region_id}/acsos/{acso_id}` | [`remove_acso`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L487) | `web_server.py` | `L487` |
| `PUT` | `/api/regions/{region_id}/acsos/{acso_id}` | [`modify_acso`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L480) | `web_server.py` | `L480` |
| `GET` | `/api/regions/{region_id}/config` | [`get_region_config`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L410) | `web_server.py` | `L410` |
| `GET` | `/api/regions/{region_id}/directory` | [`get_region_directory_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L519) | `web_server.py` | `L519` |
| `POST` | `/api/regions/{region_id}/directory` | [`add_directory_entry_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L525) | `web_server.py` | `L525` |
| `POST` | `/api/regions/{region_id}/directory/bulk-delete` | [`bulk_delete_directory_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L546) | `web_server.py` | `L546` |
| `GET` | `/api/regions/{region_id}/directory/export-excel` | [`export_directory_excel_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L568) | `web_server.py` | `L568` |
| `GET` | `/api/regions/{region_id}/directory/export-json` | [`export_directory_json_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L557) | `web_server.py` | `L557` |
| `POST` | `/api/regions/{region_id}/directory/import-json` | [`import_directory_json_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L680) | `web_server.py` | `L680` |
| `DELETE` | `/api/regions/{region_id}/directory/{row_id}` | [`delete_directory_entry_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L539) | `web_server.py` | `L539` |
| `PUT` | `/api/regions/{region_id}/directory/{row_id}` | [`update_directory_entry_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L532) | `web_server.py` | `L532` |
| `GET` | `/api/regions/{region_id}/dispatch-rules` | [`list_dispatch_rules`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1609) | `web_server.py` | `L1609` |
| `POST` | `/api/regions/{region_id}/dispatch-rules` | [`create_dispatch_rule`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1614) | `web_server.py` | `L1614` |
| `POST` | `/api/regions/{region_id}/dispatch-whatsapp` | [`dispatch_whatsapp`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1107) | `web_server.py` | `L1107` |
| `POST` | `/api/regions/{region_id}/employees` | [`create_employee`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L496) | `web_server.py` | `L496` |
| `DELETE` | `/api/regions/{region_id}/employees/{emp_id}` | [`remove_employee`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L510) | `web_server.py` | `L510` |
| `PUT` | `/api/regions/{region_id}/employees/{emp_id}` | [`modify_employee`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L503) | `web_server.py` | `L503` |
| `POST` | `/api/regions/{region_id}/generate-and-send` | [`generate_and_send_now`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1176) | `web_server.py` | `L1176` |
| `POST` | `/api/regions/{region_id}/generate-reports` | [`generate_reports`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1018) | `web_server.py` | `L1018` |
| `GET` | `/api/regions/{region_id}/pending-followup-settings` | [`get_pending_followup_settings_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L425) | `web_server.py` | `L425` |
| `PUT` | `/api/regions/{region_id}/pending-followup-settings` | [`update_pending_followup_settings_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L432) | `web_server.py` | `L432` |
| `GET` | `/api/regions/{region_id}/schedule-times` | [`list_schedule_times`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1684) | `web_server.py` | `L1684` |
| `POST` | `/api/regions/{region_id}/schedule-times` | [`create_schedule_time`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1689) | `web_server.py` | `L1689` |
| `POST` | `/api/regions/{region_id}/team-leaders` | [`create_team_leader`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L442) | `web_server.py` | `L442` |
| `DELETE` | `/api/regions/{region_id}/team-leaders/{tl_id}` | [`remove_team_leader`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L456) | `web_server.py` | `L456` |
| `PUT` | `/api/regions/{region_id}/team-leaders/{tl_id}` | [`modify_team_leader`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L449) | `web_server.py` | `L449` |
| `GET` | `/api/regions/{region_id}/test-engine` | [`test_calculation_engine`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L980) | `web_server.py` | `L980` |
| `POST` | `/api/regions/{region_id}/upload-directory` | [`upload_directory_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L761) | `web_server.py` | `L761` |
| `DELETE` | `/api/schedule-times/{time_id}` | [`delete_schedule_time_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1712) | `web_server.py` | `L1712` |
| `PUT` | `/api/schedule-times/{time_id}` | [`update_schedule_time_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1700) | `web_server.py` | `L1700` |
| `POST` | `/api/schedule-times/{time_id}/toggle` | [`toggle_schedule_time_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1718) | `web_server.py` | `L1718` |
| `GET` | `/api/service-request/download-excel` | [`download_service_request_excel_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1810) | `web_server.py` | `L1810` |
| `POST` | `/api/service-request/generate-and-send` | [`send_service_request_to_phone_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1895) | `web_server.py` | `L1895` |
| `GET` | `/api/service-request/reports` | [`get_service_request_reports_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1774) | `web_server.py` | `L1774` |
| `POST` | `/api/service-request/run-cycle` | [`run_service_request_cycle_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1794) | `web_server.py` | `L1794` |
| `POST` | `/api/service-request/upload-raw` | [`upload_service_request_raw_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1869) | `web_server.py` | `L1869` |
| `POST` | `/api/system/run-automated-cycle-now` | [`run_automated_cycle_now`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1747) | `web_server.py` | `L1747` |
| `POST` | `/api/system/scheduler-toggle` | [`toggle_master_scheduler`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1739) | `web_server.py` | `L1739` |
| `GET` | `/api/system/settings` | [`get_system_settings`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1726) | `web_server.py` | `L1726` |
| `GET` | `/api/tat/download-excel` | [`download_tat_excel_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1972) | `web_server.py` | `L1972` |
| `POST` | `/api/tat/generate-and-send` | [`send_tat_to_phone_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2020) | `web_server.py` | `L2020` |
| `POST` | `/api/tat/render` | [`render_tat_reports_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1955) | `web_server.py` | `L1955` |
| `GET` | `/api/tat/reports` | [`get_tat_reports_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1930) | `web_server.py` | `L1930` |
| `POST` | `/api/tat/run-cycle` | [`run_tat_cycle_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2037) | `web_server.py` | `L2037` |
| `POST` | `/api/tat/upload-raw` | [`upload_tat_raw_endpoint`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L1988) | `web_server.py` | `L1988` |
| `POST` | `/api/whatsapp/cancel-login` | [`cancel_whatsapp_login`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2120) | `web_server.py` | `L2120` |
| `POST` | `/api/whatsapp/logout` | [`logout_whatsapp_session`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2126) | `web_server.py` | `L2126` |
| `POST` | `/api/whatsapp/start-login` | [`start_whatsapp_login`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2114) | `web_server.py` | `L2114` |
| `GET` | `/api/whatsapp/status` | [`get_whatsapp_auth_status`](file:///C:/Users/Anoop P/Antigravity/Daily Work Flow/web_server.py#L2108) | `web_server.py` | `L2108` |

---

## 5. Automated Documentation Synchronization (How to Keep Wiring Updated)

To ensure that this wiring blueprint **never becomes stale** when future code edits are made:

### Automatic Git Post-Commit Hook
Whenever a developer or agent commits changes to git, this document regenerates automatically via `.git/hooks/post-commit`:
```bash
python generate_wiring_docs.py
```

### Graft Repository Knowledge Graph Sync
This repository is also fully synchronized with `graft/`: small linked markdown nodes that verify symbols and line numbers via:
```bash
graft build
```

### Verification Test Suite
Before deploying any changes to production, run the automated test suite:
```bash
pytest -v
```
