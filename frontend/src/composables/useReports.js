import { ref, computed } from 'vue'
import axios from 'axios'

export function useReports(patientId) {
  const isProcessing = ref(false)
  const labData = ref(null)
  const errorMsg = ref('')
  const isSharedView = ref(false)
  const patientHistory = ref([])
  const activeView = ref('upload')

  const fetchPatientHistory = async () => {
    if (!patientId.value) return
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const res = await axios.get(`${apiUrl}/api/patient/${patientId.value}/reports`)
      patientHistory.value = res.data.reports || []
    } catch (err) {
      console.error("Failed to fetch history", err)
    }
  }

  const hasTrends = computed(() => {
    const dates = new Set(patientHistory.value.map(r => new Date(r.created_at).toDateString()))
    return dates.size >= 2
  })

  const loadSharedReport = async (sharedId) => {
    isSharedView.value = true
    isProcessing.value = true
    errorMsg.value = ''
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await axios.get(`${apiUrl}/api/report/${sharedId}`)
      labData.value = response.data
      activeView.value = 'results'
    } catch (err) {
      console.error(err)
      errorMsg.value = err.response?.data?.detail || 'Failed to load shared report.'
    } finally {
      isProcessing.value = false
    }
  }

  const handleUploadSuccess = async (data) => {
    labData.value = data
    activeView.value = 'results'
    isProcessing.value = false
    await fetchPatientHistory()
    errorMsg.value = ''
  }

  const handleUploadStart = () => {
    isProcessing.value = true
    errorMsg.value = ''
  }

  const handleUploadError = (err) => {
    isProcessing.value = false
    errorMsg.value = err
  }

  const selectReport = (report) => {
    labData.value = report
    activeView.value = 'results'
  }

  const clearData = () => {
    labData.value = null
    patientHistory.value = []
    activeView.value = 'upload'
  }

  return {
    isProcessing,
    labData,
    errorMsg,
    isSharedView,
    patientHistory,
    activeView,
    hasTrends,
    fetchPatientHistory,
    loadSharedReport,
    handleUploadSuccess,
    handleUploadStart,
    handleUploadError,
    selectReport,
    clearData
  }
}
