<script setup>
const pageDesktop = new BroadcastChannel('pageDesktop')

pageDesktop.onmessage = async (event) => {
  console.log(event.data.action)
}
</script>


<template>
  Desktop
</template>
