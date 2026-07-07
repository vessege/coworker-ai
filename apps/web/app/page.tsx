"use client";

import { useEffect, useMemo, useState } from "react";
import {
  ask,
  generate,
  listAssets,
  listModels,
  type AskResponse,
  type GenerateResponse,
  type AssetCard,
  type ModelInfo,
  type SourceRef,
} from "@/lib/api";

type Mode = "ask" | "generate";
type View = "home" | "result";

const EXAMPLES: Record<Mode, string[]> = {
  ask: [
    "QQS hisobotini qachon topshiraman?",
    "Aylanma soliq stavkasi qancha?",
    "Hisobotni kechiktirsam qancha jarima?",
  ],
  generate: [
    "Schyot-faktura tayyorla: sotuvchi OOO Alfa, STIR 300123456",
    "Bajarilgan ishlar dalolatnomasini tayyorla",
  ],
};

const TAB_FILTERS: { label: string; test: (a: AssetCard) => boolean }[] = [
  { label: "Hammasi", test: () => true },
  { label: "Soliq", test: (a) => /soliq|tax|QQS|FAQ/i.test(a.title + a.type) && a.type !== "TEMPLATE" },
  { label: "Shablonlar", test: (a) => a.type === "TEMPLATE" },
  { label: "Jarayonlar", test: (a) => a.type === "SOP" || a.type === "WORKFLOW" },
  { label: "Qarorlar", test: (a) => a.type === "DECISION" || a.type === "RULE" },
  { label: "Lug'at", test: (a) => a.type === "FACT" && /glossary|lug|term/i.test(a.title) },
];

const TYPE_COLORS: Record<string, string> = {
  FACT: "linear-gradient(135deg,#6366f1,#22d3ee)",
  FAQ: "linear-gradient(135deg,#0ea5e9,#38bdf8)",
  TEMPLATE: "linear-gradient(135deg,#10b981,#34d399)",
  SOP: "linear-gradient(135deg,#f59e0b,#fbbf24)",
  WORKFLOW: "linear-gradient(135deg,#f59e0b,#f97316)",
  DECISION: "linear-gradient(135deg,#8b5cf6,#a78bfa)",
  RULE: "linear-gradient(135deg,#ec4899,#f472b6)",
};

function greeting(): string {
  const h = new Date().getHours();
  if (h < 6) return "Xayrli tun";
  if (h < 12) return "Xayrli tong";
  if (h < 18) return "Xayrli kun";
  return "Xayrli kech";
}

function Sources({ sources }: { sources: SourceRef[] }) {
  if (!sources?.length) return null;
  return (
    <>
      {sources.map((s) => (
        <div className="src-card" key={s.id}>
          <div className="sid">{s.id}</div>
          {s.source_url && (
            <div className="sm">
              <a href={s.source_url} target="_blank" rel="noreferrer">{s.source_url}</a>
            </div>
          )}
          {s.verified && <div className="src-meta">Tekshirilgan: {s.verified}</div>}
        </div>
      ))}
    </>
  );
}

