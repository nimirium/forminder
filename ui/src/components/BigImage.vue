<template>
  <div class="w-1/2 max-w-2xl" :class="{ hidden: hideImageIfSmall, 'lg:block': hideImageIfSmall }">
    <img :src="image" alt="Forminder">
  </div>
</template>

<script lang="ts">
export default {
  name: "BigImage",
  props: {
    image: {
      type: String,
      required: true
    },
    hideImageIfSmall: {
      type: Boolean,
      required: false,
      default: false
    }
  }
}
</script>

<style scoped>
</style>
