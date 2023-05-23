<!-- FormSubmissions.vue -->
<template>
  <div v-if="!loading" class="w-full text-3xl text-center p-5">
    <span class="text-3xl">{{formName}} - Submissions</span>
  </div>
  <div v-if="loading" class="loading-indicator">
    Loading...
  </div>
  <div>
    <div class="flex justify-around">
      <div v-if="!loading">
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
            class="bg-greenish p-2 m-1 rounded"
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
          v-if="!loading && !submissions.length"
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
    <div v-if="!loading" class="flex justify-center">
      <div class="m-3">
        <button
            v-if="page > 1"
            @click="changePage(1)"
            class="p-3 underline"
        >
          First
        </button>
        <button
            v-if="page > 1"
            @click="changePage(page - 1)"
            class="p-3 underline"
        >
          Previous
        </button>
        <span class="p-3">
        Page {{ page }} of {{ lastPage }}
      </span>
        <button
            v-if="page < lastPage"
            @click="changePage(page + 1)"
            class="p-3 underline"
        >
          Next
        </button>
        <button
            v-if="page < lastPage"
            @click="changePage(lastPage)"
            class="p-3 underline"
        >
          Last
        </button>
      </div>
    </div>
    <!-- /Pagination -->
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import SubmissionCard from "@/components/SubmissionCard.vue";
import { useRoute } from "vue-router";
import type { Submission } from "@/types/submissions";
import {apiURL} from "@/config/config";


export default defineComponent({
  components: {
    SubmissionCard,
  },
  setup() {
    const slashCommand = ref(import.meta.env.VITE_SLASH_COMMAND as string);

    const loading = ref<Boolean>(true);
    const exportType = ref("csv");
    const submissions = ref<Submission[]>([]);
    const page = ref(1);
    const perPage = ref(10);
    const lastPage = ref(1);
    const route = useRoute();
    const formId = route.query.formId as string;
    const formName = ref<String>();

    const downloadData = () => {
      const exportUrl =
        exportType.value === "csv"
          ? apiURL + "/api/v1/submissions/export/csv?formId=" + formId
          : apiURL + "/api/v1/submissions/export/xlsx?formId=" + formId;
      window.location.href = exportUrl;
    };

    const fetchSubmissions = async () => {
      const response = await fetch(
          apiURL + `/api/v1/submissions?formId=${formId}&page=${page.value}&per_page=${perPage.value}`
      );

      loading.value = false;

      if (response.ok) {
        const data = await response.json();
        formName.value = data.form_name;
        submissions.value = data.submissions;
        lastPage.value = Math.floor(data.total / perPage.value) + (data.total % perPage.value > 0 ? 1 : 0);
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
      loading,
      formName,
      slashCommand,
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
