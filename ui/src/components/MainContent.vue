<template>
  <div class="flex flex-col">
    <h1 v-if="title" class="page-title">{{ title }}</h1>
    <div class="center flex items-center justify-center">
      <slot name="image">
        <BigImage :image="image" :hide-image-if-small="hideImageIfSmall"></BigImage>
      </slot>
      <div class="flex flex-col items-start justify-center">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
import BigImage from "@/components/BigImage.vue";
import forminderImageUrl from '@/assets/forminder_no_bg.png';

export default {
  name: "MainContent",
  components: {BigImage},
  props: {
    title: {
      type: String,
      required: false,
    },
    hideImageIfSmall: {
      type: Boolean,
      required: false,
      default: false,
    },
    image: {
      type: String,
      required: false,
      default: forminderImageUrl,
    }
  },
}
</script>

<style scoped>
</style>
