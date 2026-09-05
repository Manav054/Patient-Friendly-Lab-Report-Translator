<script setup>
import { useTheme } from '../composables/useTheme'

const { isDark, toggleTheme } = useTheme()

const props = defineProps({
  userProfile: { type: Object, default: null }
})
</script>

<template>
  <header class="h-16 border-b border-slate-200 dark:border-slate-800 flex items-center justify-end px-4 sm:px-6 flex-shrink-0 z-10 sticky top-0 backdrop-blur-md bg-white/80 dark:bg-slate-950/80 transition-colors duration-300">
    <div v-if="!userProfile" class="flex items-center mr-auto">
      <svg aria-hidden="true" class="w-6 h-6 text-teal-600 mr-2 drop-shadow-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
      <span class="font-bold text-xl tracking-tight text-slate-900 dark:text-white font-display">{{ $t('app.lab') }}<span class="text-teal-600 dark:text-teal-400">{{ $t('app.translator') }}</span></span>
    </div>
    <div class="flex items-center gap-2 sm:gap-4">
      <button @click="toggleTheme" class="p-2 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-white dark:hover:bg-slate-800 transition-colors" aria-label="Toggle Dark Mode">
        <!-- Sun icon -->
        <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
        <!-- Moon icon -->
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
      </button>
      <select v-model="$i18n.locale" class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-sm rounded-lg focus:ring-teal-500 focus:border-teal-500 block p-2 outline-none shadow-sm transition-colors">
        <option value="English">English</option>
        <option value="Spanish">Español</option>
        <option value="French">Français</option>
        <option value="German">Deutsch</option>
        <option value="Italian">Italiano</option>
        <option value="Portuguese">Português</option>
        <option value="Hindi">हिन्दी</option>
        <option value="Chinese (Simplified)">简体中文</option>
        <option value="Japanese">日本語</option>
      </select>
    </div>
  </header>
</template>
