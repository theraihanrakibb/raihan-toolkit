import { useState } from "react";
import { api } from "../api.js";

export default function Apply() {
  const [jd, setJd] = useState("");
  const [resume, setResume] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const run = async () => {
    if (!jd.trim() || !resume.trim()) { setError("Paste both the JD and your resume."); return; }
    setLoading(true); setError(""); setResult(null);
    try {
      setResult(await api.apply(jd, resume));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Tailor a job application</h2>
      <p style={{ color: "var(--muted)", marginTop: 0 }}>
        Paste a job description and your resume. Get a cover letter, interview questions, skills-gap analysis, and a 7-day prep plan.
      </p>

      <label>Job description</label>
      <textarea value={jd} onChange={(e) => setJd(e.target.value)} placeholder="We're hiring a Senior Engineer to join our team at Acme Corp..." style={{ minHeight: 140 }} />

      <label>Resume (paste text)</label>
      <textarea value={resume} onChange={(e) => setResume(e.target.value)} placeholder="MD RAKIBUL ISLAM RAIHAN&#10;AI Infrastructure Engineer..." style={{ minHeight: 140 }} />

      <button className="primary" onClick={run} disabled={loading}>
        {loading ? "Tailoring…" : "Generate application pack"}
      </button>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result">
          <h3>Cover letter — {result.company} / {result.role}</h3>
          <pre>{result.cover_letter}</pre>

          <h3>Matched keywords ({result.matched_keywords.length})</h3>
          <p style={{ color: "var(--accent-2)", fontSize: "0.85rem" }}>{result.matched_keywords.join(", ")}</p>

          <h3>Skills gap ({result.missing_keywords.length})</h3>
          <ul>{result.skills_gap.map((s, i) => <li key={i} style={{ fontSize: "0.85rem" }}>{s.skill} — <em>{s.status}</em></li>)}</ul>

          <h3>Likely interview questions ({result.interview_questions.length})</h3>
          <ol>{result.interview_questions.map((q, i) => <li key={i} style={{ fontSize: "0.9rem" }}>{q}</li>)}</ol>

          <h3>7-day prep plan</h3>
          <ul>{result.prep_plan.map((p, i) => <li key={i} style={{ fontSize: "0.9rem" }}><strong>Day {i + 1}.</strong> {p.replace(/^Day \d+: /, "")}</li>)}</ul>
        </div>
      )}
    </div>
  );
}
