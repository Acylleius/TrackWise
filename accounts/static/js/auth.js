document.addEventListener('DOMContentLoaded', () => {
  // ✅ Toggle password show/hide
  document.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
      const selector = btn.dataset.target;
      const input = document.querySelector(selector);
      if (!input) return;
      if (input.type === 'password') { 
        input.type = 'text'; 
        btn.innerText = 'Hide'; 
      } else { 
        input.type = 'password'; 
        btn.innerText = 'Show'; 
      }
    });
  });

  // ✅ Registration form password check
  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
      const p1 = document.getElementById('reg-password1').value;
      const p2 = document.getElementById('reg-password2').value;
      if (p1 !== p2) { 
        e.preventDefault(); 
        alert('Passwords do not match'); 
      }
    });
  }

  // ✅ Cancel button handler
  const cancelBtn = document.getElementById('cancel-btn');
  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => {
      // Option 1: Clear the form
      if (registerForm) registerForm.reset();

      // Option 2: Redirect (uncomment if you want to send them back to login instead)
       window.location.href = "{% url 'accounts:login' %}";
    });
  }

  // ✅ Login form validation
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      const u = document.getElementById('login-username').value.trim();
      const p = document.getElementById('login-password').value.trim();
      if (!u || !p) { 
        e.preventDefault(); 
        alert('Please fill username and password.'); 
      }
    });
  }
});
