<script setup>
import { onMounted } from 'vue'
import UploadForm from './components/UploadForm.vue'
import ReportResults from './components/ReportResults.vue'
import TrendsView from './components/TrendsView.vue'
import HistoryCalendar from './components/HistoryCalendar.vue'
import AppSidebar from './components/AppSidebar.vue'
import AppHeader from './components/AppHeader.vue'
import LoginView from './components/LoginView.vue'
import LoadingOverlay from './components/LoadingOverlay.vue'

import { useAuth } from './composables/useAuth'
import { useReports } from './composables/useReports'
import { useTheme } from './composables/useTheme'

const { initTheme } = useTheme()
const { userProfile, patientId, initAuth, handleLoginSuccess, handleLogout } = useAuth()
const {
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
  clearCurrentReport,
  clearData
} = useReports(patientId)

onMounted(async () => {
  initTheme()
  initAuth()
  if (userProfile.value) {
    await fetchPatientHistory()
  }

  const urlParams = new URLSearchParams(window.location.search)
  const sharedId = urlParams.get('shared')
  
  if (sharedId) {
    await loadSharedReport(sharedId)
  }
})

const onLoginSuccess = async (response) => {
  handleLoginSuccess(response)
  await fetchPatientHistory()
}

const onLogout = () => {
  handleLogout()
  clearData()
}
</script>

<template>
  <div class="flex h-screen bg-slate-50 dark:bg-slate-950 overflow-hidden w-full font-sans text-slate-900 dark:text-slate-50 transition-colors duration-300">
    <!-- Accessibility Skip Link -->
    <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 z-50 bg-teal-600 text-white px-4 py-2 font-bold rounded-lg shadow-lg outline-none ring-2 ring-teal-600 ring-offset-2 ring-offset-slate-50">
      {{ $t('app.skipToMain') }}
    </a>

    <!-- Sidebar -->
    <AppSidebar 
      v-if="userProfile && !isSharedView" 
      :user-profile="userProfile" 
      :has-trends="hasTrends"
      v-model:active-view="activeView"
      @logout="onLogout"
      @clear-data="clearCurrentReport"
    />

    <div class="flex-1 flex flex-col w-full relative h-full">
      <AppHeader :user-profile="userProfile" />

      <main id="main-content" class="flex-1 overflow-y-auto w-full relative">
        <div class="fixed inset-0 pointer-events-none z-0 opacity-40 dark:opacity-20 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-100 via-slate-50 to-slate-50 dark:from-teal-900/20 dark:via-slate-950 dark:to-slate-950 transition-colors duration-300"></div>
        <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8 flex flex-col relative z-10 min-h-full">
          
          <!-- Login Screen -->
          <LoginView v-if="!userProfile && !isSharedView" @login-success="onLoginSuccess" />

          <!-- App Views -->
          <div v-else class="w-full flex flex-col flex-1">
            <div v-if="errorMsg" class="mb-8 w-full bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-6 py-4 rounded-xl shadow-sm flex items-start justify-between">
              <div>
                <p class="font-bold text-base text-red-800 dark:text-red-400">{{ $t('app.errorProcessing') }}</p>
                <p class="text-sm mt-1 font-medium">{{ errorMsg }}</p>
              </div>
              <button @click="errorMsg = ''" class="p-1 rounded-md hover:bg-red-100 dark:hover:bg-red-900/50 text-red-600 dark:text-red-400 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </div>

            <LoadingOverlay v-if="isProcessing" />

            <div v-show="!isProcessing && activeView === 'upload'" class="w-full h-full flex flex-col items-center">
              <section class="text-center px-4 w-full max-w-3xl mx-auto mb-8 animate-in fade-in slide-in-from-bottom-8 duration-1000 mt-8">
                <h1 class="text-3xl md:text-5xl font-black text-slate-900 dark:text-white tracking-tight mb-3 leading-tight font-display">
                  {{ $t('app.demystify') }} <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-600 via-emerald-500 to-teal-600 dark:from-teal-400 dark:via-emerald-300 dark:to-teal-400 animate-text-gradient">{{ $t('app.labTests') }}</span>
                </h1>
                <p class="text-base md:text-lg text-slate-500 dark:text-slate-400 mb-6 leading-relaxed font-medium">
                  {{ $t('app.subtitle') }}
                </p>
                <div class="bg-white dark:bg-slate-900 border-l-4 border-l-teal-600 dark:border-l-teal-500 px-4 py-3 rounded-lg shadow-sm text-left w-full border-y border-r border-y-slate-200 dark:border-y-slate-800 border-r-slate-200 dark:border-r-slate-800 transition-colors">
                  <div class="flex items-start">
                    <div class="flex-shrink-0">
                      <svg class="h-5 w-5 text-teal-600 dark:text-teal-400 mt-0.5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" /></svg>
                    </div>
                    <div class="ml-3">
                      <h3 class="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300 font-display">{{ $t('app.medicalDisclaimer') }}</h3>
                      <p class="text-xs mt-1.5 leading-relaxed text-slate-500 dark:text-slate-400 font-medium">{{ $t('app.disclaimerText') }}</p>
                    </div>
                  </div>
                </div>
              </section>
              <div class="w-full max-w-3xl">
                <UploadForm :patient-id="patientId" @upload-start="handleUploadStart" @upload-success="handleUploadSuccess" @upload-error="handleUploadError" />
              </div>
            </div>

            <div v-if="!isProcessing && activeView === 'results'" class="w-full">
              <ReportResults :data="labData" :is-shared-view="isSharedView" />
            </div>

            <div v-if="!isProcessing && activeView === 'calendar'" class="w-full">
              <HistoryCalendar :patientHistory="patientHistory" @select-report="selectReport" />
            </div>

            <div v-if="!isProcessing && activeView === 'trends'" class="w-full">
              <TrendsView :patientHistory="patientHistory" />
            </div>
            
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
@keyframes scanLine {
  0% { top: 0; opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { top: 100%; opacity: 0; }
}
@keyframes scan {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}
@keyframes textGradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.animate-text-gradient {
  background-size: 200% auto;
  animation: textGradient 4s linear infinite;
}
</style>
