<script setup>
const props = defineProps({
  userProfile: { type: Object, default: null }
})
</script>

<template>
  <header class="h-16 border-b border-slate-200 flex items-center justify-end px-4 sm:px-6 flex-shrink-0 z-10 sticky top-0 backdrop-blur-md bg-white/80">
    <div v-if="!userProfile" class="flex items-center mr-auto">
      <svg aria-hidden="true" class="w-6 h-6 text-teal-600 mr-2 drop-shadow-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
      <span class="font-bold text-xl tracking-tight text-slate-900 font-display">{{ $t('app.lab') }}<span class="text-teal-600">{{ $t('app.translator') }}</span></span>
    </div>
    <div class="flex items-center gap-4">
      <select v-model="$i18n.locale" class="bg-white border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-teal-500 focus:border-teal-500 block p-2 outline-none shadow-sm">
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
