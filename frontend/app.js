const API = "http://127.0.0.1:8000";

function getToken() {
  return localStorage.getItem("token");
}

function setMessage(el, text, isError = true) {
  if (!el) return;
  el.innerText = text;
  el.style.color = isError ? "red" : "green";
}

/* ===================== AUTH ===================== */

async function login() {
  const email = document.getElementById("email")?.value.trim();
  const password = document.getElementById("password")?.value.trim();
  const msg = document.getElementById("msg");

  if (!email || !password) {
    setMessage(msg, "Email and password required");
    return;
  }

  try {
    const res = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (!res.ok) {
      if (typeof data.detail === "string") {
        setMessage(msg, data.detail);
      } else if (Array.isArray(data.detail)) {
        setMessage(msg, data.detail.map(e => e.msg).join(", "));
      } else {
        setMessage(msg, "Login failed");
      }
      return;
    }

    if (!data.access_token) {
      setMessage(msg, "Token not received");
      return;
    }

    localStorage.setItem("token", data.access_token);
    window.location.href = "dashboard.html";

  } catch (err) {
    setMessage(msg, "Server not reachable");
  }
}



async function loadApplications() {
  const token = getToken();

  if (!token) {
    window.location.href = "index.html";
    return;
  }

  try {
    const res = await fetch(`${API}/applications`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) {
      logout();
      return;
    }

    const data = await res.json();
    renderApplications(data);

  } catch {
    logout();
  }
}

function renderApplications(applications) {
  if (!Array.isArray(applications)) return;

  const cards = document.getElementById("cards");
  cards.innerHTML = "";

  applications.forEach(app => {
    const card = document.createElement("div");
    card.className = "app-card";

    card.innerHTML = `
      <h3>${app.company}</h3>
      <p>${app.role}</p>
      <span class="status ${app.status}">${app.status}</span>
    `;

    cards.appendChild(card);
  });

  gsap.from(".app-card", {
    opacity: 0,
    y: 40,
    stagger: 0.08,
    duration: 0.4
  });
}

async function addApplication() {
  const token = getToken();

  const company = document.getElementById("company")?.value.trim();
  const role = document.getElementById("role")?.value.trim();
  const status = document.getElementById("status")?.value;

  if (!company || !role || !status) {
    alert("All fields required");
    return;
  }

  try {
    const res = await fetch(`${API}/applications`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ company, role, status })
    });

    if (!res.ok) {
      alert("Failed to add application");
      return;
    }

    document.getElementById("company").value = "";
    document.getElementById("role").value = "";
    document.getElementById("status").value = "";

    loadApplications();

  } catch {
    alert("Server error");
  }
}


function logout() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}

/* ===================== PAGE INIT ===================== */

if (window.location.pathname.includes("dashboard")) {
  loadApplications();
}

const card = document.querySelector(".card");
if (card) {
  gsap.from(card, { opacity: 0, y: 50, duration: 0.5 });
}
