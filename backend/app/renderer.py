import html

from .schema import (
    ContactFormBlock,
    FeaturesBlock,
    FooterBlock,
    GalleryBlock,
    HeroBlock,
    PricingBlock,
    Site,
    TextBlock,
)


def _esc(value: str) -> str:
    return html.escape(value or "")


def _render_hero(block: HeroBlock, theme) -> str:
    img = (
        f'<img class="hero-img" src="{_esc(block.imageUrl)}" alt="">'
        if block.imageUrl
        else ""
    )
    cta = (
        f'<a class="btn" href="#contact">{_esc(block.ctaLabel)}</a>'
        if block.ctaLabel
        else ""
    )
    return f"""
    <section class="hero">
      {img}
      <div class="hero-text">
        <h1>{_esc(block.heading)}</h1>
        <p>{_esc(block.subheading)}</p>
        {cta}
      </div>
    </section>"""


def _render_text(block: TextBlock) -> str:
    heading = f"<h2>{_esc(block.heading)}</h2>" if block.heading else ""
    return f"""
    <section class="section">
      {heading}
      <p>{_esc(block.body)}</p>
    </section>"""


def _render_features(block: FeaturesBlock) -> str:
    items = "".join(f"<li>{_esc(item)}</li>" for item in block.items)
    return f"""
    <section class="section">
      <h2>{_esc(block.heading)}</h2>
      <ul class="features">{items}</ul>
    </section>"""


def _render_gallery(block: GalleryBlock) -> str:
    imgs = "".join(
        f'<figure><img src="{_esc(src)}" alt=""></figure>' for src in block.images
    )
    return f"""
    <section class="section">
      <h2>{_esc(block.heading)}</h2>
      <div class="gallery">{imgs}</div>
    </section>"""


def _render_pricing(block: PricingBlock) -> str:
    plans = ""
    for plan in block.plans:
        plans += (
            '<div class="plan">'
            f'<h3>{_esc(plan.get("name", ""))}</h3>'
            f'<p class="price">{_esc(plan.get("price", ""))}</p>'
            f'<p>{_esc(plan.get("description", ""))}</p>'
            "</div>"
        )
    return f"""
    <section class="section">
      <h2>{_esc(block.heading)}</h2>
      <div class="plans">{plans}</div>
    </section>"""


def _render_contact(block: ContactFormBlock) -> str:
    email_line = (
        f'<p class="muted">Wordt verstuurd naar: {_esc(block.email)}</p>'
        if block.email
        else ""
    )
    return f"""
    <section class="section" id="contact">
      <h2>{_esc(block.heading)}</h2>
      <form class="contact-form" onsubmit="event.preventDefault()">
        <input type="text" placeholder="Naam" required>
        <input type="email" placeholder="E-mail" required>
        <textarea placeholder="Bericht" rows="4" required></textarea>
        <button class="btn" type="submit">Versturen</button>
      </form>
      {email_line}
    </section>"""


def _render_footer(block: FooterBlock) -> str:
    links = "".join(
        f'<a href="{_esc(link.get("url", "#"))}">{_esc(link.get("label", ""))}</a>'
        for link in block.links
    )
    return f"""
    <footer class="footer">
      <p>{_esc(block.text)}</p>
      <nav>{links}</nav>
    </footer>"""


_STYLES = """
* { box-sizing: border-box; margin: 0; }
body { font-family: {font}; color: #1f2937; background: #f8fafc; }
.hero { display: flex; flex-direction: column; align-items: center; gap: 1rem;
  background: linear-gradient(135deg, {primary}, #1e293b); color: #fff;
  padding: 4rem 1.5rem; text-align: center; }
.hero h1 { font-size: 2.5rem; }
.hero-img { max-width: 260px; border-radius: 12px; }
.btn { display: inline-block; margin-top: 1rem; background: #fff; color: {primary};
  padding: .7rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600; }
.section { max-width: 820px; margin: 0 auto; padding: 3rem 1.5rem; }
.section h2 { margin-bottom: 1rem; }
.features { list-style: none; padding: 0; display: grid; gap: .6rem; }
.gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; }
.gallery img { width: 100%; border-radius: 10px; }
.plans { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }
.plan { background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.5rem; }
.price { font-size: 1.4rem; font-weight: 700; color: {primary}; margin: .5rem 0; }
.contact-form { display: grid; gap: .8rem; }
.contact-form input, .contact-form textarea { padding: .7rem; border-radius: 8px;
  border: 1px solid #cbd5e1; font: inherit; }
.footer { background: #1e293b; color: #94a3b8; padding: 2rem 1.5rem; text-align: center; }
.footer nav { margin-top: .8rem; display: flex; gap: 1rem; justify-content: center; }
.footer a { color: #cbd5e1; }
"""


def render_html(site: Site) -> str:
    body = ""
    for block in site.blocks:
        match block:
            case HeroBlock():
                body += _render_hero(block, site.theme)
            case TextBlock():
                body += _render_text(block)
            case FeaturesBlock():
                body += _render_features(block)
            case GalleryBlock():
                body += _render_gallery(block)
            case PricingBlock():
                body += _render_pricing(block)
            case ContactFormBlock():
                body += _render_contact(block)
            case FooterBlock():
                body += _render_footer(block)
    styles = (
        _STYLES.replace("{primary}", site.theme.primaryColor)
        .replace("{font}", site.theme.fontFamily)
    )
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_esc(site.name)}</title>
<style>{styles}</style>
</head>
<body>{body}
</body>
</html>"""
