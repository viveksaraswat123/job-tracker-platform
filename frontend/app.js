const API = "";

function getToken() {
  return localStorage.getItem("token");
}

function setMessage(el, text, isError = true) {
  if (!el) return;
  el.innerText = text;
  el.style.color = isError ? "red" : "green";
}

/* ===================== AUTH ===================== */

function showLogin() {
  document.getElementById("login-tab").classList.add("active");
  document.getElementById("register-tab").classList.remove("active");
  document.getElementById("login-form").style.display = "block";
  document.getElementById("register-form").style.display = "none";
}

function showRegister() {
  document.getElementById("register-tab").classList.add("active");
  document.getElementById("login-tab").classList.remove("active");
  document.getElementById("register-form").style.display = "block";
  document.getElementById("login-form").style.display = "none";
}

async function login() {
  const email = document.getElementById("login-email")?.value.trim();
  const password = document.getElementById("login-password")?.value.trim();
  const msg = document.getElementById("login-msg");

  if (!email || !password) {
    setMessage(msg, "Email and password required");
    return;
  }

  try {
    const res = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ username: email, password })
    });

    const data = await res.json();

    if (!res.ok) {
      setMessage(msg, data.detail || "Login failed");
      return;
    }

    localStorage.setItem("token", data.access_token);
    window.location.href = "/dashboard";

  } catch (err) {
    setMessage(msg, "Server not reachable");
  }
}

async function register() {
  const email = document.getElementById("register-email")?.value.trim();
  const password = document.getElementById("register-password")?.value.trim();
  const msg = document.getElementById("register-msg");

  if (!email || !password) {
    setMessage(msg, "Email and password required");
    return;
  }

  try {
    const res = await fetch(`${API}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (!res.ok) {
      setMessage(msg, data.detail || "Registration failed");
      return;
    }

    setMessage(msg, "Registration successful! Please login.", false);
    showLogin();

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
      <span class="delete" onclick="deleteApplication(${app.id})">×</span>
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

async function deleteApplication(appId) {
  if (!confirm("Are you sure you want to delete this application?")) return;

  const token = getToken();

  try {
    const res = await fetch(`${API}/applications/${appId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!res.ok) {
      alert("Failed to delete application");
      return;
    }

    loadApplications();

  } catch {
    alert("Server error");
  }
}


function logout() {
  localStorage.removeItem("token");
  window.location.href = "/";
}

/* ===================== STATS ===================== */

async function loadStats() {
  try {
    const res = await fetch(`${API}/stats`);
    if (res.ok) {
      const data = await res.json();
      document.getElementById("total-users").textContent = data.total_users;
      document.getElementById("total-apps").textContent = data.total_applications;
    }
  } catch {
    // Ignore errors
  }
}

/* ===================== PAGE INIT ===================== */

if (window.location.pathname === "/dashboard") {
  loadApplications();
} else if (window.location.pathname === "/") {
  loadStats();
  if (getToken()) {
    window.location.href = "/dashboard";
  }
}

const card = document.querySelector(".card");
if (card) {
  gsap.from(card, { opacity: 0, y: 50, duration: 0.5 });
}
