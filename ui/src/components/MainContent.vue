<template>
  <div class="flex flex-col">
    <h1 v-if="title" class="page-title">{{ title }}</h1>
    <div class="center flex items-center justify-center">
      <ForminderBigImage :hide-image-if-small="hideImageIfSmall"/>
      <div class="flex flex-col items-start justify-center">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
import ForminderBigImage from "@/components/ForminderBigImage.vue";
export default {
  name: "MainContent",
  components: {ForminderBigImage},
  props: {
    title: {
      type: String,
      required: false,
    },
    hideImageIfSmall: {
      type: Boolean,
      required: false,
      default: false,
    }
  },
}
</script>

<style scoped>
.page-title {
  font-family: 'Lobster Two', cursive;
  font-size: 2.7rem;
  font-weight: 700;
  text-align: center;
  padding-top: 25px;

}
</style>
