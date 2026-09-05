import { ref, watch } from 'vue'

const isDark = ref(false)

export function useTheme() {
  const initTheme = () => {
    // Check local storage or system preference
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      isDark.value = true
    } else {
      isDark.value = false
    }
    applyTheme()
  }

  const toggleTheme = () => {
    isDark.value = !isDark.value
    applyTheme()
  }

  const applyTheme = () => {
    if (isDark.value) {
      document.documentElement.classList.add('dark')
      localStorage.theme = 'dark'
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.theme = 'light'
    }
  }

  return {
    isDark,
    initTheme,
    toggleTheme
  }
}
