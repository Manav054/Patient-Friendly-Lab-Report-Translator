<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

const props = defineProps({
  patientId: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['upload-start', 'upload-success', 'upload-error'])

const isDragging = ref(false)
const isUploading = ref(false)
const fileInput = ref(null)

const MAX_FILE_SIZE_MB = 5
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

const handleDragOver = (e) => {
  e.preventDefault()
  isDragging.value = true
}

const handleDragLeave = (e) => {
  e.preventDefault()
  isDragging.value = false
}

const handleDrop = (e) => {
  e.preventDefault()
  isDragging.value = false
  const files = e.dataTransfer.files
  if (files.length > 0) {
    processFile(files[0])
  }
}

const handleFileSelect = (e) => {
  const files = e.target.files
  if (files.length > 0) {
    processFile(files[0])
  }
}

const processFile = async (file) => {
  // Prevent duplicate submissions if already uploading
  if (isUploading.value) return

  // Client-side validation
  const validTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']
  if (!validTypes.includes(file.type)) {
    emit('upload-error', t('upload.invalidType'))
    return
  }

  if (file.size > MAX_FILE_SIZE_BYTES) {
    emit('upload-error', t('upload.sizeExceeded'))
    return
  }

  isUploading.value = true
  emit('upload-start')

  const formData = new FormData()
  formData.append('file', file)
  if (props.patientId) {
    formData.append('patient_id', props.patientId)
  }

  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await axios.post(`${apiUrl}/api/analyze-report?target_language=${encodeURIComponent(locale.value)}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
    })
    
    let resultData = response.data
    if (typeof resultData === 'string') {
      try {
        resultData = JSON.parse(resultData)
      } catch (e) {
        console.error("Failed to parse JSON response:", e)
      }
    }
    
    isUploading.value = false
    emit('upload-success', resultData)
  } catch (err) {
    console.error(err)
    isUploading.value = false
    
    // Graceful handling of timeouts
    if (err.code === 'ECONNABORTED' || err.message.includes('timeout')) {
      emit('upload-error', t('upload.timeout'))
      return
    }

    const errorMsg = err.response?.data?.detail || t('upload.unexpected')
    emit('upload-error', errorMsg)
  }
}

const triggerFileInput = () => {
  fileInput.value.click()
}
</script>

<template>
  <div 
    class="group rounded-2xl shadow-sm border-2 border-dashed transition-all duration-500 p-8 sm:p-10 text-center cursor-pointer w-full relative overflow-hidden focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-600 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-50 dark:focus-visible:ring-offset-slate-900 bg-white dark:bg-slate-900"
    :class="isDragging ? 'border-teal-500 bg-teal-50/80 dark:bg-teal-900/20 shadow-[0_0_40px_rgba(15,118,110,0.15)] dark:shadow-[0_0_40px_rgba(20,184,166,0.1)] scale-[1.02]' : 'border-slate-300 dark:border-slate-700 hover:border-teal-500/60 dark:hover:border-teal-400/60 hover:shadow-[0_0_30px_rgba(15,118,110,0.08)] dark:hover:shadow-[0_0_30px_rgba(20,184,166,0.05)] hover:bg-slate-50/50 dark:hover:bg-slate-800/30 animate-[breatheLight_4s_ease-in-out_infinite]'"
    @dragover="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
    @click="triggerFileInput"
    tabindex="0"
    @keydown.enter.space.prevent="triggerFileInput"
    role="button"
    aria-label="Upload Lab Report"
  >
    <input 
      type="file" 
      ref="fileInput" 
      class="hidden" 
      accept=".pdf,image/png,image/jpeg"
      @change="handleFileSelect"
    />
    
    <!-- Background Bloom Effect -->
    <div class="absolute inset-0 bg-gradient-to-tr from-teal-600/5 dark:from-teal-400/5 via-transparent to-transparent opacity-0 transition-opacity duration-500 pointer-events-none" :class="{'opacity-100': isDragging}"></div>

    <div class="flex justify-center mb-4 relative z-10">
      <div class="p-4 rounded-full bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 shadow-inner group-hover:bg-teal-50 dark:group-hover:bg-teal-900/30 transition-colors duration-300" :class="{'bg-teal-100 dark:bg-teal-900/50 border-teal-300 dark:border-teal-700': isDragging}">
        <svg class="h-12 w-12 text-teal-600 dark:text-teal-400 transition-all duration-500" :class="{'animate-[bounceSpring_1s_infinite] text-teal-700 dark:text-teal-300': isDragging, 'group-hover:scale-110 group-hover:-translate-y-1': !isDragging}" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
      </svg>
    </div>
  </div>
    
    <h3 class="text-lg sm:text-xl font-black text-slate-900 dark:text-white mb-2 tracking-tight relative z-10 font-display">{{ t('upload.clickOrDrag') }}</h3>
    <p class="text-sm text-slate-500 dark:text-slate-400 mb-6 font-medium relative z-10">{{ t('upload.supports') }} <span class="text-slate-700 dark:text-slate-300 font-bold">PDF, PNG, JPG</span> ({{ t('upload.maxSize') }})</p>
    
    <button type="button" class="relative z-10 bg-teal-600 hover:bg-teal-500 text-white font-bold py-3 px-8 rounded-xl transition-all duration-300 shadow-md hover:shadow-lg hover:shadow-teal-600/30 active:scale-95 focus:outline-none focus:ring-2 focus:ring-teal-600 focus:ring-offset-2 focus:ring-offset-slate-50 pointer-events-none uppercase tracking-wide text-sm">
      {{ t('upload.selectFile') }}
    </button>
  </div>
</template>

<style scoped>
@keyframes breatheLight {
  0%, 100% { border-color: rgba(203, 213, 225, 0.8); }
  50% { border-color: rgba(15, 118, 110, 0.3); }
}
@keyframes bounceSpring {
  0%, 100% { transform: translateY(0) scale(1); }
  25% { transform: translateY(-8px) scale(1.05); }
  50% { transform: translateY(0) scale(0.95); }
  75% { transform: translateY(-4px) scale(1.02); }
}
</style>
