"use client";

import { useEffect, useRef, useState } from "react";
import {
  ask,
  generate,
  listModels,
  listTasks,
  me,
  uploadDocument,
  type ModelInfo,
  type SourceRef,
  type TaskInfo,
  type TenantInfo,
} from "@/lib/api";

type Mode = "ask" | "generate";
type View = "dashboard" | "picker";

const OPEN_STATUSES = new Set(["Created", "Planned", "Running", "Waiting", "Review"]);

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

function coworkerFor(role: string): Coworker {
  return COWORKERS.find((c) => c.id === role) ?? COWORKERS[COWORKERS.length - 1];
}

const STATUS_LABEL: Record<string, string> = {
  Created: "Yangi", Planned: "Rejalashtirilgan", Running: "Jarayonda",
  Waiting: "Kutilmoqda", Review: "Ko'rib chiqilmoqda", Completed: "Bajarildi",
  Archived: "Arxivlangan", Cancelled: "Bekor qilingan",
};

function timeAgo(iso: string): string {
  const diffMin = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 60000));
  if (diffMin < 1) return "hozir";
  if (diffMin < 60) return `${diffMin} daq oldin`;
  const h = Math.round(diffMin / 60);
  if (h < 24) return `${h} soat oldin`;
  return `${Math.round(h / 24)} kun oldin`;
}

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
  const [view, setView] = useState<View>("dashboard");
  const [cw, setCw] = useState<Coworker | null>(null);
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [mode, setMode] = useState<Mode>("ask");
  const [loading, setLoading] = useState(false);
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [model, setModel] = useState("");
  const [menu, setMenu] = useState(false);
  const [tenant, setTenant] = useState<TenantInfo | null>(null);
  const [tasks, setTasks] = useState<TaskInfo[]>([]);
  const [uploadOpen, setUploadOpen] = useState(false);
  const [uploadName, setUploadName] = useState("");
  const [uploadBody, setUploadBody] = useState("");
  const [uploadMsg, setUploadMsg] = useState("");
  const pendingMode = useRef<Mode>("ask");
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    listModels().then((ms) => {
      setModels(ms);
      setModel(ms.find((m) => m.default)?.id ?? ms[0]?.id ?? "");
    }).catch(() => {});
    me().then(setTenant).catch(() => {});
    listTasks().then(setTasks).catch(() => {});
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const modelLabel = models.find((m) => m.id === model)?.label ?? "Claude";

  function refreshTasks() {
    listTasks().then(setTasks).catch(() => {});
    me().then(setTenant).catch(() => {});
  }

  function openChat(c: Coworker) {
    setCw(c);
    setMode(pendingMode.current);
    pendingMode.current = "ask";
    setMessages([{
      who: "ai",
      text: `Salom! Men ${c.name} — sizning ${c.title.toLowerCase()}ingizman. ${c.desc} Savolingizni yozing yoki hujjat so'rang.`,
    }]);
  }

  function askAI() { pendingMode.current = "ask"; setView("picker"); }
  function generateDoc() { pendingMode.current = "generate"; setView("picker"); }

  async function submitUpload() {
    if (uploadName.trim().length < 2 || uploadBody.trim().length < 10) return;
    try {
      await uploadDocument(uploadName.trim(), uploadBody.trim());
      setUploadMsg(`"${uploadName.trim()}" yuklandi.`);
      setUploadName(""); setUploadBody(""); setUploadOpen(false);
    } catch (e) {
      setUploadMsg(e instanceof Error ? e.message : "Yuklashda xatolik.");
    }
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

  /* ---------- HOME: Dashboard or Coworker Picker ---------- */
  if (!cw) {
    const openTasks = tasks.filter((t) => OPEN_STATUSES.has(t.status))
      .sort((a, b) => b.updated_at.localeCompare(a.updated_at));
    const recent = [...tasks].sort((a, b) => b.created_at.localeCompare(a.created_at)).slice(0, 6);
    const counts = tasks.reduce<Record<string, number>>((acc, t) => {
      acc[t.status] = (acc[t.status] ?? 0) + 1;
      return acc;
    }, {});

    return (
      <div className="app">
        <div className="main">
          <div className="topbar">
            <div className="tb-left">
              <span className="brandmark">🟣 CoWorker AI</span>
              {view === "picker" && (
                <button className="pill" onClick={() => setView("dashboard")}>🏠 Bosh sahifa</button>
              )}
            </div>
            <div className="tb-right">
              {tenant && (
                <span className="pill" title="Kredit sarfi">
                  💳 {tenant.remaining < 0 ? "cheksiz" : `${tenant.remaining} qoldi`}
                </span>
              )}
              <button className="pill" onClick={askAI}>🔎 Qidirish</button>
            </div>
          </div>

          <div className="content">
            {view === "picker" ? (
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
            ) : (
              <div className="dash">
                <div className="dash-grid">
                  <div className="dash-main">
                    <div className="widget greet">
                      <div className="greet-orb" />
                      <div>
                        <div className="greet-h">{greeting()}!</div>
                        <div className="greet-p">
                          {openTasks.length > 0
                            ? `Bugun ${openTasks.length} ta ish diqqatingizni kutmoqda.`
                            : "Barcha ishlar bajarilgan — yangi savol bering."}
                        </div>
                      </div>
                    </div>

                    <div className="widget">
                      <div className="widget-h">Diqqat talab qiladi</div>
                      {openTasks.length === 0 ? (
                        <div className="empty">Hozircha ochiq ish yo'q ✓</div>
                      ) : (
                        <div className="focus-list">
                          {openTasks.slice(0, 5).map((t) => {
                            const c = coworkerFor(t.role);
                            return (
                              <div key={t.id} className="focus-item">
                                <div className="focus-ico" style={{ background: c.grad }}>{c.emoji}</div>
                                <div className="focus-body">
                                  <div className="focus-title">{t.title}</div>
                                  <div className="focus-sub">{c.title} · {STATUS_LABEL[t.status] ?? t.status}</div>
                                </div>
                                <div className="focus-time">{timeAgo(t.updated_at)}</div>
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>

                    <div className="widget">
                      <div className="widget-h">So'nggi AI faoliyati</div>
                      {recent.length === 0 ? (
                        <div className="empty">Hali AI faoliyati yo'q — birinchi savolni bering.</div>
                      ) : (
                        <div className="focus-list">
                          {recent.map((t) => {
                            const c = coworkerFor(t.role);
                            return (
                              <div key={t.id} className="focus-item">
                                <div className="focus-ico" style={{ background: c.grad }}>{c.emoji}</div>
                                <div className="focus-body">
                                  <div className="focus-title">{t.title}</div>
                                  <div className="focus-sub">{c.name} · {STATUS_LABEL[t.status] ?? t.status}</div>
                                </div>
                                <div className="focus-time">{timeAgo(t.created_at)}</div>
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>

                    {tasks.length > 0 && (
                      <div className="widget">
                        <div className="widget-h">Tasklar holati</div>
                        <div className="stat-row">
                          {Object.entries(counts).map(([status, n]) => (
                            <div key={status} className="stat">
                              <div className="stat-n">{n}</div>
                              <div className="stat-l">{STATUS_LABEL[status] ?? status}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    <div className="widget">
                      <div className="widget-h">Tezkor amallar</div>
                      <div className="qa-row">
                        <button className="qa-btn" onClick={askAI}>💬 AI'dan so'rash</button>
                        <button className="qa-btn" onClick={generateDoc}>📄 Hujjat yaratish</button>
                        <button className="qa-btn" onClick={() => setUploadOpen((v) => !v)}>📤 Hujjat yuklash</button>
                        <button className="qa-btn" onClick={askAI}>🔎 Bilim bazasidan qidirish</button>
                      </div>
                      {uploadOpen && (
                        <div className="upload-box">
                          <input className="upload-input" placeholder="Fayl nomi (masalan: shartnoma.md)"
                            value={uploadName} onChange={(e) => setUploadName(e.target.value)} />
                          <textarea className="upload-input" placeholder="Hujjat matni…" rows={4}
                            value={uploadBody} onChange={(e) => setUploadBody(e.target.value)} />
                          <button className="qa-btn primary" onClick={submitUpload}>Yuklash</button>
                        </div>
                      )}
                      {uploadMsg && <div className="upload-msg">{uploadMsg}</div>}
                    </div>
                  </div>

                  <div className="dash-rail">
                    <div className="widget">
                      <div className="widget-h">Sevimli hamkasblar</div>
                      <div className="rail-cw">
                        {COWORKERS.map((c) => (
                          <button key={c.title} className="rail-cw-item" onClick={() => openChat(c)}>
                            <div className="cw-avatar sm" style={{ background: c.grad }}>{c.emoji}</div>
                            <div>
                              <div className="rail-cw-name">{c.name}</div>
                              <div className="rail-cw-title">{c.title}</div>
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
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
            <button className="back" onClick={() => { setCw(null); setMessages([]); setView("dashboard"); refreshTasks(); }}>←</button>
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
