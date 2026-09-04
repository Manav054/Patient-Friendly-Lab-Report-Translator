<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['reset'])

// Separate normal vs abnormal tests
const abnormalTests = computed(() => props.data.tests.filter(t => t.is_abnormal))
const normalTests = computed(() => props.data.tests.filter(t => !t.is_abnormal))

const getStatusColor = (isAbnormal) => {
  return isAbnormal ? 'bg-medical-red' : 'bg-medical-green'
}

const getStatusBadgeClass = (isAbnormal) => {
  return isAbnormal 
    ? 'bg-red-100 text-red-800 border-red-200' 
    : 'bg-green-100 text-green-800 border-green-200'
}
</script>

<template>
  <div class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
    
    <div class="flex justify-between items-center bg-white p-4 rounded-xl shadow-sm border border-slate-100">
      <div>
        <h2 class="text-xl font-semibold text-slate-800">Your Lab Results</h2>
        <p class="text-sm text-slate-500" v-if="data.patient_identifiers_found">
          Note: Patient identifiers were detected and securely anonymized before processing.
        </p>
      </div>
      <button @click="emit('reset')" class="text-sm font-medium text-indigo-600 hover:text-indigo-800 px-3 py-1.5 bg-indigo-50 rounded-lg hover:bg-indigo-100 transition-colors">
        Upload New Report
      </button>
    </div>

    <!-- Questions to Ask Your Doctor -->
    <div v-if="data.suggested_physician_questions && data.suggested_physician_questions.length > 0" class="bg-indigo-50 border border-indigo-100 p-6 rounded-xl shadow-sm">
      <h3 class="text-lg font-semibold text-indigo-900 mb-3 flex items-center">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
        Questions for your Doctor
      </h3>
      <ul class="space-y-2">
        <li v-for="(question, index) in data.suggested_physician_questions" :key="index" class="flex items-start">
          <span class="text-indigo-500 mr-2 font-bold">•</span>
          <span class="text-indigo-800">{{ question }}</span>
        </li>
      </ul>
    </div>

    <!-- Abnormal Results (Prioritized) -->
    <div v-if="abnormalTests.length > 0" class="bg-white rounded-xl shadow-sm border border-red-100 overflow-hidden">
      <div class="bg-red-50 px-6 py-4 border-b border-red-100">
        <h3 class="text-lg font-semibold text-red-900">Out of Range (Requires Attention)</h3>
      </div>
      <div class="divide-y divide-slate-100">
        <div v-for="(test, index) in abnormalTests" :key="index" class="p-6">
          <div class="flex flex-col md:flex-row md:items-start justify-between mb-3">
            <div>
              <div class="flex items-center gap-3 mb-1">
                <h4 class="text-lg font-bold text-slate-800">{{ test.marker_name }}</h4>
                <span :class="getStatusBadgeClass(test.is_abnormal)" class="text-xs font-semibold px-2.5 py-0.5 rounded-full border">
                  Out of Range
                </span>
              </div>
              <div class="text-3xl font-black text-red-600 my-2">
                {{ test.value }} <span class="text-base font-medium text-slate-500">{{ test.unit }}</span>
              </div>
              <div class="text-sm text-slate-500 font-medium">
                Standard Range: {{ test.reference_range_low ?? '?' }} - {{ test.reference_range_high ?? '?' }} {{ test.unit }}
              </div>
            </div>
          </div>
          <div class="mt-4 bg-slate-50 rounded-lg p-4 text-slate-700 text-sm border border-slate-100">
            <span class="font-semibold text-slate-900 block mb-1">What does this mean?</span>
            {{ test.layman_explanation }}
          </div>
        </div>
      </div>
    </div>

    <!-- Normal Results -->
    <div v-if="normalTests.length > 0" class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
      <div class="bg-slate-50 px-6 py-4 border-b border-slate-100">
        <h3 class="text-lg font-semibold text-slate-800">Normal Range</h3>
      </div>
      <div class="divide-y divide-slate-100">
        <div v-for="(test, index) in normalTests" :key="index" class="p-6 flex flex-col md:flex-row items-center justify-between">
          <div class="w-full md:w-1/3 mb-4 md:mb-0">
            <h4 class="text-base font-bold text-slate-800">{{ test.marker_name }}</h4>
            <div class="text-sm text-slate-500 font-medium">
              Range: {{ test.reference_range_low ?? '?' }} - {{ test.reference_range_high ?? '?' }} {{ test.unit }}
            </div>
          </div>
          <div class="w-full md:w-1/3 flex items-center mb-4 md:mb-0">
            <div class="text-2xl font-black text-green-600 mr-2">{{ test.value }}</div>
            <div class="text-sm text-slate-500 font-medium">{{ test.unit }}</div>
          </div>
          <div class="w-full md:w-1/3 text-sm text-slate-600 bg-slate-50 p-3 rounded-lg">
            {{ test.layman_explanation }}
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>
