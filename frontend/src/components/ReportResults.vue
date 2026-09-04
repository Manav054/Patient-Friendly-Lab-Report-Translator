<script setup>
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { toPng } from 'html-to-image'
import jsPDF from 'jspdf'

const { t } = useI18n()

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  isSharedView: {
    type: Boolean,
    default: false
  }
})

const copied = ref(false)
const shareLink = async () => {
  if (!props.data.report_id) return
  const link = `${window.location.origin}/?shared=${props.data.report_id}`
  try {
    await navigator.clipboard.writeText(link)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch (err) {
    console.error('Failed to copy', err)
  }
}

const isGeneratingPDF = ref(false)
const downloadPDF = async () => {
  isGeneratingPDF.value = true
  try {
    const element = document.getElementById('report-content')
    const dataUrl = await toPng(element, {
      quality: 0.98,
      backgroundColor: '#09090b',
      pixelRatio: 2
    })
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'px',
      format: [element.offsetWidth, element.offsetHeight]
    })
    pdf.addImage(dataUrl, 'PNG', 0, 0, element.offsetWidth, element.offsetHeight)
    pdf.save(`LabTranslator_Report_${new Date().toLocaleDateString().replace(/\//g, '-')}.pdf`)
  } catch (err) {
    console.error("PDF Generation failed", err)
  } finally {
    isGeneratingPDF.value = false
  }
}

// Separate normal vs abnormal tests safely
const abnormalTests = computed(() => {
  if (!props.data || !Array.isArray(props.data.tests)) return []
  return props.data.tests.filter(t => t.is_abnormal)
})

const normalTests = computed(() => {
  if (!props.data || !Array.isArray(props.data.tests)) return []
  return props.data.tests.filter(t => !t.is_abnormal)
})

const getStatusBadgeClass = (isAbnormal) => {
  return isAbnormal 
    ? 'bg-amber-50 text-amber-700 border-amber-200' 
    : 'bg-teal-50 text-teal-700 border-teal-200'
}

const calculateGaugePosition = (test) => {
  if (test.reference_range_low == null || test.reference_range_high == null) return 50;
  const low = parseFloat(test.reference_range_low);
  const high = parseFloat(test.reference_range_high);
  const val = parseFloat(test.value);
  if (isNaN(low) || isNaN(high) || isNaN(val)) return 50;
  
  const range = high - low;
  if (range <= 0) return 50;
  
  const buffer = range * 0.5;
  const minBound = low - buffer;
  const maxBound = high + buffer;
  
  let percentage = ((val - minBound) / (maxBound - minBound)) * 100;
  return Math.max(0, Math.min(100, percentage));
}
</script>

