import json
import os
import threading
import uuid

from .schema import FooterBlock, HeroBlock, Site, SiteTheme, TextBlock

DATA_DIR = os.environ.get("WEBBUILDER_DATA_DIR", "/tmp/webbuilder-data")
SITES_FILE = os.path.join(DATA_DIR, "sites.json")

_lock = threading.Lock()


def _ensure_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_all() -> dict[str, dict]:
    if not os.path.exists(SITES_FILE):
        return {}
    with open(SITES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_all(sites: dict[str, dict]) -> None:
    _ensure_dir()
    tmp = SITES_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(sites, f, ensure_ascii=False, indent=2)
    os.replace(tmp, SITES_FILE)


def create_site(name: str) -> Site:
    site = Site(
        id=uuid.uuid4().hex[:12],
        name=name,
        theme=SiteTheme(),
        blocks=[
            HeroBlock(
                heading=f"Welkom bij {name}",
                subheading="Pas deze site aan door gewoon te typen wat je wilt.",
                ctaLabel="Neem contact op",
            ),
            TextBlock(
                heading="Over ons",
                body="Vertel hier iets meer over jezelf of je bedrijf.",
            ),
            FooterBlock(text=f"© {name}"),
        ],
    )
    save_site(site)
    return site


def get_site(site_id: str) -> Site | None:
    with _lock:
        data = _load_all()
    if site_id not in data:
        return None
    return Site.model_validate(data[site_id])


def save_site(site: Site) -> None:
    with _lock:
        data = _load_all()
        data[site.id] = site.model_dump(mode="json")
        _save_all(data)


def list_sites() -> list[Site]:
    with _lock:
        data = _load_all()
    return [Site.model_validate(v) for v in data.values()]
