<template>
  <div class="flex py-4 items-center">
    <div class="max-w-xs md:max-w-md mr-2.5">
      {{ text }}
    </div>
    <CodeBlock :code="code"></CodeBlock>
    <div v-if="textAfter" class="max-w-xs md:max-w-md ml-2.5">
      {{ textAfter }}
    </div>
  </div>
</template>

<script>
import CodeBlock from "./CodeBlock.vue";
export default {
  name: "TextAndCode",
  components: {CodeBlock},
  props: {
    text: {
      type: String,
      required: true,
    },
    code: {
      type: String,
      required: true,
    },
    textAfter: {
      type: String,
      required: false,
    },
  }
}
</script>

<style scoped>

</style>
