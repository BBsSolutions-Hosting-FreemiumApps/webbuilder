"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { createSite, renderUrl, sendPrompt, Site } from "@/lib/api";

interface Message {
  role: "user" | "assistant" | "error";
  text: string;
}

export default function Home() {
  const [site, setSite] = useState<Site | null>(null);
  const [siteName, setSiteName] = useState("Mijn website");
  const [prompt, setPrompt] = useState("");
  const [busy, setBusy] = useState(false);
  const [previewKey, setPreviewKey] = useState(0);
  const [messages, setMessages] = useState<Message[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleStart(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    try {
      const created = await createSite(siteName);
      setSite(created);
      setMessages([
        {
          role: "assistant",
          text:
            `Je site "${created.name}" staat klaar! Zeg bijvoorbeeld:\n` +
            "- maak het een warm en gastvrij design\n" +
            "- voeg een prijzen-sectie toe met 3 abonnementen\n" +
            "- verander de hoofdkleur naar groen",
        },
      ]);
    } catch (err) {
      setMessages([{ role: "error", text: String((err as Error).message) }]);
    } finally {
      setBusy(false);
    }
  }

  async function handleSend(e: FormEvent) {
    e.preventDefault();
    if (!site || !prompt.trim()) return;
    const message = prompt.trim();
    setPrompt("");
    setMessages((m) => [...m, { role: "user", text: message }]);
    setBusy(true);
    try {
      const { reply, site: updated } = await sendPrompt(site.id, message);
      setSite(updated);
      setPreviewKey((k) => k + 1);
      setMessages((m) => [...m, { role: "assistant", text: reply }]);
    } catch (err) {
      setMessages((m) => [...m, { role: "error", text: String((err as Error).message) }]);
    } finally {
      setBusy(false);
    }
  }

  if (!site) {
    return (
      <main className="start-screen">
        <form className="start-card" onSubmit={handleStart}>
          <h1>WebBuilder</h1>
          <p>Bouw je eigen website door gewoon te typen wat je wilt.</p>
          <input
            value={siteName}
            onChange={(e) => setSiteName(e.target.value)}
            placeholder="Naam van je website"
          />
          <button className="start-button" disabled={busy} type="submit">
            {busy ? "Bezig..." : "Website aanmaken"}
          </button>
          {messages.map((m, i) => (
            <p key={i} className="msg error">{m.text}</p>
          ))}
        </form>
      </main>
    );
  }

  return (
    <main className="layout">
      <aside className="sidebar">
        <div className="header">
          <h1>{site.name}</h1>
          <p>Versie {site.version} · pas alles aan met één zin</p>
        </div>
        <div className="messages">
          {messages.map((m, i) => (
            <div key={i} className={`msg ${m.role}`}>{m.text}</div>
          ))}
          <div ref={bottomRef} />
        </div>
        <form className="composer" onSubmit={handleSend}>
          <input
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="bijv. maak de hero speels en voeg een galerij toe"
            disabled={busy}
          />
          <button disabled={busy || !prompt.trim()} type="submit">
            {busy ? "..." : "Stuur"}
          </button>
        </form>
      </aside>
      <section className="preview">
        <div className="preview-bar">
          <span>Live preview</span>
          <span>{site.blocks.length} secties</span>
        </div>
        <iframe key={previewKey} src={renderUrl(site.id)} title="Website preview" />
      </section>
    </main>
  );
}
