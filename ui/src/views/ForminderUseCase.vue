<template>
  <div class="py-3">
    <div class="font-bold py-3">
      {{ title }}
    </div>
    <div class="py-3">
      {{ description }}
    </div>
    <div class="py-3 italic">
      {{ exampleDescription }}
    </div>
    <CodeBlock :code="code"></CodeBlock>
    <div v-if="scheduleDescription" class="py-3 italic">
      {{ scheduleDescription }}
    </div>
    <slot name="fill-form"></slot>
  </div>
</template>
<script lang="ts">
import CodeBlock from "@/components/CodeBlock.vue"

export default {
  name: 'ForminderUseCase',
  components: {CodeBlock},
  props: {
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
    exampleDescription: {
      type: String,
      required: true,
    },
    code: {
      type: String,
      required: true,
    },
    scheduleDescription: {
      type: String,
      required: false,
    }
  }
}
</script>
