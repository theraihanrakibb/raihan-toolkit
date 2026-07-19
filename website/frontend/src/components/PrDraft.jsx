import { useState } from "react";
import { api } from "../api.js";

export default function PrDraft() {
  const [diff, setDiff] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const run = async () => {
    if (!diff.trim()) { setError("Paste a git diff first."); return; }
    setLoading(true); setError(""); setResult(null);
    try {
      setResult(await api.prDraft(diff));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Generate a commit / PR description</h2>
      <p style={{ color: "var(--muted)", marginTop: 0 }}>
        Paste <code>git diff --cached</code> output. Get a Conventional Commit message, PR description, and changelog entry.
      </p>

      <label>git diff</label>
      <textarea value={diff} onChange={(e) => setDiff(e.target.value)} placeholder="diff --git a/foo.py b/foo.py&#10;index abc..def 100644&#10;--- a/foo.py&#10;+++ b/foo.py" style={{ minHeight: 200 }} />

      <button className="primary" onClick={run} disabled={loading}>
        {loading ? "Generating…" : "Draft commit + PR"}
      </button>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result">
          <h3>Commit message</h3>
          <pre>{result.commit_message}</pre>

          <h3>PR description</h3>
          <pre>{result.pr_description}</pre>

          <h3>Changelog entry</h3>
          <pre>{result.changelog_entry}</pre>

          <p style={{ color: "var(--muted)", fontSize: "0.85rem" }}>
            {result.files.length} file(s) · +{result.additions} / -{result.deletions}
          </p>
        </div>
      )}
    </div>
  );
}
