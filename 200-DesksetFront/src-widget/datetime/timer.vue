<!-- Qwen3-Max 编写，待修改 -->

<script lang="ts" setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

// 定义倒计时状态枚举
const TimerState = {
  IDLE: 'idle',
  RUNNING: 'running',
  PAUSED: 'paused'
};

const props = defineProps({
  initialDuration: {
    type: Number,
    default: 60
  }
});

const duration = ref(props.initialDuration);
const remaining = ref(duration.value);
const timerState = ref(TimerState.IDLE); // 使用状态枚举
const timer = ref<number | null>(null);
const isCustom = ref(false);
const customInput = ref('');

// 格式化时间
const formattedTime = computed(() => {
  const seconds = remaining.value % 60;
  const minutes = Math.floor(remaining.value / 60) % 60;
  const hours = Math.floor(remaining.value / 3600);
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
});

// 选择预设时间
const selectDuration = (minutes: number) => {
  resetTimer()
  duration.value = minutes * 60;
  remaining.value = duration.value;
  isCustom.value = false;
  customInput.value = '';
};

// 设置自定义时间
const setCustomTime = () => {
  resetTimer()
  const input = parseInt(customInput.value);
  if (input > 0) {
    duration.value = input;
    remaining.value = duration.value;
    isCustom.value = true;
  }
};

// 开始/暂停倒计时
const toggleTimer = () => {
  if (timerState.value === TimerState.IDLE || timerState.value === TimerState.PAUSED) {
    // 开始或继续
    if (remaining.value <= 0) {
      remaining.value = duration.value; // 重置为初始值
    }
    timerState.value = TimerState.RUNNING;
    timer.value = setInterval(() => {
      remaining.value--;
      if (remaining.value <= 0) {
        if (timer.value != null)
          clearInterval(timer.value);
        timerState.value = TimerState.IDLE;
      }
    }, 1000);
  } else {
    // 暂停
    if (timer.value != null)
      clearInterval(timer.value);
    timerState.value = TimerState.PAUSED;
  }
};

// 重置倒计时
const resetTimer = () => {
  if (timer.value != null)
    clearInterval(timer.value);
  remaining.value = duration.value;
  timerState.value = TimerState.IDLE;
};

// 从props更新初始时间
const updateInitialDuration = () => {
  duration.value = props.initialDuration;
  remaining.value = props.initialDuration;
};

onMounted(() => {
  updateInitialDuration();
});

onBeforeUnmount(() => {
  if (timer.value) clearInterval(timer.value);
});
</script>

<template>
  <div class="countdown-container">
    <div class="header">
      <h2>倒计时</h2>
      <div class="time-selector">
        <div class="preset-buttons">
          <button 
            v-for="minute in [1, 3, 5]" 
            :key="minute"
            :class="['preset-btn', { active: duration === minute * 60 }]"
            @click="selectDuration(minute)"
          >
            {{ minute }}分钟
          </button>
        </div>

        <div class="custom-input">
          <input
            v-model="customInput"
            type="number"
            min="1"
            placeholder="自定义秒数"
            @keyup.enter="setCustomTime"
          />
          <button class="custom-btn" @click="setCustomTime">
            设置
          </button>
        </div>
      </div>
    </div>

    <div class="timer-display">
      <div class="timer-value">{{ formattedTime }}</div>
      <div class="timer-label">剩余时间</div>
    </div>

    <div class="controls">
      <button 
        class="control-btn start-btn" 
        @click="toggleTimer"
      >
        <span v-if="timerState === TimerState.IDLE || timerState === TimerState.PAUSED">
          {{ timerState === TimerState.IDLE ? '开始' : '继续' }}
        </span>
        <span v-else>暂停</span>
      </button>

      <button
        class="control-btn reset-btn" 
        @click="resetTimer"
      >
        重置
      </button>
    </div>
  </div>
</template>

<style scoped>
.countdown-container {
  background: linear-gradient(135deg, #4b6cf1, #3f8efc);
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(75, 108, 241, 0.4);
  padding: 2rem;
  max-width: 400px;
  width: 100%;
  margin: 0 auto;
  color: white;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
}

.header {
  margin-bottom: 1.5rem;
}

h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.time-selector {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.preset-buttons {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.preset-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 12px;
  padding: 0.7rem 1.2rem;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  color: white;
  backdrop-filter: blur(10px);
}

.preset-btn.active {
  background: rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.custom-input {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.custom-input input {
  flex: 1;
  padding: 0.7rem 1rem;
  border-radius: 12px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.custom-input input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.custom-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 12px;
  padding: 0.7rem 1.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  backdrop-filter: blur(10px);
}

.custom-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.timer-display {
  margin: 2rem 0;
}

.timer-value {
  font-size: 3.5rem;
  font-weight: bold;
  letter-spacing: 2px;
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  margin-bottom: 0.5rem;
}

.timer-label {
  font-size: 1.2rem;
  opacity: 0.8;
}

.controls {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
}

.control-btn {
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.start-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.start-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.start-btn:active {
  transform: scale(0.98);
}

.reset-btn {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.reset-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.reset-btn:active {
  transform: scale(0.98);
}
</style>