export default function Home() {
  const [view, setView] = useState<View>("home");
  const [mode, setMode] = useState<Mode>("ask");
  const [input, setInput] = useState("");
  const [submitted, setSubmitted] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [askRes, setAskRes] = useState<AskResponse | null>(null);
  const [genRes, setGenRes] = useState<GenerateResponse | null>(null);
  const [assets, setAssets] = useState<AssetCard[]>([]);
  const [tab, setTab] = useState(0);
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [model, setModel] = useState<string>("");
  const [modelMenu, setModelMenu] = useState(false);

  useEffect(() => {
    listAssets().then(setAssets).catch(() => {});
    listModels()
      .then((ms) => {
        setModels(ms);
        setModel(ms.find((m) => m.default)?.id ?? ms[0]?.id ?? "");
      })
      .catch(() => {});
  }, []);

  const modelLabel = models.find((m) => m.id === model)?.label ?? "Claude";

  const visible = useMemo(
    () => assets.filter(TAB_FILTERS[tab].test),
    [assets, tab]
  );

  async function submit(text?: string) {
    const q = (text ?? input).trim();
    if (q.length < 2) return;
    setSubmitted(q);
    setLoading(true);
    setError("");
    setAskRes(null);
    setGenRes(null);
    setView("result");
    try {
      if (mode === "ask") setAskRes(await ask(q, model));
      else setGenRes(await generate(q, model));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Xatolik yuz berdi");
    } finally {
      setLoading(false);
    }
  }

  function useAsset(a: AssetCard) {
    if (a.type === "TEMPLATE") {
      setMode("generate");
      submit(`${a.title.split("/")[0].trim()} tayyorla`);
    } else {
      setMode("ask");
      submit(a.title.split("/")[0].trim());
    }
  }

  const rail = (
    <div className="rail">
      <div className="orb" title="CoWorker AI" />
      <button className="rail-btn" title="Yangi" onClick={() => { setView("home"); setInput(""); }}>＋</button>
      <button className={"rail-btn" + (view === "home" ? " active" : "")} title="Bosh sahifa" onClick={() => setView("home")}>🏠</button>
      <button className="rail-btn" title="Bilimlar bazasi" onClick={() => setView("home")}>📚</button>
      <div className="rail-spacer" />
      <div className="avatar">CK</div>
    </div>
  );

  return (
    <div className="app">
      {rail}
      <div className="main">
        <div className="topbar">
          <span className="brandmark">CoWorker AI</span>
          <span className="pill">🟢 Buxgalter · Claude</span>
        </div>

        {view === "home" ? (
          <div className="content">
            <div className="home">
              <div className="hero">
                <div className="orb-lg" />
                <h1>{greeting()}!</h1>
                <p>Buxgalter uchun AI hamkasb — har javob manba bilan.</p>
              </div>

              <div className="composer">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder={mode === "ask" ? "Soliq bo'yicha savolingizni yozing…" : "Qanday hujjat kerak? (masalan: schyot-faktura)"}
                  rows={2}
                  onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); submit(); } }}
                />
                <div className="composer-row">
                  <div className="modes">
                    <button className={"mode" + (mode === "ask" ? " active" : "")} onClick={() => setMode("ask")}>Savol</button>
                    <button className={"mode" + (mode === "generate" ? " active" : "")} onClick={() => setMode("generate")}>Hujjat</button>
                  </div>
                  <div className="composer-right">
                    <div className="model-select">
                      <button className="pill" onClick={() => setModelMenu((v) => !v)}>
                        {modelLabel} <span style={{ opacity: 0.6 }}>▾</span>
                      </button>
                      {modelMenu && (
                        <div className="model-menu">
                          {models.map((m) => (
                            <button
                              key={m.id}
                              className={"model-item" + (m.id === model ? " sel" : "")}
                              disabled={!m.available}
                              onClick={() => { setModel(m.id); setModelMenu(false); }}
                            >
                              <span>{m.label}</span>
                              <span className="model-tag">
                                {m.id === model ? "✓" : m.available ? m.provider : "kalit yo'q"}
                              </span>
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                    <button className="send" onClick={() => submit()} disabled={loading}>↑</button>
                  </div>
                </div>
              </div>

              <div className="examples">
                {EXAMPLES[mode].map((ex) => (
                  <button key={ex} className="ex" onClick={() => { setInput(ex); submit(ex); }}>{ex}</button>
                ))}
              </div>

              <div className="tabs">
                {TAB_FILTERS.map((t, i) => (
                  <button key={t.label} className={"tab" + (tab === i ? " active" : "")} onClick={() => setTab(i)}>{t.label}</button>
                ))}
              </div>

              <div className="gallery">
                {visible.map((a) => (
                  <button className="card" key={a.id} onClick={() => useAsset(a)}>
                    <div className="thumb" style={{ background: TYPE_COLORS[a.type] || "linear-gradient(135deg,#64748b,#94a3b8)" }}>
                      {a.type === "TEMPLATE" ? "📄" : a.type === "SOP" ? "⚙️" : a.type === "DECISION" ? "🔀" : a.type === "FAQ" ? "❓" : "📘"}
                    </div>
                    <span className="badge-type">{a.type}</span>
                    <div className="ctitle">{a.title.split("/")[0].trim()}</div>
                    <div className="csum">{a.summary}</div>
                  </button>
                ))}
              </div>
              <div className="foot">
                {assets.length} ta bilim aktivi · Axborot xarakterida, rasmiy soliq maslahati emas.
              </div>
            </div>
          </div>
        ) : (
          <div className="content">
            <div className="workspace">
              <div className="chat">
                <div className="thread">
                  <button className="linkback" onClick={() => setView("home")}>← Bosh sahifa</button>
                  <div className="qbubble">{submitted}</div>
                  {loading && <p className="csum">Javob tayyorlanmoqda…</p>}
                  {error && <div className="error">{error}</div>}
                  {askRes && (
                    <div>
                      <div className={askRes.grounded ? "badge ok" : "badge warn"}>
                        {askRes.grounded ? "Manbaga asoslangan" : "Bazada topilmadi"}
                      </div>
                      <div className="answer">{askRes.answer}</div>
                    </div>
                  )}
                  {genRes && (
                    <div>
                      <div className={genRes.grounded ? "badge ok" : "badge warn"}>
                        {genRes.template ? `Shablon: ${genRes.template}` : "Shablon topilmadi"}
                      </div>
                      <pre className="document">{genRes.document}</pre>
                    </div>
                  )}
                </div>
              </div>
              <aside className="panel">
                <h3>Manbalar</h3>
                {askRes && <Sources sources={askRes.sources} />}
                {genRes?.source && <Sources sources={[genRes.source]} />}
                {!askRes?.sources?.length && !genRes?.source && !loading && (
                  <p className="csum">Manba yo'q.</p>
                )}
              </aside>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
