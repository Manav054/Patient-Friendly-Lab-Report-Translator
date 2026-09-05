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
      backgroundColor: '#f8fafc',
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

const totalTests = computed(() => {
  if (!props.data || !Array.isArray(props.data.tests)) return 0
  return props.data.tests.length
})

// SVG ring progress calculation
const ringCircumference = 2 * Math.PI * 42 // radius=42
const ringOffset = computed(() => {
  if (totalTests.value === 0) return ringCircumference
  const ratio = normalTests.value.length / totalTests.value
  return ringCircumference * (1 - ratio)
})

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
  return Math.max(2, Math.min(98, percentage));
}

const formatRangeLabel = (test) => {
  if (test.reference_range_low == null || test.reference_range_high == null) return ''
  return `${test.reference_range_low} – ${test.reference_range_high} ${test.unit}`
}
</script>

<template>
  <article class="space-y-6">

    <!-- Action Bar -->
    <header class="flex flex-col sm:flex-row sm:justify-between sm:items-center bg-white p-5 rounded-2xl shadow-sm border border-slate-200 gap-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h2 class="text-2xl font-bold text-slate-900 tracking-tight font-display">{{ t('dashboard.results') }}</h2>
        <div class="flex items-center gap-4 mt-1.5">
          <p v-if="data.created_at" class="text-sm text-slate-500 font-medium">
            {{ t('dashboard.reportDate') }}: {{ new Date(data.created_at).toLocaleDateString() }}
          </p>
          <p class="text-sm text-slate-500 font-medium flex items-center" v-if="data.patient_identifiers_found">
            <svg class="w-3.5 h-3.5 mr-1 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
            {{ t('dashboard.anonymized') }}
          </p>
        </div>
      </div>
      <div class="flex flex-col sm:flex-row gap-3 self-start sm:self-auto w-full sm:w-auto">
        <button v-if="!isSharedView" @click="downloadPDF" :disabled="isGeneratingPDF" class="text-sm font-semibold text-slate-700 px-4 py-2.5 bg-slate-50 rounded-xl hover:bg-slate-100 hover:text-slate-900 border border-slate-200 active:scale-[0.97] transition-all flex items-center justify-center disabled:opacity-50 min-w-[140px]">
          <svg v-if="isGeneratingPDF" class="animate-spin -ml-1 mr-2 h-4 w-4 text-slate-900" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          {{ isGeneratingPDF ? 'Generating...' : 'Download PDF' }}
        </button>
        <button v-if="data.report_id && !isSharedView" @click="shareLink" class="text-sm font-semibold text-white px-4 py-2.5 bg-violet-600 rounded-xl hover:bg-violet-500 hover:shadow-lg hover:shadow-violet-600/20 active:scale-[0.97] transition-all flex items-center justify-center min-w-[140px]">
          <svg v-if="!copied" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path></svg>
          <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          {{ copied ? t('dashboard.linkCopied') : t('dashboard.shareReport') }}
        </button>
      </div>
    </header>

    <div id="report-content" class="space-y-6 pb-4">

      <!-- ═══════════════════════════════════════════════════ -->
      <!-- 1. SUMMARY BANNER                                   -->
      <!-- ═══════════════════════════════════════════════════ -->
      <section class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sm:p-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div class="flex items-center gap-6 sm:gap-8">
          <!-- SVG Progress Ring -->
          <div class="relative flex-shrink-0 w-24 h-24 sm:w-28 sm:h-28">
            <svg class="w-full h-full -rotate-90" viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="42" fill="none" stroke="#e2e8f0" stroke-width="6" />
              <circle
                cx="50" cy="50" r="42" fill="none"
                stroke="#0d9488" stroke-width="6"
                stroke-linecap="round"
                :stroke-dasharray="ringCircumference"
                :stroke-dashoffset="ringOffset"
                class="transition-all duration-1000 ease-out ring-progress"
              />
            </svg>
            <div class="absolute inset-0 flex flex-col items-center justify-center">
              <span class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight font-display leading-none">{{ normalTests.length }}/{{ totalTests }}</span>
            </div>
          </div>

          <!-- Summary Text -->
          <div class="flex-1 min-w-0">
            <h3 class="text-lg sm:text-xl font-bold text-slate-900 tracking-tight font-display mb-2">{{ t('dashboard.summary') }}</h3>
            <p class="text-slate-600 font-medium text-sm sm:text-base leading-relaxed">
              <span class="text-teal-700 font-bold">{{ normalTests.length }}</span> {{ t('dashboard.resultsOf') }} <span class="font-bold">{{ totalTests }}</span> {{ t('dashboard.areNormal') }}
            </p>
            <p v-if="abnormalTests.length > 0" class="text-amber-700 font-medium text-sm mt-1.5">
              <span class="font-bold">{{ abnormalTests.length }}</span> {{ t('dashboard.needsAttentionCount', abnormalTests.length) }} {{ t('dashboard.needsAttention').toLowerCase() }}
            </p>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════ -->
      <!-- 2. NEEDS YOUR ATTENTION (Abnormal Results)          -->
      <!-- ═══════════════════════════════════════════════════ -->
      <section v-if="abnormalTests.length > 0" class="bg-white rounded-2xl shadow-sm border border-amber-200/80 overflow-hidden animate-in fade-in slide-in-from-bottom-6 duration-700 delay-150 fill-mode-both">
        <header class="bg-amber-50/80 px-6 py-4 border-b border-amber-100 flex items-center">
          <div class="w-2.5 h-2.5 rounded-full bg-amber-500 mr-3 ring-4 ring-amber-100"></div>
          <h3 class="text-base font-bold text-amber-800 tracking-tight font-display">{{ t('dashboard.needsAttention') }}</h3>
          <span class="ml-auto text-xs font-semibold text-amber-600 bg-amber-100 px-2.5 py-1 rounded-lg">{{ abnormalTests.length }} {{ t('dashboard.needsAttentionCount', abnormalTests.length) }}</span>
        </header>
        <div class="divide-y divide-slate-100">
          <article v-for="(test, index) in abnormalTests" :key="'a-' + index" class="p-6">
            <div class="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-5">
              <div class="flex-1">
                <div class="flex items-center gap-3 mb-2">
                  <h4 class="text-lg font-bold text-slate-900 font-display">{{ test.marker_name }}</h4>
                  <span class="text-[11px] font-bold px-2.5 py-1 rounded-lg border bg-amber-50 text-amber-700 border-amber-200 uppercase tracking-wide">{{ t('dashboard.outOfRange') }}</span>
                </div>
                <div class="flex items-baseline gap-2">
                  <span class="text-3xl sm:text-4xl font-extrabold text-amber-600 tracking-tight font-display">{{ test.value }}</span>
                  <span class="text-sm font-semibold text-amber-500">{{ test.unit }}</span>
                </div>
              </div>
            </div>

            <!-- Range Gauge with Numeric Labels -->
            <div class="mb-5 w-full max-w-md">
              <div class="relative h-2.5 w-full bg-slate-100 rounded-full overflow-hidden">
                <div class="absolute top-0 left-0 h-full bg-amber-300/60 rounded-l-full" style="width: 25%"></div>
                <div class="absolute top-0 left-[25%] h-full bg-teal-400/70" style="width: 50%"></div>
                <div class="absolute top-0 left-[75%] h-full bg-amber-300/60 rounded-r-full" style="width: 25%"></div>
                <div class="absolute top-0 left-0 h-full w-full bg-slate-100 origin-[100%_50%] animate-[revealTrack_0.8s_cubic-bezier(0.22,1,0.36,1)_forwards]"></div>
              </div>
              <!-- Marker -->
              <div class="relative w-full h-5 mt-0.5">
                <div class="absolute top-0 flex flex-col items-center -ml-2 opacity-0 animate-[popMarker_0.4s_cubic-bezier(0.34,1.56,0.64,1)_0.4s_forwards]" :style="{ left: calculateGaugePosition(test) + '%' }">
                  <div class="w-0 h-0 border-l-[5px] border-l-transparent border-r-[5px] border-r-transparent border-b-[6px] border-b-slate-800"></div>
                  <div class="w-3 h-3 bg-slate-800 rounded-full mt-0.5"></div>
                </div>
              </div>
              <!-- Reference Range Labels -->
              <div class="flex justify-between text-[11px] text-slate-500 font-semibold mt-1 px-0.5">
                <span>{{ t('dashboard.low') }}</span>
                <span v-if="formatRangeLabel(test)" class="text-slate-400">{{ t('dashboard.referenceRange') }}: {{ test.reference_range_low }} – {{ test.reference_range_high }}</span>
                <span>{{ t('dashboard.high') }}</span>
              </div>
            </div>

            <!-- Explanation Callout -->
            <div class="bg-slate-50 rounded-xl p-4 text-sm border border-slate-200/80">
              <span class="font-bold text-slate-800 block mb-1">{{ t('dashboard.whatDoesThisMean') }}</span>
              <p class="text-slate-600 font-medium leading-relaxed">{{ test.layman_explanation || '' }}</p>
            </div>
          </article>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════ -->
      <!-- 3. LOOKING GOOD (Normal Results)                    -->
      <!-- ═══════════════════════════════════════════════════ -->
      <section v-if="normalTests.length > 0" class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden animate-in fade-in slide-in-from-bottom-8 duration-700 delay-300 fill-mode-both">
        <header class="bg-teal-50/60 px-6 py-4 border-b border-teal-100/80 flex items-center">
          <div class="w-2.5 h-2.5 rounded-full bg-teal-500 mr-3 ring-4 ring-teal-100"></div>
          <h3 class="text-base font-bold text-teal-800 tracking-tight font-display">{{ t('dashboard.lookingGood') }}</h3>
          <span class="ml-auto text-xs font-semibold text-teal-600 bg-teal-100 px-2.5 py-1 rounded-lg">{{ normalTests.length }} {{ t('dashboard.needsAttentionCount', normalTests.length) }}</span>
        </header>
        <div class="p-5 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <article v-for="(test, index) in normalTests" :key="'n-' + index" class="bg-white p-5 rounded-xl border border-slate-200/80 hover:shadow-md hover:border-teal-200 hover:-translate-y-0.5 transition-all duration-300 flex flex-col justify-between group cursor-default">
            <div class="mb-3">
              <div class="flex items-center justify-between mb-1">
                <h4 class="text-sm font-bold text-slate-900 group-hover:text-teal-700 transition-colors">{{ test.marker_name }}</h4>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded-md bg-teal-50 text-teal-600 border border-teal-100 uppercase tracking-wide">{{ t('dashboard.withinRange') }}</span>
              </div>
            </div>
            <div class="flex items-baseline mb-3">
              <span class="text-2xl font-extrabold text-teal-600 tracking-tight font-display mr-1.5">{{ test.value }}</span>
              <span class="text-xs font-semibold text-teal-500">{{ test.unit }}</span>
            </div>

            <!-- Compact Gauge -->
            <div class="w-full mb-3">
              <div class="relative h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                <div class="absolute top-0 left-0 h-full bg-amber-300/30 rounded-l-full" style="width: 25%"></div>
                <div class="absolute top-0 left-[25%] h-full bg-teal-400/60" style="width: 50%"></div>
                <div class="absolute top-0 left-[75%] h-full bg-amber-300/30 rounded-r-full" style="width: 25%"></div>
                <div class="absolute top-0 left-0 h-full w-full bg-slate-100 origin-[100%_50%] animate-[revealTrack_0.8s_cubic-bezier(0.22,1,0.36,1)_forwards]"></div>
              </div>
              <div class="relative w-full h-3 mt-0.5">
                <div class="absolute top-0 flex flex-col items-center -ml-1.5 opacity-0 animate-[popMarker_0.4s_cubic-bezier(0.34,1.56,0.64,1)_0.4s_forwards]" :style="{ left: calculateGaugePosition(test) + '%' }">
                  <div class="w-0 h-0 border-l-[3px] border-l-transparent border-r-[3px] border-r-transparent border-b-[4px] border-b-slate-800"></div>
                  <div class="w-2 h-2 bg-slate-800 rounded-full mt-0.5"></div>
                </div>
              </div>
              <p v-if="formatRangeLabel(test)" class="text-[10px] text-slate-400 font-medium mt-1">{{ test.reference_range_low }} – {{ test.reference_range_high }} {{ test.unit }}</p>
            </div>

            <!-- Explanation -->
            <div class="text-sm text-slate-600 bg-slate-50 p-3 rounded-lg flex-grow border border-slate-100/80 font-medium leading-relaxed">
              {{ test.layman_explanation || '' }}
            </div>
          </article>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════ -->
      <!-- 4. QUESTIONS + WELLNESS (Side by side on desktop)   -->
      <!-- ═══════════════════════════════════════════════════ -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-500 fill-mode-both">
        <!-- Questions for Your Doctor -->
        <section v-if="data.suggested_physician_questions && data.suggested_physician_questions.length > 0" class="bg-white border border-slate-200 p-6 rounded-2xl shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 w-1 h-full bg-teal-500 rounded-r-full"></div>
          <h3 class="text-base font-bold text-slate-900 mb-4 flex items-center tracking-tight font-display">
            <div class="w-8 h-8 rounded-lg bg-teal-50 border border-teal-100 flex items-center justify-center mr-3">
              <svg class="w-4 h-4 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
            </div>
            {{ t('dashboard.questions') }}
          </h3>
          <ol class="space-y-3 list-none">
            <li v-for="(question, index) in data.suggested_physician_questions" :key="'q-' + index" class="flex items-start">
              <span class="flex-shrink-0 w-6 h-6 rounded-full bg-teal-50 text-teal-700 text-xs font-bold flex items-center justify-center mr-3 mt-0.5 border border-teal-100">{{ index + 1 }}</span>
              <span class="text-slate-700 font-medium text-sm leading-relaxed">{{ question }}</span>
            </li>
          </ol>
        </section>

        <!-- Wellness Suggestions -->
        <section v-if="data.lifestyle_recommendations && data.lifestyle_recommendations.length > 0" class="bg-white border border-slate-200 p-6 rounded-2xl shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 w-1 h-full bg-violet-400 rounded-r-full"></div>
          <h3 class="text-base font-bold text-slate-900 mb-1 flex items-center tracking-tight font-display">
            <div class="w-8 h-8 rounded-lg bg-violet-50 border border-violet-100 flex items-center justify-center mr-3">
              <svg class="w-4 h-4 text-violet-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
            </div>
            {{ t('dashboard.wellnessTips') }}
          </h3>
          <p class="text-[11px] text-slate-400 mb-4 font-medium ml-11">{{ t('dashboard.lifestyleDisclaimer') }}</p>
          <ul class="space-y-3">
            <li v-for="(recommendation, index) in data.lifestyle_recommendations" :key="'r-' + index" class="flex items-start">
              <span class="flex-shrink-0 w-1.5 h-1.5 rounded-full bg-violet-400 mr-3 mt-2"></span>
              <span class="text-slate-700 font-medium text-sm leading-relaxed">{{ recommendation }}</span>
            </li>
          </ul>
        </section>
      </div>

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
.ring-progress {
  animation: ringDraw 1.2s cubic-bezier(0.65, 0, 0.35, 1) forwards;
}
@keyframes ringDraw {
  from { stroke-dashoffset: 263.89; }
}
</style>
