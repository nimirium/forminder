<!-- FormSubmissions.vue -->
<template>
  <div>
    <div class="flex justify-around">
      <div>
        <span>
          Export as
        </span>
        <select
            name="export"
            id="export"
            class="p-2 m-1 rounded-md shadow"
            v-model="exportType"
        >
          <option value="csv">CSV</option>
          <option value="xlsx">XLSX</option>
        </select>
        <button
            id="download-btn"
            class="mybutton p-2 m-1 rounded"
            @click="downloadData"
        >
          Download
        </button>
      </div>
    </div>

    <div class="flex flex-wrap justify-center place-content-evenly">
      <SubmissionCard
          v-for="submission in submissions"
          :key="submission.id"
          :submission="submission"
      />

      <div
          v-if="!submissions.length"
          class="mygrid-item opacity-75 p-7 rounded-xl shadow-md w-full md:w-1/3 lg:w-1/4 p-4"
      >
        <div class="p-1">
          There are no submissions for this form.
        </div>
        <div class="p-1">
          Schedule the form in slack by running:
        </div>
        <div class="p-1 code">
          /{{ slashCommand }} list
        </div>
        <div class="p-1">
          and then pressing "Schedule".
        </div>
        <div class="p-1">
          Or fill it without scheduling by pressing "Fill now".
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div class="flex justify-center">
      <div class="m-3">
        <button
            :disabled="page === 1"
            @click="changePage(page - 1)"
            class="p-3"
        >
          Previous
        </button>
        <span class="p-3">
        Page {{ page }} of {{ lastPage }}
      </span>
        <button
            :disabled="page === lastPage"
            @click="changePage(page + 1)"
            class="p-3"
        >
          Next
        </button>
      </div>
    </div>
    <!-- /Pagination -->
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import SubmissionCard from "@/components/SubmissionCard.vue";
import {useRoute} from "vue-router";

export default defineComponent({
  components: {
    SubmissionCard,
  },
  data() {
    return {
      slashCommand: import.meta.env.VITE_SLASH_COMMAND
    }
  },
  setup() {
    const exportType = ref("csv");
    const submissions = ref([]);
    const page = ref(1);
    const perPage = ref(10);
    const lastPage = ref(1);
    const route = useRoute();
    const formId = route.query.formId as string;

    const downloadData = () => {
      const exportUrl =
          exportType.value === "csv"
              ? "/export-submissions-csv"
              : "/export-submissions-xlsx";
      window.location.href = exportUrl;
    };

    const fetchSubmissions = async () => {
      const response = await fetch(
          `/api/v1/submissions?formId=${formId}&page=${page.value}&per_page=${perPage.value}`
      );

      if (response.ok) {
        const data = await response.json();
        submissions.value = data.submissions;
        lastPage.value = data.last_page;
      }
    };

    const changePage = (newPage: number) => {
      page.value = newPage;
      fetchSubmissions();
    };

    onMounted(() => {
      fetchSubmissions();
    });

    return {
      exportType,
      submissions,
      downloadData,
      page,
      lastPage,
      changePage,
    };
  },
});
</script>

<style scoped>
body {
  color: #632616;
  font-family: sans-serif;
  background-color: #D7CDC3;
}

.mygrid-item {
  background-color: #f5f5f5;
}

.bg-greenish {
  background-color: #ACBFA5;
}

.code {
  font-family: 'Source Code Pro', monospace;
  color: black;
}

.loading-indicator {
  /* Custom styles for the loading indicator */
  text-align: center;
  font-size: 1.5rem;
  margin: 2rem 0;
}
</style>
