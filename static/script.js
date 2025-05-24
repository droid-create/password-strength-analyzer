const passwordInput = document.getElementById('passwordInput');
const togglePassword = document.getElementById('togglePassword');
const themeIcon = document.getElementById("themeIcon");

// Toggle password visibility
togglePassword.addEventListener('change', function () {
  passwordInput.type = this.checked ? 'text' : 'password';
});

// Theme toggle
if (localStorage.getItem("theme") === "dark") {
  document.body.classList.add("dark-mode");
  themeIcon.textContent = "🌞";
}
themeIcon.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  themeIcon.textContent = document.body.classList.contains("dark-mode") ? "🌞" : "🌙";
  localStorage.setItem("theme", document.body.classList.contains("dark-mode") ? "dark" : "light");
});

passwordInput.addEventListener('input', () => {
  fetch('/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password: passwordInput.value })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('strength').innerText = 'Strength: ' + data.strength;
    document.getElementById('crackTime').innerText = 'Estimated Crack Time: ' + data.crack_time;

    const sugEl = document.getElementById('suggestions');
    const common = data.suggestions.find(s => s.includes("common password"));
    if (common) {
      sugEl.innerHTML = `<strong style="color:red">${common}</strong><br>- ${data.suggestions.filter(s => s !== common).join('<br>- ')}`;
    } else if (data.suggestions.length > 0) {
      sugEl.innerHTML = "Suggestions:<br>- " + data.suggestions.join('<br>- ');
    } else {
      sugEl.innerHTML = "Good password! 🎉";
      sugEl.style.color = 'green';
    }

    const bar = document.getElementById("strengthBar");
    if (data.strength === "Weak") {
      bar.style.width = "30%";
      bar.style.background = "red";
    } else if (data.strength === "Moderate") {
      bar.style.width = "60%";
      bar.style.background = "orange";
    } else if (data.strength === "Strong") {
      bar.style.width = "100%";
      bar.style.background = "green";
    }

    const password = passwordInput.value;
    const criteria = [
      { test: password.length >= 12, text: "At least 12 characters" },
      { test: /[a-z]/.test(password), text: "Contains lowercase letter" },
      { test: /[A-Z]/.test(password), text: "Contains uppercase letter" },
      { test: /[0-9]/.test(password), text: "Contains number" },
      { test: /[^A-Za-z0-9]/.test(password), text: "Contains special character" }
    ];

    const listHtml = criteria.map(c =>
      `<span style="color:${c.test ? 'green' : 'red'}">• ${c.text}</span>`
    ).join('<br>');
    document.getElementById('criteriaList').innerHTML = listHtml;
  });
});