<script lang="ts">
  import { onMount } from 'svelte';
  import {
    Chart,
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
    Filler,
    LineController
  } from 'chart.js';

  Chart.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
    Filler,
    LineController
  );

  let { labels = [], data = [] } = $props<{ labels: string[], data: number[] }>();

  let canvas: HTMLCanvasElement;
  let chart: Chart;

  $effect(() => {
    if (chart) {
        chart.data.labels = labels;
        chart.data.datasets[0].data = data;
        chart.update();
    }
  });

  onMount(() => {
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Sales ($)',
            fill: true,
            tension: 0.3,
            backgroundColor: 'rgba(79, 70, 229, 0.1)',
            borderColor: 'rgb(79, 70, 229)',
            borderJoinStyle: 'miter',
            pointBorderColor: 'rgb(79, 70, 229)',
            pointBackgroundColor: '#fff',
            pointBorderWidth: 5,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: 'rgb(79, 70, 229)',
            pointHoverBorderColor: 'rgba(220, 220, 220, 1)',
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: data
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: '#1f2937',
            titleColor: '#f9fafb',
            bodyColor: '#f3f4f6',
            padding: 10,
            cornerRadius: 8,
            displayColors: false
          }
        },
        scales: {
          x: {
            grid: {
                display: false
            },
            ticks: {
                color: '#6b7280'
            }
          },
          y: {
            grid: {
                color: '#f3f4f6'
            },
            ticks: {
                color: '#6b7280',
                 callback: function(value: any) {
                    return '$' + value;
                }
            },
            beginAtZero: true
          }
        }
      }
    });

    return () => {
        chart.destroy();
    };
  });
</script>

<div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm h-auto">
	<div class="flex items-center justify-between mb-4">
		<h3 class="text-lg font-bold text-gray-900">Sales Overview</h3>
		<select
			class="text-sm border-gray-200 rounded-md text-gray-500 bg-gray-50 border px-2 py-1 focus:outline-none focus:ring-2 focus:ring-indigo-500"
		>
			<option>Last 7 days</option>
			<option>Last 30 days</option>
			<option>This Year</option>
		</select>
	</div>
	<div class="h-80 w-full relative">
		<canvas bind:this={canvas}></canvas>
	</div>
</div>
