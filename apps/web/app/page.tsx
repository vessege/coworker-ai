"use client";

import { useState } from "react";
import {
  ask,
  generate,
  type AskResponse,
  type GenerateResponse,
  type SourceRef,
} from "@/lib/api";

type Tab = "ask" | "generate";

const ASK_EXAMPLES = [
  "QQS hisobotini qachon topshiraman?",
  "Aylanma soliq stavkasi qancha?",
  "Ijtimoiy badallarni qachon to'layman?",
];
const GEN_EXAMPLES = [
  "Schyot-faktura tayyorla: sotuvchi OOO Alfa, STIR 300123456, xaridor OOO Beta",
  "Bajarilgan ishlar dalolatnomasini tayyorla",
];

function Sources({ sources }: { sources: SourceRef[] }) {
  if (!sources?.length) return null;
  return (
    <div className="sources">
      <span className="sources-label">Manbalar:</span>
      {sources.map((s) => (
        <span key={s.id} className="source-chip">
          {s.source_url ? (
            <a href={s.source_url} target="_blank" rel="noreferrer">
              {s.id}
            </a>
          ) : (
            s.id
          )}
          {s.verified && <em> · {s.verified}</em>}
        </span>
      ))}
    </div>
  );
}

export default function Home() {
  const [tab, setTab] = useState<Tab>("ask");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [askRes, setAskRes] = useState<AskResponse | null>(null);
  const [genRes, setGenRes] = useState<GenerateResponse | null>(null);

  async function submit() {
    if (input.trim().length < 2) return;
    setLoading(true);
    setError("");
    try {
      if (tab === "ask") {
        setGenRes(null);
        setAskRes(await ask(input));
      } else {
        setAskRes(null);
        setGenRes(await generate(input));
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Xatolik yuz berdi");
    } finally {
      setLoading(false);
    }
  }

  const examples = tab === "ask" ? ASK_EXAMPLES : GEN_EXAMPLES;

  return (
    <main className="wrap">
      <header className="head">
        <div className="logo">CoWorker AI</div>
        <p className="tagline">Buxgalter uchun AI hamkasb — har javob manba bilan</p>
      </header>

      <div className="tabs">
        <button
          className={tab === "ask" ? "tab active" : "tab"}
          onClick={() => setTab("ask")}
        >
          Savol berish
        </button>
        <button
          className={tab === "generate" ? "tab active" : "tab"}
          onClick={() => setTab("generate")}
        >
          Hujjat tayyorlash
        </button>
      </div>

      <div className="card">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={
            tab === "ask"
              ? "Soliq muddati bo'yicha savolingiz..."
              : "Qanday hujjat kerak? (masalan: schyot-faktura)"
          }
          rows={3}
          onKeyDown={(e) => {
            if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) submit();
          }}
        />
        <div className="row">
          <div className="examples">
            {examples.map((ex) => (
              <button key={ex} className="ex" onClick={() => setInput(ex)}>
                {ex.length > 42 ? ex.slice(0, 42) + "…" : ex}
              </button>
            ))}
          </div>
          <button className="submit" onClick={submit} disabled={loading}>
            {loading ? "..." : tab === "ask" ? "So'rash" : "Tayyorlash"}
          </button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {askRes && (
        <div className="result">
          <div className={askRes.grounded ? "badge ok" : "badge warn"}>
            {askRes.grounded ? "Manbaga asoslangan" : "Bazada topilmadi"}
          </div>
          <div className="answer">{askRes.answer}</div>
          <Sources sources={askRes.sources} />
        </div>
      )}

      {genRes && (
        <div className="result">
          <div className={genRes.grounded ? "badge ok" : "badge warn"}>
            {genRes.template ? `Shablon: ${genRes.template}` : "Shablon topilmadi"}
          </div>
          <pre className="document">{genRes.document}</pre>
          {genRes.source && <Sources sources={[genRes.source]} />}
        </div>
      )}

      <footer className="foot">
        Axborot xarakterida — rasmiy soliq maslahati emas. Aniq holatni soliq.uz
        yoki buxgalteringiz bilan tasdiqlang.
      </footer>
    </main>
  );
}
