<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const time = ref('')
const date = ref('')

const week = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']

let timerID = null

function zeroPadding(num, digit) {
  let zero = ''
  for (let i = 0; i < digit; i++) {
    zero += '0'
  }
  return (zero + num).slice(-digit)
}

function updateTime() {
  const cd = new Date()
  time.value = zeroPadding(cd.getHours(), 2) + ':' + zeroPadding(cd.getMinutes(), 2) + ':' + zeroPadding(cd.getSeconds(), 2)
  date.value = zeroPadding(cd.getFullYear(), 4) + '-' + zeroPadding(cd.getMonth() + 1, 2) + '-' + zeroPadding(cd.getDate(), 2) + ' ' + week[cd.getDay()]
}

onMounted(() => {
  updateTime()
  timerID = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timerID) {
    clearInterval(timerID)
  }
})
</script>


<template>
  <div class="clock">
    <p class="date">{{ date }}</p>
    <p class="time">{{ time }}</p>
    <p class="text">DIGITAL CLOCK with Vue.js</p>
  </div>
</template>


<style scoped>
/* Google Fonts 在线字体：Share Tech Mono */
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

html,
body {
  height: 100%;
}

body {
  background: #0f3854;
  background: radial-gradient(ellipse at center, #0a2e38 0%, #000000 70%);
  background-size: 100%;
}

p {
  margin: 0;
  padding: 0;
}

.clock {
  font-family: 'Share Tech Mono', monospace;
  color: #ffffff;
  text-align: center;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  color: #daf6ff;
  text-shadow: 0 0 20px rgba(10, 175, 230, 1), 0 0 20px rgba(10, 175, 230, 0);

  .time {
    letter-spacing: 0.05em;
    font-size: 80px;
    padding: 5px 0;
  }

  .date {
    letter-spacing: 0.1em;
    font-size: 24px;
  }

  .text {
    letter-spacing: 0.1em;
    font-size: 12px;
    padding: 20px 0 0;
  }
}
</style>
