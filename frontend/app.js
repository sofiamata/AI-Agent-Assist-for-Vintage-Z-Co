const API_BASE = "http://localhost:8000";

const msgEl = document.getElementById("msg");
const runBtn = document.getElementById("runBtn");
const clearBtn = document.getElementById("clearBtn");

const statusEl = document.getElementById("status");
const intentEl = document.getElementById("intent");
const replyEl = document.getElementById("reply");
const summaryEl = document.getElementById("summary");
const actionsEl = document.getElementById("actions");
const inventoryEl = document.getElementById("inventory");

function setStatus(text, isError=false) {
  statusEl.textContent = text;
  statusEl.className = "status " + (isError ? "error" : "");
}

function renderInventory(items) {
  if (!items || items.length === 0) {
    inventoryEl.textContent = "No matches. (Try adding more mock inventory in backend/inventory.py)";
    inventoryEl.className = "muted";
    return;
  }

  const rows = items.map(it => {
    const stock = it.in_stock ? "✅ In stock" : "❌ Out of stock";
    const side = it.side ? ` • ${it.side}` : "";
    return `
      <div class="inv-row">
        <div class="inv-top">
          <span class="mono">${it.sku}</span>
          <span class="pill">${stock}</span>
        </div>
        <div>${it.part} • ${it.model}${side} • <strong>$${it.price}</strong></div>
      </div>
    `;
  }).join("");

  inventoryEl.className = "";
  inventoryEl.innerHTML = rows;
}

function renderActions(actions) {
  actionsEl.innerHTML = "";
  if (!actions || actions.length === 0) {
    const li = document.createElement("li");
    li.textContent = "—";
    actionsEl.appendChild(li);
    actionsEl.className = "muted";
    return;
  }
  actionsEl.className = "";
  actions.forEach(a => {
    const li = document.createElement("li");
    li.textContent = a;
    actionsEl.appendChild(li);
  });
}

runBtn.addEventListener("click", async () => {
  const customer_message = msgEl.value.trim();
  if (!customer_message) {
    setStatus("Please paste a customer message first.", true);
    return;
  }

  setStatus("Running workflow…");
  runBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/agent-assist`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ customer_message })
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(errText || `HTTP ${res.status}`);
    }

    const data = await res.json();

    intentEl.textContent = data.intent || "general";
    intentEl.className = "mono";
    replyEl.textContent = data.draft_reply || "";
    replyEl.className = "pre";
    summaryEl.textContent = data.summary || "";
    summaryEl.className = "pre";

    renderActions(data.next_actions);
    renderInventory(data.inventory_hits);

    setStatus(`Done. Conversation ID: ${data.conversation_id}`);
  } catch (e) {
    console.error(e);
    setStatus(`Error: ${e.message}`, true);
  } finally {
    runBtn.disabled = false;
  }
});

clearBtn.addEventListener("click", () => {
  msgEl.value = "";
  intentEl.textContent = "—";
  replyEl.textContent = "—";
  summaryEl.textContent = "—";
  inventoryEl.textContent = "—";
  actionsEl.innerHTML = "<li>—</li>";
  setStatus("");
});
