"""
test_tat_web_and_telegram.py
============================
Unit & integration tests verifying TAT Turnaround Time endpoints in web_server,
templates/index.html UI components, and telegram_bot interactions.
"""

import os
os.environ["WEB_API_TOKEN"] = "test-token"

from unittest.mock import Mock, patch
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

import config
config.WEB_API_TOKEN = "test-token"

import web_server
web_server.WEB_API_TOKEN = "test-token"
from web_server import app, is_tat_report_type, get_images_for_report_type
from config import (
    TAT_ADL_CENTER_IMAGE_PATH,
    TAT_ADL_TL_IMAGE_PATH,
    TAT_ADTV_CENTER_IMAGE_PATH,
    TAT_ADTV_TL_IMAGE_PATH,
    TAT_EXCEL_REPORT_PATH,
)
import telegram_bot

client = TestClient(app, headers={"Authorization": "Bearer test-token"})


def test_is_tat_report_type():
    assert is_tat_report_type("tat") is True
    assert is_tat_report_type("tat_all") is True
    assert is_tat_report_type("tat_adl_center") is True
    assert is_tat_report_type("tat_adtv_tl") is True
    assert is_tat_report_type("turnaround_time") is True
    assert is_tat_report_type("complaint") is False
    assert is_tat_report_type("sr") is False


def test_get_images_for_tat_report_type():
    adl_center = get_images_for_report_type("tat_adl_center")
    assert adl_center == [TAT_ADL_CENTER_IMAGE_PATH]

    adl_tl = get_images_for_report_type("tat_adl_tl")
    assert adl_tl == [TAT_ADL_TL_IMAGE_PATH]

    adtv_center = get_images_for_report_type("tat_adtv_center")
    assert adtv_center == [TAT_ADTV_CENTER_IMAGE_PATH]

    adtv_tl = get_images_for_report_type("tat_adtv_tl")
    assert adtv_tl == [TAT_ADTV_TL_IMAGE_PATH]

    tat_all = get_images_for_report_type("tat_all")
    assert len(tat_all) == 4
    assert TAT_ADL_CENTER_IMAGE_PATH in tat_all
    assert TAT_ADL_TL_IMAGE_PATH in tat_all
    assert TAT_ADTV_CENTER_IMAGE_PATH in tat_all
    assert TAT_ADTV_TL_IMAGE_PATH in tat_all


def test_tat_api_reports_endpoint():
    res = client.get("/api/tat/reports?region_id=thrissur")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "OK"
    assert "adl_center" in data
    assert "adl_tl" in data
    assert "adtv_center" in data
    assert "adtv_tl" in data


def test_tat_api_render_endpoint():
    res = client.post("/api/tat/render?region_id=thrissur")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "OK"
    assert "images" in data
    assert len(data["images"]) == 4


def test_tat_api_download_excel():
    res = client.get("/api/tat/download-excel?region_id=thrissur")
    assert res.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in res.headers["content-type"]
    assert len(res.content) > 1000


def test_tat_api_generate_and_send_endpoint():
    with patch("whatsapp_sender.flash_report_image", return_value=True), patch("tat_engine.render_tat_report_images", return_value={}):
        res = client.post(
            "/api/tat/generate-and-send?region_id=thrissur",
            json={"target_phone": "+919846000000", "report_type": "tat_all"},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "OK"
        assert "9846000000" in data["message"]


def test_tat_api_run_cycle_endpoint():
    with patch("whatsapp_sender.flash_report_image", return_value=True), patch("tat_engine.render_tat_report_images", return_value={}):
        res = client.post(
            "/api/tat/run-cycle?region_id=thrissur",
            json={"region_id": "thrissur", "background": False},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["status"] in ("OK", "QUEUED")


def test_telegram_bot_tat_controls():
    # 1. Keyboard buttons
    kb = telegram_bot.get_render_send_menu_keyboard()
    callbacks = [btn["callback_data"] for row in kb["inline_keyboard"] for btn in row]
    texts = [btn["text"] for row in kb["inline_keyboard"] for btn in row]
    assert "action:send_tat" in callbacks
    assert "action:test_tat" in callbacks
    assert any("Send TAT" in t for t in texts)
    assert any("Test Send TAT" in t for t in texts)

    # 2. Render and send message documentation
    msg = telegram_bot.format_render_send_menu_message()
    assert "Send TAT" in msg
    assert "Test Send TAT" in msg

    # 3. Alert retry keyboard
    alert_kb = telegram_bot.get_alert_retry_keyboard("tat")
    alert_cbs = [btn["callback_data"] for row in alert_kb["inline_keyboard"] for btn in row]
    assert "action:send_tat" in alert_cbs

    # 4. Trigger functions
    with patch("telegram_bot.requests.post") as mock_post:
        mock_resp = Mock(status_code=200)
        mock_resp.json.return_value = {"status": "OK", "message": "TAT reports delivered to +919846112233 successfully."}
        mock_post.return_value = mock_resp

        ok, out_msg = telegram_bot.trigger_tat_dispatch("thrissur")
        assert ok is True
        assert "delivered" in out_msg.lower()

        ok_test, test_msg = telegram_bot.trigger_tat_test_delivery("+919846112233", "thrissur")
        assert ok_test is True
        assert "delivered" in test_msg.lower()


def test_html_template_tat_integration():
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    # Action bar buttons & download link
    assert "renderTATReports" in html
    assert "/api/tat/download-excel" in html
    assert "tat-file-upload" in html
    assert "uploadRawTATExcel" in html
    assert "dispatchToWhatsApp('tat')" in html

    # Test delivery dropdown
    assert 'value="tat_all"' in html
    assert 'value="tat_adl_center"' in html
    assert 'value="tat_adtv_tl"' in html

    # Preview cards
    assert 'id="img-tat-adl-center"' in html
    assert 'id="img-tat-adl-tl"' in html
    assert 'id="img-tat-adtv-center"' in html
    assert 'id="img-tat-adtv-tl"' in html
