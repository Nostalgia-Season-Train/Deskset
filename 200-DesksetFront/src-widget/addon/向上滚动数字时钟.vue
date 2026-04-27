<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const date = ref(new Date())

let interval = null

onMounted(() => {
  interval = setInterval(() => {
    const update = new Date()

    if (update.getSeconds() !== date.value.getSeconds()) {
      date.value = update
    }
  }, 100)
})

onUnmounted(() => {
  if (interval) {
    clearInterval(interval)
  }
})

const formatSegment = (segment) => {
  return segment < 10 ? `0${segment}` : String(segment)
}

const getHours = (hours) => {
  return hours % 12 === 0 ? 12 : hours % 12
}

const timeString = computed(() => {
  const hours = getHours(date.value.getHours())
  const minutes = date.value.getMinutes()
  const seconds = date.value.getSeconds()

  return `${formatSegment(hours)}:${formatSegment(minutes)}:${formatSegment(seconds)}`
})

const chars = computed(() => {
  return timeString.value.split('')
})

const timerCharRefs = ref([])

const getSliderTop = (char, index) => {
  if (char === ':') return '0px'

  const number = parseInt(char)
  const height = timerCharRefs.value[index]?.offsetHeight || 0

  return `${number * height * -1}px`
}
</script>


<template>
  <div id="app">
    <div id="timer">
      <div id="timer-text">
        <div
          v-for="(char, index) in chars"
          :key="index"
          :ref="(el) => timerCharRefs[index] = el"
          :class="['timer-char', char === ':' ? 'colon' : 'number']"
        >
          <h1 v-if="char === ':'" class="timer-char colon">:</h1>
          <div v-else class="timer-char-slider" :style="{ top: getSliderTop(char, index) }">
            <span
              v-for="i in 10"
              :key="i - 1"
              :class="['timer-char-slider-option', { active: parseInt(char) === i - 1 }]"
            >
              {{ i - 1 }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400&display=swap');

body {
  background-color: #1e1e1e;
  margin: 0px;
  overflow: hidden;
  padding: 0px;
}

body input,
body h1,
body a,
body span {
  color: #5a5a5a;
  font-family: "Rubik", sans-serif;
  font-weight: 400;
  margin: 0px;
  padding: 0px;
}

#app {
  align-items: center;
  display: flex;
  height: 100vh;
  justify-content: center;
  width: 100vw;
}

#app #timer {
  background: linear-gradient(to bottom right, #0263e1, #eb1836);
  border-radius: 22px;
}

#app #timer #timer-text {
  align-items: center;
  background-color: #1e1e1e;
  border-radius: 20px;
  display: flex;
  margin: 4px;
  padding: 0px 20px;
}

#app #timer #timer-text .timer-char {
  height: 150px;
  position: relative;
  text-align: center;
  width: 80px;
}

#app #timer #timer-text .timer-char.colon {
  color: white;
  font-size: 3em;  /* 分隔符 : 大小，原始 8em 太大原因未知 */
  line-height: 150px;
}

#app #timer #timer-text .timer-char .timer-char-slider {
  display: flex;
  flex-direction: column;
  left: 0px;
  position: absolute;
  top: 0px;
  transition: top 200ms;
  width: 80px;
}

#app #timer #timer-text .timer-char .timer-char-slider .timer-char-slider-option {
  color: white;
  font-size: 4em;
  height: 150px;
  line-height: 150px;
  opacity: 0.05;
  transition: opacity 400ms, font-size 400ms;
  width: 80px;
}

#app #timer #timer-text .timer-char .timer-char-slider .timer-char-slider-option.active {
  font-size: 8em;
  opacity: 1;
}

@media (max-width: 800px) {
  #app #timer {
    border-radius: 16px;
  }

  #app #timer #timer-text {
    border-radius: 14px;
    margin: 4px;
    padding: 0px 12px;
  }

  #app #timer #timer-text .timer-char {
    height: 80px;
    width: 40px;
  }

  #app #timer #timer-text .timer-char.colon {
    font-size: 4em;
    line-height: 80px;
  }

  #app #timer #timer-text .timer-char .timer-char-slider {
    width: 40px;
  }

  #app #timer #timer-text .timer-char .timer-char-slider .timer-char-slider-option {
    font-size: 2em;
    height: 80px;
    line-height: 80px;
    width: 40px;
  }

  #app #timer #timer-text .timer-char .timer-char-slider .timer-char-slider-option.active {
    font-size: 4em;
  }
}

@media (max-width: 400px) {
  #app #timer {
    border-radius: 8px;
  }

  #app #timer #timer-text {
    border-radius: 6px;
    margin: 2px;
    padding: 0px 10px;
  }

  #app #timer #timer-text .timer-char {
    height: 40px;
    width: 20px;
  }

  #app #timer #timer-text .timer-char.colon {
    font-size: 2em;
    line-height: 40px;
  }

  #app #timer #timer-text .timer-char .timer-char-slider {
    width: 20px;
  }

  #app #timer #timer-text .timer-char .timer-char-slider .timer-char-slider-option {
    font-size: 1.25em;
    height: 40px;
    line-height: 40px;
    width: 20px;
  }

  #app #timer #timer-text .timer-char .timer-char-slider .timer-char-slider-option.active {
    font-size: 2em;
  }
}
</style>
