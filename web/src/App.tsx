import { useEffect, useState } from "react";

type HealthStatus = "loading" | "ok" | "error";

export default function App() {
  const [status, setStatus] = useState<HealthStatus>("loading");

  useEffect(() => {
    fetch("/api/health/")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json() as Promise<{ status: string }>;
      })
      .then((data) => {
        setStatus(data.status === "ok" ? "ok" : "error");
      })
      .catch(() => {
        setStatus("error");
      });
  }, []);

  const label: Record<HealthStatus, string> = {
    loading: "Vérification en cours…",
    ok: "✅ API opérationnelle",
    error: "❌ API inaccessible",
  };

  return (
    <main style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>SecOnDemand</h1>
      <p>
        <strong>Statut de l'API :</strong> {label[status]}
      </p>
    </main>
  );
}
