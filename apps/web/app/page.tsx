"use client";

import { useEffect, useRef, useState } from "react";
import {
  ask,
  generate,
  listModels,
  type ModelInfo,
  type SourceRef,
} from "@/lib/api";

type Mode = "ask" | "generate";

interface Coworker {
  id: string;        // API role value ("" = general)
  name: string;
  title: string;
  emoji: string;
  grad: string;
  desc: string;
  examples: string[];
}

const COWORKERS: Coworker[] = [
  {
    id: "Accountant", name: "Aziza", title: "Buxgalter", emoji: "🧮",
    grad: "linear-gradient(135deg,#10b981,#34d399)",
    desc: "Soliq muddatlari, stavkalar, schyot-faktura va hisobot savollari.",
    examples: ["QQS hisobotini qachon topshiraman?", "YaTT qancha soliq to'laydi?", "Schyot-faktura tayyorla"],
  },
  {
    id: "HR", name: "Malika", title: "HR mutaxassis", emoji: "👥",
    grad: "linear-gradient(135deg,#8b5cf6,#a78bfa)",
    desc: "Ishga qabul, mehnat shartnomasi, ta'til va Mehnat kodeksi savollari.",
    examples: ["Sinov muddati qancha bo'lishi mumkin?", "Yillik ta'til necha kun?", "Ishga qabul buyrug'ini tayyorla"],
  },
  {
    id: "Office Manager", name: "Jasur", title: "Ofis-menejer", emoji: "🗂️",
    grad: "linear-gradient(135deg,#f59e0b,#fbbf24)",
    desc: "Hujjat aylanishi, rasmiy xatlar, ma'lumotnoma va ish yuritish.",
    examples: ["Kiruvchi hujjatni qanday ro'yxatga olaman?", "Rasmiy xat yozib ber", "Ish joyidan ma'lumotnoma tayyorla"],
  },
  {
    id: "", name: "CoWorker", title: "Umumiy yordamchi", emoji: "✨",
    grad: "linear-gradient(135deg,#6366f1,#22d3ee)",
    desc: "Istalgan mavzuda — butun bilimlar bazasi bo'yicha javob beradi.",
    examples: ["Qaysi soliq rejimini tanlashim kerak?", "Xodim ishdan chiqsa nima qilaman?", "Xizmat shartnomasini tayyorla"],
  },
];

interface Msg {
  who: "user" | "ai";
  text: string;
  doc?: boolean;          // render as document block
  sources?: SourceRef[];
  grounded?: boolean;
}

function greeting(): string {
  const h = new Date().getHours();
  if (h < 6) return "Xayrli tun";
  if (h < 12) return "Xayrli tong";
  if (h < 18) return "Xayrli kun";
  return "Xayrli kech";
}

