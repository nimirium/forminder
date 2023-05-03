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
            v-if="page > 1"
            @click="changePage(1)"
            class="p-3"
        >
          First
        </button>
        <button
            v-if="page > 1"
            @click="changePage(page - 1)"
            class="p-3"
        >
          Previous
        </button>
        <span class="p-3">
        Page {{ page }} of {{ lastPage }}
      </span>
        <button
            v-if="page < lastPage"
            @click="changePage(page + 1)"
            class="p-3"
        >
          Next
        </button>
        <button
            v-if="page < lastPage"
            @click="changePage(lastPage)"
            class="p-3"
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
          ? "/export-submissions-csv"
          : "/export-submissions-xlsx";
      window.location.href = exportUrl;
    };

    const fetchSubmissions = async () => {
      const response = await fetch(
        `/api/v1/submissions?formId=${formId}&page=${page.value}&per_page=${perPage.value}`
      );

      loading.value = false;

      if (response.ok) {
        const data = await response.json();
        // const data = {
        //   "form_name": "Dogs form",
        //   "page": 1,
        //   "per_page": 10,
        //   "submissions": [{
        //     "created_at": "2023-04-03T10:35:42.103000",
        //     "fields": [{"title": "Are you bringing your dog to work tomorrow?", "value": "Yes"}, {
        //       "title": "Dog name",
        //       "value": "Doggie"
        //     }, {"title": "Is your dog friendly with other dogs?", "value": "Yes"}],
        //     "form_id": "642aabdb1ef24e18c6d95fab",
        //     "formatted_date": "Apr. 3, 2023",
        //     "formatted_time": "10:35",
        //     "id": "642aabfe7af57bab8b74f38d",
        //     "user_id": "U02RCUYKPK4",
        //     "user_name": "sophie.fogel"
        //   }, {
        //     "created_at": "2023-04-17T18:54:31.048000",
        //     "fields": [{"title": "Dog name", "value": "sfsdf"}, {
        //       "title": "Is your dog friendly with other dogs?",
        //       "value": "fhgfgh"
        //     }, {"title": "Are you bringing your dog to work tomorrow?", "value": "No"}],
        //     "form_id": "642aabdb1ef24e18c6d95fab",
        //     "formatted_date": "Apr. 17, 2023",
        //     "formatted_time": "18:54",
        //     "id": "643d6bb7f02800015e0d3c44",
        //     "user_id": "U02RCUYKPK4",
        //     "user_name": "sophie.fogel"
        //   }, {
        //     "created_at": "2023-04-17T18:54:45.590000",
        //     "fields": [{"title": "Dog name", "value": "ertert"}, {
        //       "title": "Is your dog friendly with other dogs?",
        //       "value": "asdasd"
        //     }, {"title": "Are you bringing your dog to work tomorrow?", "value": "No"}],
        //     "form_id": "642aabdb1ef24e18c6d95fab",
        //     "formatted_date": "Apr. 17, 2023",
        //     "formatted_time": "18:54",
        //     "id": "643d6bc5f02800015e0d3c45",
        //     "user_id": "U02RCUYKPK4",
        //     "user_name": "sophie.fogel"
        //   }, {
        //     "created_at": "2023-04-17T18:55:18.489000",
        //     "fields": [{"title": "Dog name", "value": "etert"}, {
        //       "title": "Is your dog friendly with other dogs?",
        //       "value": "fgdgd"
        //     }, {"title": "Are you bringing your dog to work tomorrow?", "value": "Yes"}],
        //     "form_id": "642aabdb1ef24e18c6d95fab",
        //     "formatted_date": "Apr. 17, 2023",
        //     "formatted_time": "18:55",
        //     "id": "643d6be6f02800015e0d3c46",
        //     "user_id": "U02RCUYKPK4",
        //     "user_name": "sophie.fogel"
        //   }, {
        //     "created_at": "2023-04-17T18:55:31.831000",
        //     "fields": [{"title": "Dog name", "value": "ertret"}, {
        //       "title": "Is your dog friendly with other dogs?",
        //       "value": "qw"
        //     }, {"title": "Are you bringing your dog to work tomorrow?", "value": "Yes"}],
        //     "form_id": "642aabdb1ef24e18c6d95fab",
        //     "formatted_date": "Apr. 17, 2023",
        //     "formatted_time": "18:55",
        //     "id": "643d6bf3f02800015e0d3c47",
        //     "user_id": "U02RCUYKPK4",
        //     "user_name": "sophie.fogel"
        //   }, {
        //     "created_at": "2023-04-17T18:55:48.752000",
        //     "fields": [{"title": "Dog name", "value": "yrtyrt"}, {
        //       "title": "Is your dog friendly with other dogs?",
        //       "value": "ghjghj"
        //     }, {"title": "Are you bringing your dog to work tomorrow?", "value": "No"}],
        //     "form_id": "642aabdb1ef24e18c6d95fab",
        //     "formatted_date": "Apr. 17, 2023",
        //     "formatted_time": "18:55",
        //     "id": "643d6c04f02800015e0d3c48",
        //     "user_id": "U02RCUYKPK4",
        //     "user_name": "sophie.fogel"
        //   }, {
        //     "created_at": "2023-04-17T18:56:00.230000",
        //     "fields": [{"title": "Dog name", "value": "qweqwe"}, {
        //       "title": "Is your dog friendly with other dogs?",
        //       "value": "fghfgh"
        //     }, {"title": "Are you bringing your dog to work tomorrow?", "value": "Yes"}],
        //     "form_id": "642aabdb1ef24e18c6d95fab",
        //     "formatted_date": "Apr. 17, 2023",
        //     "formatted_time": "18:56",
        //     "id": "643d6c10f02800015e0d3c49",
        //     "user_id": "U02RCUYKPK4",
        //     "user_name": "sophie.fogel"
        //   }, {
        //     "created_at": "2023-04-17T18:56:20.480000",
        //     "fields": [{"title": "Dog name", "value": "trty"}, {
        //       "title": "Is your dog friendly with other dogs?",
        //       "value": "fghfgh"
        //     }, {"title": "Are you bringing your dog to work tomorrow?", "value": "Yes"}],
        //     "form_id": "642aabdb1ef24e18c6d95fab",
        //     "formatted_date": "Apr. 17, 2023",
        //     "formatted_time": "18:56",
        //     "id": "643d6c24f02800015e0d3c4a",
        //     "user_id": "U02RCUYKPK4",
        //     "user_name": "sophie.fogel"
        //   }, {
        //     "created_at": "2023-04-17T18:56:29.305000",
        //     "fields": [{"title": "Dog name", "value": "wrwer"}, {
        //       "title": "Is your dog friendly with other dogs?",
        //       "value": "fghfgh"
        //     }, {"title": "Are you bringing your dog to work tomorrow?", "value": "Yes"}],
        //     "form_id": "642aabdb1ef24e18c6d95fab",
        //     "formatted_date": "Apr. 17, 2023",
        //     "formatted_time": "18:56",
        //     "id": "643d6c2df02800015e0d3c4b",
        //     "user_id": "U02RCUYKPK4",
        //     "user_name": "sophie.fogel"
        //   }, {
        //     "created_at": "2023-04-17T18:56:39.064000",
        //     "fields": [{"title": "Dog name", "value": "qweqwe"}, {
        //       "title": "Is your dog friendly with other dogs?",
        //       "value": "ertret"
        //     }, {"title": "Are you bringing your dog to work tomorrow?", "value": "Yes"}],
        //     "form_id": "642aabdb1ef24e18c6d95fab",
        //     "formatted_date": "Apr. 17, 2023",
        //     "formatted_time": "18:56",
        //     "id": "643d6c37f02800015e0d3c4c",
        //     "user_id": "U02RCUYKPK4",
        //     "user_name": "sophie.fogel"
        //   }],
        //   "total": 11
        // };

        formName.value = data.form_name;
        submissions.value = data.submissions;
        lastPage.value = data.total;
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
