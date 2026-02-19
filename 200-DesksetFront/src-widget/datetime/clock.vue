<script lang="ts" setup>
const model = defineModel<{
  clock_type: string
}>({ required: true })


import { shallowRef } from 'vue'
import DigitalClock from './clock/digital-clock.vue'
import FlipClock from './clock/flip-clock.vue'

const clock = shallowRef()

const refresh = async () => {
  if (model.value.clock_type === 'digital-clock') {
    clock.value = DigitalClock
  } else if (model.value.clock_type === 'flip-clock') {
    clock.value = FlipClock
  } else {
    clock.value = DigitalClock
  }
}
refresh()


import { watch } from 'vue'

watch(model.value, refresh)
</script>


<template>
<div class="clock">
  <component :is="clock"/>
</div>
</template>