<template>
  <article class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
    <header class="flex flex-col sm:flex-row sm:justify-between sm:items-center bg-white p-5 rounded-xl shadow-sm border border-slate-200 gap-4 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div>
        <h2 class="text-2xl font-bold text-slate-900 tracking-tight font-display">
          <span v-if="data.created_at" class="text-teal-600 text-lg mr-2 block sm:inline">{{ new Date(data.created_at).toLocaleDateString() }}</span>
          {{ t('dashboard.results') }}
        </h2>
        <p class="text-sm text-slate-500 font-medium mt-1" v-if="data.patient_identifiers_found">
          <span class="inline-block w-2 h-2 rounded-full bg-teal-500 mr-1.5 mb-px"></span>
          {{ t('dashboard.anonymized') }}
        </p>
      </div>
      <div class="flex flex-col sm:flex-row gap-3 self-start sm:self-auto w-full sm:w-auto">
        <button v-if="!isSharedView" @click="downloadPDF" :disabled="isGeneratingPDF" class="text-sm font-bold text-slate-700 px-4 py-2 bg-slate-50 rounded-lg hover:bg-slate-100 hover:text-slate-900 border border-slate-200 active:scale-95 transition-all flex items-center justify-center disabled:opacity-50 min-w-[140px]">
          <svg v-if="isGeneratingPDF" class="animate-spin -ml-1 mr-2 h-4 w-4 text-slate-900" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          {{ isGeneratingPDF ? 'Generating...' : 'Download PDF' }}
        </button>
        <button v-if="data.report_id && !isSharedView" @click="shareLink" class="text-sm font-bold text-white px-4 py-2 bg-violet-600 rounded-lg hover:bg-violet-500 hover:shadow-lg hover:shadow-violet-600/20 active:scale-95 transition-all flex items-center justify-center min-w-[140px]">
          <svg v-if="!copied" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path></svg>
          <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          {{ copied ? t('dashboard.linkCopied') : t('dashboard.shareReport') }}
        </button>
      </div>
    </header>

    <div id="report-content" class="space-y-8 pb-4">
      <!-- Questions to Ask Your Doctor -->
      <section v-if="data.suggested_physician_questions && data.suggested_physician_questions.length > 0" class="bg-white border border-slate-200 p-6 rounded-xl shadow-sm relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-teal-600"></div>
        <h3 class="text-lg font-bold text-slate-900 mb-3 flex items-center tracking-tight font-display">
          <svg class="w-5 h-5 mr-2 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
          {{ t('dashboard.questions') }}
        </h3>
        <ul class="space-y-2.5">
          <li v-for="(question, index) in data.suggested_physician_questions" :key="index" class="flex items-start">
            <span class="text-teal-600 mr-2.5 font-bold mt-px">•</span>
            <span class="text-slate-700 font-medium">{{ question }}</span>
          </li>
        </ul>
      </section>

      <!-- Lifestyle & Wellness Suggestions -->
      <section v-if="data.lifestyle_recommendations && data.lifestyle_recommendations.length > 0" class="bg-white border border-slate-200 p-6 rounded-xl shadow-sm relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-violet-500"></div>
        <h3 class="text-lg font-bold text-slate-900 mb-3 flex items-center tracking-tight font-display">
          <svg class="w-5 h-5 mr-2 text-violet-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
          {{ t('dashboard.lifestyle') }}
        </h3>
        <p class="text-xs text-slate-500 mb-4 font-medium italic">{{ t('dashboard.lifestyleDisclaimer') }}</p>
        <ul class="space-y-2.5">
          <li v-for="(recommendation, index) in data.lifestyle_recommendations" :key="index" class="flex items-start">
            <span class="text-violet-500 mr-2.5 font-bold mt-px">•</span>
            <span class="text-slate-700 font-medium">{{ recommendation }}</span>
          </li>
        </ul>
      </section>

      <!-- Abnormal Results -->
      <section v-if="abnormalTests.length > 0" class="bg-white rounded-xl shadow-sm border border-amber-200 overflow-hidden relative animate-in fade-in slide-in-from-bottom-6 duration-700 delay-150 fill-mode-both">
        <div class="absolute top-0 left-0 w-1 h-full bg-amber-500"></div>
        <header class="bg-amber-50 px-6 py-4 border-b border-amber-100 flex items-center">
          <div class="w-3 h-3 rounded-full bg-amber-500 mr-3 shadow-sm animate-pulse"></div>
          <h3 class="text-lg font-bold text-amber-800 tracking-tight font-display">{{ t('dashboard.outOfRangeAttention') }}</h3>
        </header>
        <div class="divide-y divide-slate-100">
          <article v-for="(test, index) in abnormalTests" :key="index" class="p-6 hover:bg-slate-50 hover:-translate-y-1 hover:shadow-md hover:border-amber-200 transition-all duration-300">
            <div class="flex flex-col md:flex-row md:items-start justify-between mb-4">
              <div>
                <div class="flex items-center gap-3 mb-1.5">
                  <h4 class="text-xl font-bold text-slate-900">{{ test.marker_name }}</h4>
                  <span :class="getStatusBadgeClass(test.is_abnormal)" class="text-xs font-bold px-2.5 py-1 rounded-md border shadow-sm uppercase tracking-wide">
                    {{ t('dashboard.outOfRange') }}
                  </span>
                </div>
                <div class="text-4xl font-black text-amber-600 my-2 tracking-tight">
                  {{ test.value }} <span class="text-lg font-bold text-amber-600/70">{{ test.unit }}</span>
                </div>
                
                <div class="mt-4 mb-2 w-full max-w-sm">
                  <div class="relative h-2 w-full bg-slate-200 rounded-full border border-slate-300 overflow-hidden group">
                    <div class="absolute top-0 left-0 h-full bg-amber-400/80 rounded-l-full" style="width: 25%"></div>
                    <div class="absolute top-0 left-[25%] h-full bg-teal-500/80" style="width: 50%"></div>
                    <div class="absolute top-0 left-[75%] h-full bg-amber-400/80 rounded-r-full" style="width: 25%"></div>
                    <div class="absolute top-0 left-0 h-full w-full bg-slate-200 origin-[100%_50%] animate-[revealTrack_0.8s_cubic-bezier(0.22,1,0.36,1)_forwards]"></div>
                  </div>
                  
                  <div class="relative w-full h-4 mt-1">
                    <div class="absolute top-0 flex flex-col items-center -ml-2 opacity-0 animate-[popMarker_0.4s_cubic-bezier(0.34,1.56,0.64,1)_0.4s_forwards]" :style="{ left: calculateGaugePosition(test) + '%' }">
                      <div class="w-0 h-0 border-l-[4px] border-l-transparent border-r-[4px] border-r-transparent border-b-[6px] border-b-slate-900"></div>
                      <div class="w-3 h-3 bg-slate-900 rounded-full shadow-sm border border-slate-900 z-10 mt-0.5"></div>
                    </div>
                  </div>
                  <div class="flex justify-between text-[10px] text-slate-500 font-bold uppercase tracking-wider mt-2 px-1">
                    <span>{{ t('dashboard.low') }}</span>
                    <span>{{ t('dashboard.normal') }}</span>
                    <span>{{ t('dashboard.high') }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="bg-slate-50 rounded-xl p-4 text-slate-700 text-sm border border-slate-200 shadow-inner relative">
              <div class="absolute -top-2 left-6 w-4 h-4 bg-slate-50 border-t border-l border-slate-200 transform rotate-45"></div>
              <span class="font-bold text-slate-900 block mb-1.5 relative z-10">{{ t('dashboard.whatDoesThisMean') }}</span>
              <p class="relative z-10 font-medium leading-relaxed" v-html="(test.layman_explanation || '').replace(/\b([a-zA-Z]{6,})\b/g, '<span class=\'border-b border-dashed border-slate-400 hover:bg-teal-50 hover:text-teal-900 transition-colors cursor-help\'>$1</span>')"></p>
            </div>
          </article>
        </div>
      </section>

      <!-- Normal Results -->
      <section v-if="normalTests.length > 0" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden animate-in fade-in slide-in-from-bottom-8 duration-700 delay-300 fill-mode-both">
        <header class="bg-slate-50 px-6 py-4 border-b border-slate-200 flex items-center">
          <div class="w-3 h-3 rounded-full bg-teal-500 mr-3 shadow-sm"></div>
          <h3 class="text-lg font-bold text-slate-900 tracking-tight font-display">{{ t('dashboard.normalRange') }}</h3>
        </header>
        <div class="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 bg-slate-50/50">
          <article v-for="(test, index) in normalTests" :key="index" class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md hover:border-teal-200 hover:-translate-y-1 transition-all duration-300 flex flex-col justify-between group cursor-default">
            <div class="mb-4">
              <h4 class="text-base font-bold text-slate-900 group-hover:text-teal-600 transition-colors">{{ test.marker_name }}</h4>
            </div>
            <div class="flex flex-col mb-4">
              <div class="flex items-baseline mb-2">
                <div class="text-3xl font-black text-teal-600 mr-1.5 tracking-tight">{{ test.value }}</div>
                <div class="text-sm font-bold text-teal-600/70">{{ test.unit }}</div>
              </div>
              
              <div class="w-full">
                <div class="relative h-1.5 w-full bg-slate-200 rounded-full border border-slate-300 overflow-hidden group">
                  <div class="absolute top-0 left-0 h-full bg-amber-400/30 rounded-l-full" style="width: 25%"></div>
                  <div class="absolute top-0 left-[25%] h-full bg-teal-500/80" style="width: 50%"></div>
                  <div class="absolute top-0 left-[75%] h-full bg-amber-400/30 rounded-r-full" style="width: 25%"></div>
                  <div class="absolute top-0 left-0 h-full w-full bg-slate-200 origin-[100%_50%] animate-[revealTrack_0.8s_cubic-bezier(0.22,1,0.36,1)_forwards]"></div>
                </div>
                
                <div class="relative w-full h-3 mt-1">
                  <div class="absolute top-0 flex flex-col items-center -ml-1.5 opacity-0 animate-[popMarker_0.4s_cubic-bezier(0.34,1.56,0.64,1)_0.4s_forwards]" :style="{ left: calculateGaugePosition(test) + '%' }">
                    <div class="w-0 h-0 border-l-[3px] border-l-transparent border-r-[3px] border-r-transparent border-b-[4px] border-b-slate-900"></div>
                    <div class="w-2.5 h-2.5 bg-slate-900 rounded-full shadow-[0_1px_3px_rgba(0,0,0,0.2)] border border-slate-900 z-10 mt-0.5"></div>
                  </div>
                </div>
              </div>
            </div>
            <div class="text-sm text-slate-600 bg-slate-50 p-3.5 rounded-lg flex-grow border border-slate-100 font-medium leading-relaxed" v-html="(test.layman_explanation || '').replace(/\b([a-zA-Z]{6,})\b/g, '<span class=\'border-b border-dashed border-slate-400 hover:bg-teal-50 hover:text-teal-900 transition-colors cursor-help\'>$1</span>')">
            </div>
          </article>
        </div>
      </section>
    </div>
  </article>
</template>

<style scoped>
@keyframes revealTrack {
  0% { transform: scaleX(1); }
  100% { transform: scaleX(0); }
}
@keyframes popMarker {
  0% { transform: scale(0); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
</style>