export default function Home() {
  const [cw, setCw] = useState<Coworker | null>(null);
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [mode, setMode] = useState<Mode>("ask");
  const [loading, setLoading] = useState(false);
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [model, setModel] = useState("");
  const [menu, setMenu] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    listModels().then((ms) => {
      setModels(ms);
      setModel(ms.find((m) => m.default)?.id ?? ms[0]?.id ?? "");
    }).catch(() => {});
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const modelLabel = models.find((m) => m.id === model)?.label ?? "Claude";

  function openChat(c: Coworker) {
    setCw(c);
    setMessages([{
      who: "ai",
      text: `Salom! Men ${c.name} — sizning ${c.title.toLowerCase()}ingizman. ${c.desc} Savolingizni yozing yoki hujjat so'rang.`,
    }]);
  }

  async function send(text?: string) {
    const q = (text ?? input).trim();
    if (q.length < 2 || loading || !cw) return;
    setInput("");
    setMessages((m) => [...m, { who: "user", text: q }]);
    setLoading(true);
    try {
      if (mode === "ask") {
        const r = await ask(q, model, cw.id || undefined);
        setMessages((m) => [...m, { who: "ai", text: r.answer, sources: r.sources, grounded: r.grounded }]);
      } else {
        const r = await generate(q, model);
        setMessages((m) => [...m, {
          who: "ai", text: r.document, doc: true, grounded: r.grounded,
          sources: r.source ? [r.source] : [],
        }]);
      }
    } catch (e) {
      setMessages((m) => [...m, { who: "ai", text: e instanceof Error ? e.message : "Xatolik yuz berdi." }]);
    } finally {
      setLoading(false);
    }
  }

  /* ---------- HOME: coworker picker ---------- */
  if (!cw) {
    return (
      <div className="app">
        <div className="main">
          <div className="topbar">
            <span className="brandmark">🟣 CoWorker AI</span>
            <span className="pill">Biznesingiz uchun AI jamoa</span>
          </div>
          <div className="content">
            <div className="home">
              <div className="hero">
                <div className="orb-lg" />
                <h1>{greeting()}!</h1>
                <p>Bugun qaysi hamkasbingiz yordam bersin?</p>
              </div>
              <div className="cw-grid">
                {COWORKERS.map((c) => (
                  <button key={c.title} className="cw-card" onClick={() => openChat(c)}>
                    <div className="cw-avatar" style={{ background: c.grad }}>{c.emoji}</div>
                    <div className="cw-name">{c.name}</div>
                    <div className="cw-title">{c.title}</div>
                    <div className="cw-desc">{c.desc}</div>
                    <div className="cw-cta">Suhbatni boshlash →</div>
                  </button>
                ))}
              </div>
              <div className="foot">
                30+ manbali bilim aktivi · Har javob manba bilan · Axborot xarakterida, rasmiy maslahat emas
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  /* ---------- CHAT ---------- */
  return (
    <div className="app">
      <div className="main chatmode">
        <div className="topbar">
          <div className="tb-left">
            <button className="back" onClick={() => { setCw(null); setMessages([]); }}>←</button>
            <div className="cw-mini" style={{ background: cw.grad }}>{cw.emoji}</div>
            <div>
              <div className="tb-name">{cw.name} · {cw.title}</div>
              <div className="tb-sub">{loading ? "yozmoqda…" : "onlayn"}</div>
            </div>
          </div>
          <div className="tb-right">
            <div className="model-select">
              <button className="pill" onClick={() => setMenu((v) => !v)}>{modelLabel} ▾</button>
              {menu && (
                <div className="model-menu">
                  {models.map((m) => (
                    <button key={m.id} disabled={!m.available}
                      className={"model-item" + (m.id === model ? " sel" : "")}
                      onClick={() => { setModel(m.id); setMenu(false); }}>
                      <span>{m.label}</span>
                      <span className="model-tag">{m.id === model ? "✓" : m.available ? m.provider : "kalit yo'q"}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
            <button className="pill" onClick={() => openChat(cw)}>＋ Yangi</button>
          </div>
        </div>

        <div className="thread-wrap">
          <div className="thread-inner">
            {messages.map((m, i) => (
              <div key={i} className={`msg ${m.who}`}>
                {m.who === "ai" && <div className="msg-avatar" style={{ background: cw.grad }}>{cw.emoji}</div>}
                <div className="bubble-col">
                  {m.doc
                    ? <pre className="bubble doc">{m.text}</pre>
                    : <div className={`bubble ${m.who}`}>{m.text}</div>}
                  {m.sources && m.sources.length > 0 && (
                    <div className="src-chips">
                      {m.sources.map((s) => (
                        <a key={s.id} className="chip" href={s.source_url || "#"} target="_blank" rel="noreferrer"
                           title={s.verified ? `Tekshirilgan: ${s.verified}` : ""}>
                          📎 {s.id}
                        </a>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="msg ai">
                <div className="msg-avatar" style={{ background: cw.grad }}>{cw.emoji}</div>
                <div className="bubble ai typing"><span/><span/><span/></div>
              </div>
            )}
            {messages.length <= 1 && (
              <div className="starter">
                {cw.examples.map((ex) => (
                  <button key={ex} className="ex" onClick={() => send(ex)}>{ex}</button>
                ))}
              </div>
            )}
            <div ref={endRef} />
          </div>
        </div>

        <div className="composer-bar">
          <div className="composer-inner">
            <div className="modes">
              <button className={"mode" + (mode === "ask" ? " active" : "")} onClick={() => setMode("ask")}>💬 Savol</button>
              <button className={"mode" + (mode === "generate" ? " active" : "")} onClick={() => setMode("generate")}>📄 Hujjat</button>
            </div>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={mode === "ask" ? `${cw.name}ga savol yozing…` : "Qanday hujjat kerak?"}
              rows={1}
              onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
            />
            <button className="send" onClick={() => send()} disabled={loading}>➤</button>
          </div>
        </div>
      </div>
    </div>
  );
}
