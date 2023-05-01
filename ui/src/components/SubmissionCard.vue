<template>
  <div>
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
        {{ field.display_title }}
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

interface SubmissionField {
  id: string;
  display_title: string;
  value: string;
}

interface Submission {
  id: string;
  user_name: string;
  formatted_date: string;
  formatted_time: string;
  fields: SubmissionField[];
}

export default defineComponent({
  props: {
    submission: {
      type: Object as PropType<Submission>,
      required: true,
    },
  },
});
</script>

