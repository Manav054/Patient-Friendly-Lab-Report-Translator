<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

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
            borderColor: '#0f766e',
            backgroundColor: 'rgba(15, 118, 110, 0.1)',
            tension: 0.3,
            fill: true,
            pointBackgroundColor: '#0f766e',
            pointBorderColor: '#fff',
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
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              titleColor: '#0f172a',
              bodyColor: '#0f766e',
              borderColor: '#e2e8f0',
              borderWidth: 1
            }
          },
          scales: {
            y: { grid: { color: '#f1f5f9' }, ticks: { color: '#64748b' } },
            x: { grid: { display: false }, ticks: { color: '#64748b' } }
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
    <header class="bg-white p-5 rounded-xl shadow-sm border border-slate-200 mb-6">
      <h2 class="text-2xl font-bold text-slate-900 tracking-tight font-display">Historical Trends</h2>
      <p class="text-sm text-slate-500 font-medium mt-1">Track your biomarkers over time.</p>
    </header>

    <div v-if="trendCharts.length === 0" class="text-center py-12 text-slate-500 bg-slate-50 border border-slate-200 rounded-xl">
      <p>No historical trends available yet.</p>
      <p class="text-sm mt-2">Upload more reports over time to see your progress.</p>
    </div>
    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <article v-for="chart in trendCharts" :key="chart.name" class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
        <h4 class="text-lg font-bold text-slate-900 mb-4">{{ chart.name }}</h4>
        <div class="h-64">
          <Line :data="chart.chartData" :options="chart.chartOptions" />
        </div>
      </article>
    </div>
  </div>
</template>
