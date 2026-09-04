<script setup>
import { ref } from 'vue'
import UploadForm from './components/UploadForm.vue'
import Dashboard from './components/Dashboard.vue'

const isProcessing = ref(false)
const labData = ref(null)
const errorMsg = ref('')

const handleUploadSuccess = (data) => {
  labData.value = data
  isProcessing.value = false
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
</script>

<template>
  <div class="min-h-screen bg-slate-50 text-slate-800 font-sans p-6 md:p-12">
    <!-- Medical Disclaimer -->
    <div class="max-w-4xl mx-auto bg-blue-50 border-l-4 border-blue-500 text-blue-700 p-4 rounded mb-8 shadow-sm">
      <div class="flex items-start">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-blue-500 mt-0.5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-semibold">Medical Disclaimer</h3>
          <p class="text-sm mt-1">
            This application uses AI to help you understand your lab reports. It provides information, not medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
          </p>
        </div>
      </div>
    </div>

    <!-- Main Content Header -->
    <div class="max-w-4xl mx-auto mb-10 text-center">
      <h1 class="text-3xl md:text-4xl font-bold text-slate-900 tracking-tight mb-3">Patient-Friendly Lab Translator</h1>
      <p class="text-slate-500 max-w-2xl mx-auto">Upload your complex blood test results and instantly get a plain-English, visual dashboard to understand what your numbers mean.</p>
    </div>

    <!-- Main Views -->
    <div class="max-w-4xl mx-auto">
      <div v-if="errorMsg" class="mb-6 bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded shadow-sm">
        <p class="font-semibold">Error processing report</p>
        <p class="text-sm mt-1">{{ errorMsg }}</p>
        <button @click="errorMsg = ''" class="mt-2 text-sm underline text-red-600 hover:text-red-800">Dismiss</button>
      </div>

      <div v-if="isProcessing" class="flex flex-col items-center justify-center p-12 bg-white rounded-xl shadow-sm border border-slate-100">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
        <h3 class="text-lg font-medium text-slate-700">Analyzing your lab report...</h3>
        <p class="text-slate-500 text-sm mt-2 text-center max-w-md">Our AI is reading your file, extracting biomarker data, and simplifying the medical jargon. This may take a few seconds.</p>
      </div>
      
      <Dashboard v-else-if="labData" :data="labData" @reset="labData = null" />
      
      <UploadForm v-else @upload-start="handleUploadStart" @upload-success="handleUploadSuccess" @upload-error="handleUploadError" />
    </div>
  </div>
</template>
