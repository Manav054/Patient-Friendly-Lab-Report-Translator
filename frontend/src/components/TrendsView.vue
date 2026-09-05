<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js'
import { useTheme } from '../composables/useTheme'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const { isDark } = useTheme()

const props = defineProps({
  patientHistory: {
    type: Array,
    required: true
  }
})

const trendCharts = computed(() => {
  if (!props.patientHistory || props.patientHistory.length < 2) return []
  
  const sortedHistory = [...props.patientHistory].sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
  const labels = sortedHistory.map(h => new Date(h.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' }))
  
  const markerMap = {}
  sortedHistory.forEach((report, i) => {
    report.tests.forEach(test => {
      if (!markerMap[test.marker_name]) {
        markerMap[test.marker_name] = {
          data: new Array(sortedHistory.length).fill(null),
          unit: test.unit
        }
      }
      markerMap[test.marker_name].data[i] = test.value
    })
  })
  
  const charts = []
  for (const [name, info] of Object.entries(markerMap)) {
    const validPoints = info.data.filter(v => v !== null).length
    if (validPoints > 1) {
      charts.push({
        name,
        chartData: {
          labels,
          datasets: [{
            label: `${name} (${info.unit})`,
            data: info.data,
            borderColor: isDark.value ? '#2dd4bf' : '#0f766e',
            backgroundColor: isDark.value ? 'rgba(45, 212, 191, 0.15)' : 'rgba(15, 118, 110, 0.1)',
            tension: 0.3,
            fill: true,
            pointBackgroundColor: isDark.value ? '#2dd4bf' : '#0f766e',
            pointBorderColor: isDark.value ? '#0f172a' : '#fff',
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6
          }]
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { 
              mode: 'index', 
              intersect: false,
              backgroundColor: isDark.value ? 'rgba(15, 23, 42, 0.95)' : 'rgba(255, 255, 255, 0.95)',
              titleColor: isDark.value ? '#f8fafc' : '#0f172a',
              bodyColor: isDark.value ? '#2dd4bf' : '#0f766e',
              borderColor: isDark.value ? '#334155' : '#e2e8f0',
              borderWidth: 1
            }
          },
          scales: {
            y: { grid: { color: isDark.value ? '#334155' : '#f1f5f9' }, ticks: { color: isDark.value ? '#94a3b8' : '#64748b' } },
            x: { grid: { display: false }, ticks: { color: isDark.value ? '#94a3b8' : '#64748b' } }
          }
        }
      })
    }
  }
  return charts
})
</script>

<template>
  <div class="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
    <header class="bg-white dark:bg-slate-900 p-5 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 mb-6 transition-colors">
      <h2 class="text-2xl font-bold text-slate-900 dark:text-white tracking-tight font-display">{{ $t('app.historicalTrends') }}</h2>
      <p class="text-sm text-slate-500 dark:text-slate-400 font-medium mt-1">{{ $t('app.trendsSubtitle') }}</p>
    </header>

    <div v-if="trendCharts.length === 0" class="text-center py-12 text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-xl transition-colors">
      <p>{{ $t('app.noTrends') }}</p>
      <p class="text-sm mt-2">{{ $t('app.noTrendsSub') }}</p>
    </div>
    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <article v-for="chart in trendCharts" :key="chart.name" class="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm transition-colors">
        <h4 class="text-lg font-bold text-slate-900 dark:text-white mb-4">{{ chart.name }}</h4>
        <div class="h-64">
          <Line :data="chart.chartData" :options="chart.chartOptions" />
        </div>
      </article>
    </div>
  </div>
</template>
