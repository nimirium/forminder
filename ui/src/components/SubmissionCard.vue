<template>
  <div class="mygrid-item opacity-75 p-7 rounded-xl shadow-md w-full md:w-1/3 lg:w-1/4 m-4">
    <div class="p-2">
      <div>
        Submitted by {{ submission.user_name }}
      </div>
      <div>
        on {{ submission.formatted_date }} at {{ submission.formatted_time }}
      </div>
    </div>

    <div v-for="field in submission.fields" :key="field.id" class="p-2">
      <div class="font-semibold">
        {{ field.title }}
      </div>
      <div>
        {{ field.value }}
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import type { PropType } from "vue";
import type {Submission} from "@/types/submissions";

export default defineComponent({
  props: {
    submission: {
      type: Object as PropType<Submission>,
      required: true,
    },
  },
});
</script>
