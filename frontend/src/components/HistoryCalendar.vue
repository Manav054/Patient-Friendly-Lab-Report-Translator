<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

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

const isMonthDropdownOpen = ref(false)
const isYearDropdownOpen = ref(false)

const closeDropdowns = (e) => {
  if (!e.target.closest('.month-dropdown-container')) isMonthDropdownOpen.value = false
  if (!e.target.closest('.year-dropdown-container')) isYearDropdownOpen.value = false
}

onMounted(() => document.addEventListener('click', closeDropdowns))
onUnmounted(() => document.removeEventListener('click', closeDropdowns))

const monthOptions = computed(() => {
  return Array.from({ length: 12 }, (_, i) => {
    return new Date(2000, i, 1).toLocaleString('default', { month: 'long' })
  })
})

const yearOptions = computed(() => {
  const currentY = new Date().getFullYear()
  return Array.from({ length: currentY - 2000 + 1 }, (_, i) => currentY - i)
})

const setMonth = (m) => {
  currentDate.value = new Date(currentYear.value, m, 1)
  isMonthDropdownOpen.value = false
}

const setYear = (y) => {
  currentDate.value = new Date(y, currentMonth.value, 1)
  isYearDropdownOpen.value = false
}

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
    <header class="bg-white dark:bg-slate-900 p-5 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 flex justify-between items-center transition-colors">
      <div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white tracking-tight font-display">{{ $t('app.previousReports') }}</h2>
        <p class="text-sm text-slate-500 dark:text-slate-400 font-medium mt-1">{{ $t('app.calendarSubtitle') }}</p>
      </div>
    </header>

    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-sm max-w-md mx-auto transition-colors">
      <div class="flex items-center justify-between px-6 py-4 bg-slate-50 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800 transition-colors">
        <button @click="prevMonth" class="p-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
        </button>
        
        <div class="flex items-center gap-3">
          <!-- Month Dropdown -->
          <div class="relative group month-dropdown-container">
            <button @click="isMonthDropdownOpen = !isMonthDropdownOpen" class="flex items-center gap-1.5 bg-transparent text-lg font-bold text-slate-900 dark:text-white font-display cursor-pointer focus:outline-none hover:text-teal-600 dark:hover:text-teal-400 transition-colors">
              {{ monthOptions[currentMonth] }}
              <svg class="w-4 h-4 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            </button>
            <div v-if="isMonthDropdownOpen" class="absolute top-full mt-2 left-1/2 -translate-x-1/2 w-44 bg-white dark:bg-slate-800 rounded-xl shadow-xl border border-slate-200 dark:border-slate-700 z-50 overflow-hidden py-1.5 animate-in fade-in zoom-in-95 duration-200 max-h-[200px] overflow-y-auto custom-scrollbar">
              <button v-for="(m, i) in monthOptions" :key="i" @click="setMonth(i)" class="w-full text-left px-4 py-2.5 text-[15px] font-semibold transition-colors flex items-center justify-between" :class="i === currentMonth ? 'bg-teal-50 dark:bg-teal-900/30 text-teal-700 dark:text-teal-400' : 'text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/50'">
                {{ m }}
                <svg v-if="i === currentMonth" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              </button>
            </div>
          </div>
          
          <!-- Year Dropdown -->
          <div class="relative group year-dropdown-container">
            <button @click="isYearDropdownOpen = !isYearDropdownOpen" class="flex items-center gap-1.5 bg-transparent text-lg font-bold text-slate-900 dark:text-white font-display cursor-pointer focus:outline-none hover:text-teal-600 dark:hover:text-teal-400 transition-colors">
              {{ currentYear }}
              <svg class="w-4 h-4 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            </button>
            <div v-if="isYearDropdownOpen" class="absolute top-full mt-2 left-1/2 -translate-x-1/2 w-32 bg-white dark:bg-slate-800 rounded-xl shadow-xl border border-slate-200 dark:border-slate-700 z-50 py-1.5 animate-in fade-in zoom-in-95 duration-200 max-h-[200px] overflow-y-auto custom-scrollbar">
              <button v-for="y in yearOptions" :key="y" @click="setYear(y)" class="w-full text-left px-4 py-2.5 text-[15px] font-semibold transition-colors flex items-center justify-between" :class="y === currentYear ? 'bg-teal-50 dark:bg-teal-900/30 text-teal-700 dark:text-teal-400' : 'text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/50'">
                {{ y }}
                <svg v-if="y === currentYear" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              </button>
            </div>
          </div>
        </div>

        <button @click="nextMonth" class="p-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
        </button>
      </div>
      
      <div class="p-6">
        <div class="grid grid-cols-7 gap-2 mb-2 text-center text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
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
                    ? 'bg-teal-50 dark:bg-teal-900/30 text-teal-700 dark:text-teal-400 border-teal-200 dark:border-teal-800 hover:bg-teal-600 dark:hover:bg-teal-600 hover:text-white dark:hover:text-white cursor-pointer hover:shadow-md' 
                    : 'bg-slate-50 dark:bg-slate-800/30 text-slate-400 dark:text-slate-600 border-slate-100 dark:border-slate-800 cursor-default hover:bg-slate-50 dark:hover:bg-slate-800/30'
                ]"
              >
                <span class="text-lg">{{ dayObj.day }}</span>
                <div v-if="dayObj.reports.length > 0" class="absolute bottom-2 flex gap-1">
                  <div class="w-1.5 h-1.5 rounded-full bg-teal-500 dark:bg-teal-400 shadow-sm"></div>
                </div>
              </button>
            </template>
            <div v-else class="w-full h-full bg-slate-50 dark:bg-slate-800/30 rounded-lg"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 10px;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #334155;
}
</style>
