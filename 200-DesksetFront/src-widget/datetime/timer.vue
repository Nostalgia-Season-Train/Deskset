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
const customInput = ref<number>(duration.value / 60)

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
  customInput.value = remaining.value / 60
};

// 设置自定义时间
const setCustomTime = () => {
  resetTimer()
  const input = customInput.value
  if (input > 0) {
    duration.value = input * 60
    remaining.value = duration.value;
    isCustom.value = true;
  } else {
    customInput.value = remaining.value / 60
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


/* ==== 子组件 ==== */
import { ElInputNumber } from 'element-plus'
</script>

<template>
  <div class="countdown-container">
    <div class="header">
      <div class="time-selector">

        <!-- 时间输入框 -->
        <div class="custom-input" v-if="timerState === TimerState.IDLE">
          <ElInputNumber
            v-model="customInput"
            :min="1"
            :max="10"
            @blur="setCustomTime"
            @keyup.enter="setCustomTime"
          />
        </div>

        <div class="timer-display" v-else>
          <div class="timer-value">{{ formattedTime }}</div>
        </div>

        <!-- 时间预选框 -->
        <div class="preset-buttons" v-if="timerState === TimerState.IDLE">
          <div
            v-for="minute in [1, 3, 5]" 
            :key="minute"
            class="preset-btn"
            @click="selectDuration(minute)"
          >{{ minute }}:00</div>
        </div>

      </div>
    </div>

    <div class="controls">
      <!-- 重置按钮 -->
      <button
        class="control-btn reset-btn" 
        @click="resetTimer"
      >重置</button>
      <!-- 开始/暂停/继续切换按钮 -->
      <button 
        class="control-btn start-btn" 
        @click="toggleTimer"
      >
        <span v-if="timerState === TimerState.IDLE || timerState === TimerState.PAUSED">
          {{ timerState === TimerState.IDLE ? '开始' : '继续' }}
        </span>
        <span v-else>暂停</span>
      </button>
    </div>

  </div>
</template>

<style lang="less" scoped>
@import '../style.less';

.countdown-container {
  width: fit-content;
  height: fit-content;
  .dsw-box();
  text-align: center;
  &>*:first-child {
    margin-top: 0px;
  }
  &>*:last-child {
    margin-top: 5px;
    margin-bottom: 5px;
  }

  .header {
    width: 160px;
    height: fit-content;
    display: flex;
    justify-content: center;
    align-items: center;

    .time-selector {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 3px;
      .custom-input>:deep(.el-input-number) {
        width: 124px;
        .el-input-number__decrease,
        .el-input-number__increase {
          background: transparent;
          .el-icon {
            .dsw-text-title();
            font-size: 14px;
          }
        }
        .el-input__wrapper {
          background: transparent;
          border: none;
          box-shadow: none;
          .el-input__inner {
            .dsw-text-title();
          }
        }
        .el-input__wrapper.is-focus {
          border: none;
          border-radius: 0;
          box-shadow: none;
        }
      }
      .preset-btn {
        padding: 2px 4px;
        .dsw-text-title();
        font-size: 14px;
        font-weight: 350;
        font-feature-settings: 'ss01', 'tnum';
        background: #FFF;
      }
    }
    .timer-value {
      .dsw-text-title();
      font-feature-settings: 'ss01', 'tnum';
    }
  }

  .control-btn {
    border: none;
  }
}

.preset-buttons {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.custom-input {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
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

.timer-label {
  font-size: 1.2rem;
  opacity: 0.8;
}

.controls {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
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
