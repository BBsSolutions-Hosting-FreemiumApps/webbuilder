import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.renderer import render_html
from app.schema import ContactFormBlock, PricingBlock, Site, SiteTheme

client = TestClient(app)


def test_create_and_get_site(tmp_path, monkeypatch):
    monkeypatch.setenv("WEBBUILDER_DATA_DIR", str(tmp_path))
    response = client.post("/sites?name=Testsite")
    assert response.status_code == 200
    site = response.json()
    assert site["name"] == "Testsite"
    assert site["blocks"][0]["type"] == "hero"

    got = client.get(f"/sites/{site['id']}")
    assert got.status_code == 200
    assert got.json()["id"] == site["id"]


def test_render_escapes_html():
    site = Site(
        id="x",
        name="<script>alert(1)</script>",
        theme=SiteTheme(),
        blocks=[ContactFormBlock(heading="Contact", email="a@b.nl")],
    )
    html = render_html(site)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_render_pricing_and_footer():
    site = Site(
        id="x",
        name="Prijshuis",
        blocks=[
            PricingBlock(
                heading="Tarieven",
                plans=[
                    {"name": "Basis", "price": "€10", "description": "Alles wat je nodig hebt"}
                ],
            )
        ],
        theme=SiteTheme(),
    )
    html = render_html(site)
    assert "€10" in html
    assert "Tarieven" in html


def test_chat_without_api_key_returns_502(tmp_path, monkeypatch):
    monkeypatch.setenv("WEBBUILDER_DATA_DIR", str(tmp_path))
    monkeypatch.delenv("WEBBUILDER_AI_API_KEY", raising=False)
    site = client.post("/sites?name=T").json()
    response = client.post("/chat", json={"siteId": site["id"], "message": "test"})
    assert response.status_code == 502
