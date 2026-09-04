import { ref } from 'vue'
import { jwtDecode } from 'jwt-decode'

export function useAuth() {
  const userProfile = ref(null)
  const patientId = ref(null)

  const initAuth = () => {
    const storedUser = localStorage.getItem('userProfile')
    if (storedUser) {
      try {
        userProfile.value = JSON.parse(storedUser)
        patientId.value = userProfile.value.sub
      } catch (e) {
        localStorage.removeItem('userProfile')
      }
    }
  }

  const handleLoginSuccess = (response) => {
    const credential = response.credential
    const decoded = jwtDecode(credential)
    userProfile.value = decoded
    patientId.value = decoded.sub
    localStorage.setItem('userProfile', JSON.stringify(decoded))
  }

  const handleLogout = () => {
    userProfile.value = null
    patientId.value = null
    localStorage.removeItem('userProfile')
  }

  return {
    userProfile,
    patientId,
    initAuth,
    handleLoginSuccess,
    handleLogout
  }
}
