const API_BASE = "http://localhost:8000/api";

function saveToken(token) {
  localStorage.setItem("token", token);
}

function getToken() {
  return localStorage.getItem("token");
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "/"; // redirect to index
}

function toggleForm(form) {
  const login = document.getElementById("login-form");
  const register = document.getElementById("register-form");

  if (form === "register") {
    login.style.display = "none";
    register.style.display = "block";
  } else {
    register.style.display = "none";
    login.style.display = "block";
  }
}

function handleLogin(e) {
  e.preventDefault(); // prevent full page reload
  login(); // call your existing login function
}

function handleRegister(e) {
  e.preventDefault();
  register();
}

async function apiFetch(endpoint, options = {}) {
  const token = getToken();

  options.headers = {
    ...options.headers,
    "Content-Type": options.body instanceof FormData ? undefined : "application/json",
  };

  if (token) {
    options.headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${endpoint}`, options);
  // console.log("API response status:", res.status);
  if (res.status === 401 || res.status === 307) {
    alert("Session expired or unauthorized.");
    logout();
    return;
  }

  return res;
}

async function register() {
  const username = document.getElementById("reg-username").value;
  const email = document.getElementById("reg-email").value;
  const password = document.getElementById("reg-password").value;
  const res = await apiFetch("/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, email, password }),
  });

  if (res && res.ok) {
    alert("Registered successfully!");
  } else {
    alert("Registration failed");
  }
}

async function login() {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;
  const form = new URLSearchParams();
  form.append("username", username);
  form.append("password", password);

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: form,
  });

  const data = await res.json();

  if (res.ok) {
    saveToken(data.access_token);
    window.location.href = "/dashboard";
  } else {
    alert("Login failed");
  }
}

async function submitSummary() {
  const url = document.getElementById("article-url").value;
  const loadingEl = document.getElementById("loading");
  loadingEl.style.display = "block";
  const res = await apiFetch("/summaries/", {
    method: "POST",
    body: JSON.stringify({ url }),
  });
  loadingEl.style.display = "none";
  if (!res) return;

  const data = await res.json();

  if (res.ok) {
    document.getElementById("summary-output").innerText = data.summary_text;
    fetchMySummaries();
  } else {
    alert("Failed to summarize.");
  }
}

async function fetchMySummaries() {
  const res = await apiFetch("/users/me/summaries");

  if (!res) return;

  const data = await res.json();
  const list = document.getElementById("summary-history");
  list.innerHTML = "";

  if (Array.isArray(data.summaries)) {
    data.summaries.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = `${item.url} → ${item.summary_text.slice(0, 100)}...`;
      list.appendChild(li);
    });
  }
}

async function fetchAllSummaries() {
  const res = await apiFetch("/summaries/all");

  if (!res) return;

  const data = await res.json();
  const list = document.getElementById("all-summaries");
  list.innerHTML = "";

  data.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.url} → ${item.summary_text.slice(0, 100)}...`;
    list.appendChild(li);
  });
}
