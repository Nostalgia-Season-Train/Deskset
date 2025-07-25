<script lang='ts' setup>
/* === Props === */
const { onClose, onCancel, onConfirm } = defineProps<{
  title: string,
  content: string,
  placeholder: string,
  cancel: string,
  confirm: string,

  onDestory: Function,

  onClose: Function,
  onCancel: Function,
  onConfirm: Function
}>()


/* === Hook === */
  // 组件挂载：render(vnode) > onMounted > show true > Transition 渐入动画
  // 组件卸载：show false > Transition 渐出动画 > onDestory > render(null) > onUnmounted
import { ref, onMounted } from 'vue'

const is_show = ref(false)

onMounted(() => {
  is_show.value = true
})

const areaClose = () => {
  onCancel()
  is_show.value = false
}
const btnCancel = () => {
  onClose()
  is_show.value = false
}

const input = ref('')

const btnConfirm = () => {
  onConfirm(input.value)
  is_show.value = false
}


/* === 子组件 === */
import Button from './Button.vue'
import Input from './Input.vue'
</script>


<template>
<transition @after-leave="onDestory()"><!-- 由 v-if 变化触发 -->
<div class="container" @click="areaClose()" v-if="is_show">
  <div class="message" @click.stop><!-- stop 阻止子元素事件向上传递 -->

    <div class="text">
      <div class="title">{{ title }}</div>
      <div class="content">{{ content }}</div>
      <div class="input"><Input v-model="input" :placeholder="placeholder"/></div>
    </div>

    <div class="btn">
      <div class="cancel" @click="btnCancel()">
        <Button>{{ cancel }}</Button>
      </div>
      <div class="confirm" @click="btnConfirm()">
        <Button>{{ confirm }}</Button>
      </div>
    </div>

  </div>
</div>
</transition>
</template>


<style lang="less" scoped>
// 渐入渐出动画
.v-enter-active,
.v-leave-active {
  transition: .3s ease;
}
.v-enter-from,
.v-leave-to {
  opacity: 0;
}

.container {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 3;  // 比 aside 高 1 index

  width: 100vw;
  height: 100vh;
  max-width: 100vw;
  max-height: 100vh;
  user-select: none;

  background-color: #000A;
  backdrop-filter: blur(1px);

  .message {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-49.9%, -50%);  // 50% 会使左右边框跟上下边框粗细不一致（包括按钮）

    width: 420px;
    height: 128px;
    border: solid 1px rgba(#FFF, .5);
    background: #0009;

    .text {
      position: absolute;
      top: 5px;
      left: 10px;

      .title {
        color: #FFF;
        font-size: 20px;
      }
      .content {
        color: #FFFA;
        font-size: 16px;
      }
      .input {
        width: 240px;
        &>* {
          width: 100%;
        }
      }
    }
    .btn {
      position: absolute;
      bottom: 10px;
      right: 10px;

      display: flex;
      justify-content: space-between;
      gap: 5px;
    }
  }
}
</style>
