const API = "http://127.0.0.1:8000"

async function login() {
  const email = document.getElementById("email").value
  const password = document.getElementById("password").value
  const msg = document.getElementById("msg")

  const res = await fetch(`${API}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  })

  const data = await res.json()

  if (!res.ok) {
    // FastAPI errors can be object or string
    if (typeof data.detail === "string") {
      msg.innerText = data.detail
    } else if (Array.isArray(data.detail)) {
      msg.innerText = data.detail.map(e => e.msg).join(", ")
    } else {
      msg.innerText = "Login failed"
    }
    return
  }

  if (!data.access_token) {
    msg.innerText = "Token not received"
    return
  }

  localStorage.setItem("token", data.access_token)
  window.location.href = "dashboard.html"
}


async function loadApplications() {
  const token = localStorage.getItem("token")

  if (!token) {
    window.location.href = "index.html"
    return
  }

  const res = await fetch(`${API}/applications`, {
    headers: { Authorization: `Bearer ${token}` }
  })

  if (!res.ok) {
    logout()
    return
  }

  const data = await res.json()
  renderApplications(data)
}

function renderApplications(data) {
  if (!Array.isArray(data)) return

  const cards = document.getElementById("cards")
  cards.innerHTML = ""

  data.forEach(app => {
    const div = document.createElement("div")
    div.className = "app-card"
    div.innerHTML = `
      <h3>${app.company}</h3>
      <p>${app.role}</p>
      <small>${app.status}</small>
    `
    cards.appendChild(div)
  })

  gsap.from(".app-card", {
    opacity: 0,
    y: 40,
    stagger: 0.1
  })
}

async function addApplication() {
  const token = localStorage.getItem("token")

  const company = document.getElementById("company").value
  const role = document.getElementById("role").value
  const status = document.getElementById("status").value

  await fetch(`${API}/applications`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ company, role, status })
  })

  loadApplications()
}

/* ---------------- COMMON ---------------- */

function logout() {
  localStorage.removeItem("token")
  window.location.href = "index.html"
}

/* ---------------- PAGE LOGIC ---------------- */

if (window.location.pathname.includes("dashboard")) {
  loadApplications()
}

const card = document.querySelector(".card")
if (card) {
  gsap.from(card, { opacity: 0, y: 50 })
}
