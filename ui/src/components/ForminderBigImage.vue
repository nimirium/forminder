<template>
  <div class="w-1/2 max-w-2xl" :class="{ hidden: hideImageIfSmall, 'lg:block': hideImageIfSmall }">
    <img src="@/assets/forminder_no_bg.png" alt="Forminder">
  </div>
</template>

<script lang="ts">
export default {
  name: "ForminderBigImage",
  props: {
    hideImageIfSmall: {
      type: Boolean,
      required: false,
      default: false
    },
  }
}
</script>

<style scoped>

</style>
