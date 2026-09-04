<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  patientHistory: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['select-report'])

const currentDate = ref(new Date())

const currentMonth = computed(() => currentDate.value.getMonth())
const currentYear = computed(() => currentDate.value.getFullYear())

const monthName = computed(() => {
  return currentDate.value.toLocaleString('default', { month: 'long', year: 'numeric' })
})

const prevMonth = () => {
  currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
}

const nextMonth = () => {
  currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
}

// Group history by YYYY-MM-DD
const historyMap = computed(() => {
  const map = {}
  props.patientHistory.forEach(report => {
    const d = new Date(report.created_at)
    // Extract local date string YYYY-MM-DD safely
    const dateKey = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
    if (!map[dateKey]) {
      map[dateKey] = []
    }
    map[dateKey].push(report)
  })
  return map
})

const calendarDays = computed(() => {
  const firstDay = new Date(currentYear.value, currentMonth.value, 1)
  const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0)
  
  const days = []
  
  // padding for previous month
  const startingDay = firstDay.getDay()
  for (let i = 0; i < startingDay; i++) {
    days.push(null)
  }
  
  // actual days
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const dateKey = `${currentYear.value}-${String(currentMonth.value + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`
    days.push({
      day: i,
      dateKey,
      reports: historyMap.value[dateKey] || []
    })
  }
  
  return days
})
</script>

<template>
  <div class="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
    <header class="bg-white p-5 rounded-xl shadow-sm border border-slate-200 flex justify-between items-center">
      <div>
        <h2 class="text-2xl font-bold text-slate-900 tracking-tight font-display">Previous Reports</h2>
        <p class="text-sm text-slate-500 font-medium mt-1">Select a highlighted date to view your past results.</p>
      </div>
    </header>

    <div class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm max-w-md mx-auto">
      <div class="flex items-center justify-between px-6 py-4 bg-slate-50 border-b border-slate-200">
        <button @click="prevMonth" class="p-2 text-slate-500 hover:text-slate-900 hover:bg-slate-200 rounded-lg transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
        </button>
        <h3 class="text-lg font-bold text-slate-900 font-display">{{ monthName }}</h3>
        <button @click="nextMonth" class="p-2 text-slate-500 hover:text-slate-900 hover:bg-slate-200 rounded-lg transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
        </button>
      </div>
      
      <div class="p-6">
        <div class="grid grid-cols-7 gap-2 mb-2 text-center text-xs font-bold text-slate-400 uppercase tracking-wider">
          <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
        </div>
        <div class="grid grid-cols-7 gap-2">
          <div v-for="(dayObj, index) in calendarDays" :key="index" class="aspect-square">
            <template v-if="dayObj">
              <button 
                @click="dayObj.reports.length > 0 ? emit('select-report', dayObj.reports[0]) : null"
                :disabled="dayObj.reports.length === 0"
                :class="[
                  'w-full h-full flex flex-col items-center justify-center rounded-lg font-medium transition-all relative border',
                  dayObj.reports.length > 0 
                    ? 'bg-teal-50 text-teal-700 border-teal-200 hover:bg-teal-600 hover:text-white cursor-pointer hover:shadow-md' 
                    : 'bg-slate-50 text-slate-400 border-slate-100 cursor-default hover:bg-slate-50 hover:text-slate-400'
                ]"
              >
                <span class="text-lg">{{ dayObj.day }}</span>
                <div v-if="dayObj.reports.length > 0" class="absolute bottom-2 flex gap-1">
                  <div class="w-1.5 h-1.5 rounded-full bg-teal-500 shadow-sm"></div>
                </div>
              </button>
            </template>
            <div v-else class="w-full h-full bg-slate-50 rounded-lg"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
