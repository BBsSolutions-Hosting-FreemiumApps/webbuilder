from typing import Literal, Optional

from pydantic import BaseModel, Field


class HeroBlock(BaseModel):
    type: Literal["hero"] = "hero"
    heading: str = ""
    subheading: str = ""
    imageUrl: Optional[str] = None
    ctaLabel: Optional[str] = None


class TextBlock(BaseModel):
    type: Literal["text"] = "text"
    heading: str = ""
    body: str = ""


class FeaturesBlock(BaseModel):
    type: Literal["features"] = "features"
    heading: str = ""
    items: list[str] = Field(default_factory=list)


class GalleryBlock(BaseModel):
    type: Literal["gallery"] = "gallery"
    heading: str = ""
    images: list[str] = Field(default_factory=list)


class PricingBlock(BaseModel):
    type: Literal["pricing"] = "pricing"
    heading: str = ""
    plans: list[dict[str, str]] = Field(default_factory=list)


class ContactFormBlock(BaseModel):
    type: Literal["contact"] = "contact"
    heading: str = ""
    email: str = ""


class FooterBlock(BaseModel):
    type: Literal["footer"] = "footer"
    text: str = ""
    links: list[dict[str, str]] = Field(default_factory=list)


Block = (
    HeroBlock
    | TextBlock
    | FeaturesBlock
    | GalleryBlock
    | PricingBlock
    | ContactFormBlock
    | FooterBlock
)


class SiteTheme(BaseModel):
    primaryColor: str = "#4f46e5"
    fontFamily: str = "system-ui, sans-serif"


class Site(BaseModel):
    id: str
    name: str
    theme: SiteTheme = SiteTheme()
    blocks: list[Block] = Field(default_factory=list)
    version: int = 1


class ChatRequest(BaseModel):
    siteId: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    site: Site
