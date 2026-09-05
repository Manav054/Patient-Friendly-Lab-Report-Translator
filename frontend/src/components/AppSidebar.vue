<script setup>
const props = defineProps({
  userProfile: { type: Object, required: true },
  hasTrends: { type: Boolean, default: false },
  activeView: { type: String, default: 'upload' }
})

const emit = defineEmits(['update:activeView', 'logout', 'clear-data'])
</script>

<template>
  <aside class="w-64 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col flex-shrink-0 z-20 transition-colors">
    <div class="h-16 flex items-center px-6 border-b border-slate-200 dark:border-slate-800 transition-colors">
      <svg aria-hidden="true" class="w-6 h-6 text-teal-600 dark:text-teal-400 mr-2 drop-shadow-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
      <span class="font-bold text-lg tracking-tight text-slate-900 dark:text-white font-display">{{ $t('app.lab') }}<span class="text-teal-600 dark:text-teal-400">{{ $t('app.translator') }}</span></span>
    </div>
    <nav class="flex-1 px-4 py-6 space-y-2">
      <button @click="emit('update:activeView', 'upload'); emit('clear-data')" :class="['w-full flex items-center px-4 py-3 rounded-xl font-bold transition-all', activeView === 'upload' ? 'bg-teal-50 dark:bg-teal-900/30 text-teal-700 dark:text-teal-400' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/50']">
        <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
        {{ $t('dashboard.uploadNew') }}
      </button>
      <button @click="emit('update:activeView', 'calendar')" :class="['w-full flex items-center px-4 py-3 rounded-xl font-bold transition-all', activeView === 'calendar' || activeView === 'results' ? 'bg-teal-50 dark:bg-teal-900/30 text-teal-700 dark:text-teal-400' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/50']">
        <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
        {{ $t('app.previousReports') }}
      </button>
      <button v-if="hasTrends" @click="emit('update:activeView', 'trends')" :class="['w-full flex items-center px-4 py-3 rounded-xl font-bold transition-all', activeView === 'trends' ? 'bg-teal-50 dark:bg-teal-900/30 text-teal-700 dark:text-teal-400' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/50']">
        <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
        {{ $t('app.trends') }}
      </button>
    </nav>
    <div class="p-4 border-t border-slate-200 dark:border-slate-800 flex items-center gap-3 bg-slate-50/50 dark:bg-slate-800/30 transition-colors">
      <img :src="userProfile.picture" alt="Avatar" class="w-10 h-10 rounded-full border border-slate-300 dark:border-slate-600">
      <div class="flex-1 overflow-hidden">
        <p class="text-sm font-bold text-slate-900 dark:text-white truncate">{{ userProfile.name }}</p>
        <button @click="emit('logout')" class="text-xs text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-colors">{{ $t('app.logout') }}</button>
      </div>
    </div>
  </aside>
</template>
