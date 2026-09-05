<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const steps = [
  'loading.step1', // Scanning document...
  'loading.step2', // Identifying clinical markers...
  'loading.step3', // Translating medical terminology...
  'loading.step4', // Analyzing reference ranges...
  'loading.step5', // Generating your plain-English dashboard...
]

const currentStepIndex = ref(0)
let interval = null

onMounted(() => {
  interval = setInterval(() => {
    if (currentStepIndex.value < steps.length - 1) {
      currentStepIndex.value++
    }
  }, 3500)
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
})
</script>

<template>
  <div class="flex flex-col items-center justify-center py-20 px-6 bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800 w-full relative overflow-hidden animate-in zoom-in-95 duration-500">
    <!-- Animated background grid -->
    <div class="absolute inset-0 bg-[linear-gradient(to_right,#0f766e10_1px,transparent_1px),linear-gradient(to_bottom,#0f766e10_1px,transparent_1px)] dark:bg-[linear-gradient(to_right,#14b8a610_1px,transparent_1px),linear-gradient(to_bottom,#14b8a610_1px,transparent_1px)] bg-[size:24px_24px] animate-[gridPan_20s_linear_infinite]"></div>
    
    <div class="absolute inset-0 bg-gradient-to-b from-transparent via-teal-600/5 dark:via-teal-500/10 to-transparent w-full h-full animate-[scan_2.5s_ease-in-out_infinite]"></div>
    
    <div class="relative z-10 flex flex-col items-center w-full max-w-md">
      <!-- 3D pulsing orb -->
      <div class="relative w-28 h-28 mb-10 flex items-center justify-center">
        <div class="absolute inset-0 rounded-full bg-teal-500/20 dark:bg-teal-400/20 animate-ping" style="animation-duration: 3s;"></div>
        <div class="absolute inset-2 rounded-full bg-teal-500/30 dark:bg-teal-400/30 animate-pulse"></div>
        <div class="absolute inset-4 rounded-full bg-gradient-to-tr from-teal-600 to-emerald-400 shadow-[0_0_30px_rgba(20,184,166,0.6)] flex items-center justify-center">
          <svg class="w-10 h-10 text-white animate-[spin_4s_linear_infinite]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
        </div>
      </div>

      <!-- Dynamic Text Sequence -->
      <div class="h-24 flex flex-col items-center justify-center w-full text-center">
        <transition name="fade-up" mode="out-in">
          <div :key="currentStepIndex" class="w-full">
            <h3 class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white mb-3 tracking-tight font-display bg-clip-text text-transparent bg-gradient-to-r from-teal-700 to-emerald-600 dark:from-teal-300 dark:to-emerald-300">
              {{ t(steps[currentStepIndex]) }}
            </h3>
            <p class="text-slate-500 dark:text-slate-400 text-sm font-medium">
              {{ t('loading.pleaseWait') }}
            </p>
          </div>
        </transition>
      </div>

      <!-- Progress bar -->
      <div class="w-full h-2 mt-6 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden relative">
        <div class="absolute top-0 left-0 h-full bg-gradient-to-r from-teal-500 to-emerald-400 transition-all duration-1000 ease-out" :style="{ width: `${((currentStepIndex + 1) / steps.length) * 100}%` }"></div>
        <div class="absolute top-0 left-0 h-full w-full bg-[linear-gradient(45deg,rgba(255,255,255,0.2)_25%,transparent_25%,transparent_50%,rgba(255,255,255,0.2)_50%,rgba(255,255,255,0.2)_75%,transparent_75%,transparent)] bg-[length:1rem_1rem] animate-[progressStripes_1s_linear_infinite]"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes scan {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}
@keyframes gridPan {
  0% { background-position: 0 0; }
  100% { background-position: 24px 24px; }
}
@keyframes progressStripes {
  0% { background-position: 1rem 0; }
  100% { background-position: 0 0; }
}
.fade-up-enter-active,
.fade-up-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-up-enter-from {
  opacity: 0;
  transform: translateY(10px) scale(0.98);
}
.fade-up-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.98);
}
</style>
