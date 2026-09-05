<script setup>
const emit = defineEmits(['login-success'])

const handleCallback = (response) => {
  emit('login-success', response)
}
</script>

<template>
  <div class="flex-1 flex flex-col items-center justify-center min-h-[600px] w-full relative animate-in fade-in zoom-in-95 duration-700">
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-teal-600/5 dark:bg-teal-400/5 rounded-full blur-[100px] pointer-events-none"></div>
    <div class="bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border border-slate-200 dark:border-slate-800 p-8 sm:p-10 rounded-2xl shadow-xl max-w-md w-full text-center relative overflow-hidden group transition-colors">
      <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-teal-600 via-emerald-500 to-teal-600 dark:from-teal-400 dark:via-emerald-400 dark:to-teal-400 opacity-80 group-hover:opacity-100 transition-opacity"></div>
      <div class="w-16 h-16 bg-slate-50 dark:bg-slate-800 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-inner border border-slate-200 dark:border-slate-700 group-hover:scale-110 group-hover:shadow-[0_0_20px_rgba(15,118,110,0.15)] dark:group-hover:shadow-[0_0_20px_rgba(20,184,166,0.15)] transition-all duration-500">
        <svg aria-hidden="true" class="w-8 h-8 text-teal-600 dark:text-teal-400 drop-shadow-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
      </div>
      <h2 class="text-3xl font-black text-slate-900 dark:text-white mb-3 tracking-tight font-display transition-colors">
        {{ $t('login.welcomeTo') }} <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-600 to-emerald-500 dark:from-teal-400 dark:to-emerald-400">{{ $t('login.labTranslator') }}</span>
      </h2>
      <p class="text-slate-500 dark:text-slate-400 mb-8 text-sm font-medium leading-relaxed px-2 transition-colors">
        {{ $t('login.subtitle') }}
      </p>
      <div class="flex justify-center mb-4">
          <GoogleLogin :callback="handleCallback" class="transform hover:scale-105 transition-transform duration-300" />
      </div>
      <p class="text-xs text-slate-400 dark:text-slate-500 font-medium mt-8 transition-colors">
        {{ $t('login.terms') }}
      </p>
    </div>
  </div>
</template>
