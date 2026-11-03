import json
import os

import httpx

from .schema import Site
from .storage import save_site

SYSTEM_PROMPT = """Je bent een website-bouwer-agent. Je ontvangt de huidige site als JSON
en een opdracht van de gebruiker in natuurlijke taal.

Geef ALLEEN geldige JSON terug, zonder markdown, met precies deze velden:
{
  "reply": "<korte uitleg in het Nederlands van wat je hebt aangepast>",
  "site": { <de volledige nieuwe site-JSON, zelfde structuur als de input> }
}

Regels:
- Behoud het id van de site.
- Gebruik uitsluitend deze blok-types: hero, text, features, gallery, pricing, contact, footer.
- Elke blok heeft een "type"-veld; hou je exact aan de veldnamen uit de input.
- Voeg hooguit 8 blokken toe en houd de site realistisch en verzorgd.
- theme heeft primaryColor (hex-kleur) en fontFamily.
- Verander nooit velden die de gebruiker niet genoemd heeft, tenzij de opdracht daarom vraagt.
"""

PROVIDERS = {
    "mistral": "https://api.mistral.ai/v1/chat/completions",
    "openai": "https://api.openai.com/v1/chat/completions",
}


class AgentError(Exception):
    pass


def _call_llm(site: Site, message: str) -> str:
    provider = os.environ.get("WEBBUILDER_AI_PROVIDER", "mistral").lower()
    api_key = os.environ.get("WEBBUILDER_AI_API_KEY", "")
    model = os.environ.get("WEBBUILDER_AI_MODEL", "mistral-large-latest")
    url = PROVIDERS.get(provider)
    if not url:
        raise AgentError(f"Onbekende AI-provider: {provider}")
    if not api_key:
        raise AgentError(
            "Geen API-key ingesteld. Zet WEBBUILDER_AI_API_KEY in de omgevingsvariabelen."
        )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Huidige site:\n{site.model_dump_json(indent=2)}\n\n"
                    f"Opdracht van de gebruiker:\n{message}"
                ),
            },
        ],
        "temperature": 0.4,
        "response_format": {"type": "json_object"},
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    response = httpx.post(url, json=payload, headers=headers, timeout=60)
    if response.status_code != 200:
        raise AgentError(f"AI-provider fout {response.status_code}: {response.text[:300]}")
    return response.json()["choices"][0]["message"]["content"]


def apply_prompt(site: Site, message: str) -> tuple[Site, str]:
    content = _call_llm(site, message)
    try:
        data = json.loads(content)
        updated = Site.model_validate(data["site"])
        reply = str(data.get("reply", ""))
    except (json.JSONDecodeError, KeyError, ValueError) as exc:
        raise AgentError(f"Ongeldig antwoord van de AI: {exc}") from exc
    updated.id = site.id
    updated.version = site.version + 1
    save_site(updated)
    return updated, reply
