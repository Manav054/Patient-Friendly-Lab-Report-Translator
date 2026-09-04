<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emit = defineEmits(['upload-start', 'upload-success', 'upload-error'])

const isDragging = ref(false)
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
  // Client-side validation
  const validTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']
  if (!validTypes.includes(file.type)) {
    emit('upload-error', 'Invalid file type. Please upload a PDF, JPG, or PNG.')
    return
  }

  if (file.size > MAX_FILE_SIZE_BYTES) {
    emit('upload-error', `File size exceeds the ${MAX_FILE_SIZE_MB}MB limit.`)
    return
  }

  emit('upload-start')

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await axios.post('http://localhost:8000/api/analyze-report', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    emit('upload-success', response.data)
  } catch (err) {
    console.error(err)
    const errorMsg = err.response?.data?.detail || 'An unexpected error occurred while communicating with the server.'
    emit('upload-error', errorMsg)
  }
}

const triggerFileInput = () => {
  fileInput.value.click()
}
</script>

<template>
  <div 
    class="bg-white rounded-xl shadow-sm border-2 border-dashed transition-colors duration-200 p-12 text-center"
    :class="isDragging ? 'border-indigo-500 bg-indigo-50/50' : 'border-slate-200 hover:border-indigo-300 hover:bg-slate-50'"
    @dragover="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
    @click="triggerFileInput"
  >
    <input 
      type="file" 
      ref="fileInput" 
      class="hidden" 
      accept=".pdf, .png, .jpg, .jpeg"
      @change="handleFileSelect"
    />
    
    <div class="flex justify-center mb-4">
      <svg class="h-12 w-12 text-slate-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
      </svg>
    </div>
    
    <h3 class="text-lg font-medium text-slate-900 mb-1">Click or drag your lab report here</h3>
    <p class="text-sm text-slate-500 mb-4">Supports PDF, PNG, or JPG (max. 5MB)</p>
    
    <button class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-6 rounded-lg transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
      Select File
    </button>
  </div>
</template>
