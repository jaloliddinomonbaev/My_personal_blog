// Theme Toggle Functionality
document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.getElementById("themeToggle")
  const themeIcon = document.getElementById("themeIcon")
  const body = document.body

  // LocalStorage'dan theme ni yuklash
  const savedTheme = localStorage.getItem("theme") || "light"
  setTheme(savedTheme)

  // Theme toggle button event listener
  themeToggle.addEventListener("click", () => {
    const currentTheme = body.getAttribute("data-theme")
    const newTheme = currentTheme === "dark" ? "light" : "dark"
    setTheme(newTheme)
    localStorage.setItem("theme", newTheme)
  })

  function setTheme(theme) {
    body.setAttribute("data-theme", theme)

    if (theme === "dark") {
      themeIcon.className = "fas fa-sun"
      themeToggle.className = "btn btn-outline-warning"
    } else {
      themeIcon.className = "fas fa-moon"
      themeToggle.className = "btn btn-outline-light"
    }
  }
})

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault()
    const target = document.querySelector(this.getAttribute("href"))
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      })
    }
  })
})

// Loading Animation for Buttons
function showLoading(button) {
  const originalText = button.innerHTML
  button.innerHTML = '<span class="loading"></span> Yuklanmoqda...'
  button.disabled = true

  return function hideLoading() {
    button.innerHTML = originalText
    button.disabled = false
  }
}

// Form Validation
function validateForm(formId) {
  const form = document.getElementById(formId)
  const inputs = form.querySelectorAll("input[required], textarea[required]")
  let isValid = true

  inputs.forEach((input) => {
    if (!input.value.trim()) {
      input.classList.add("is-invalid")
      isValid = false
    } else {
      input.classList.remove("is-invalid")
    }
  })

  return isValid
}

// Email Validation
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// Success/Error Messages
function showMessage(message, type = "success") {
  const alertDiv = document.createElement("div")
  alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`
  alertDiv.style.cssText = "top: 100px; right: 20px; z-index: 9999; min-width: 300px;"

  alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `

  document.body.appendChild(alertDiv)

  // Auto remove after 5 seconds
  setTimeout(() => {
    if (alertDiv.parentNode) {
      alertDiv.remove()
    }
  }, 5000)
}

// Lazy Loading for Images
function lazyLoadImages() {
  const images = document.querySelectorAll("img[data-src]")

  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target
        img.src = img.dataset.src
        img.classList.remove("lazy")
        imageObserver.unobserve(img)
      }
    })
  })

  images.forEach((img) => imageObserver.observe(img))
}

// Initialize lazy loading when DOM is loaded
document.addEventListener("DOMContentLoaded", lazyLoadImages)

// Back to Top Button
function createBackToTopButton() {
  const backToTopBtn = document.createElement("button")
  backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>'
  backToTopBtn.className = "btn btn-primary position-fixed"
  backToTopBtn.style.cssText =
    "bottom: 20px; right: 20px; z-index: 9999; border-radius: 50%; width: 50px; height: 50px; display: none;"
  backToTopBtn.id = "backToTopBtn"

  document.body.appendChild(backToTopBtn)

  // Show/hide button based on scroll position
  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 300) {
      backToTopBtn.style.display = "block"
    } else {
      backToTopBtn.style.display = "none"
    }
  })

  // Scroll to top when clicked
  backToTopBtn.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    })
  })
}

// Initialize back to top button
document.addEventListener("DOMContentLoaded", createBackToTopButton)

// API Helper Functions
async function apiRequest(url, options = {}) {
  try {
    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error("API Request Error:", error)
    throw error
  }
}

// Utility Functions
function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString("uz-UZ", {
    year: "numeric",
    month: "long",
    day: "numeric",
  })
}

function truncateText(text, maxLength) {
  if (text.length <= maxLength) return text
  return text.substr(0, maxLength) + "..."
}

// Local Storage Helper
const storage = {
  set: (key, value) => {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error("LocalStorage set error:", error)
    }
  },

  get: (key, defaultValue = null) => {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : defaultValue
    } catch (error) {
      console.error("LocalStorage get error:", error)
      return defaultValue
    }
  },

  remove: (key) => {
    try {
      localStorage.removeItem(key)
    } catch (error) {
      console.error("LocalStorage remove error:", error)
    }
  },
}

// Export functions for use in other scripts
window.MyBlog = {
  showLoading,
  validateForm,
  validateEmail,
  showMessage,
  apiRequest,
  formatDate,
  truncateText,
  storage,
}
