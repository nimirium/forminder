<template>
  <div>
    <div class="flex flex-wrap justify-center place-content-evenly">
      <div
          v-for="form in forms"
          :key="form.id"
          class="mygrid-item opacity-75 p-7 rounded-xl shadow-md w-full md:w-1/3 lg:w-1/4 p-4 max-w-lg p-5 m-5"
      >
        <div class="font-semibold text-xl p-1">{{ form.name }}</div>
        <div class="p-1">Created by {{ form.user_name }}</div>
        <div class="p-1">
          <ul class="list-disc pl-5">
            <li v-for="field in form.fields" :key="field.id">{{ field.title }}</li>
          </ul>
        </div>
        <div class="font-semibold p-1">
          Submissions: {{ form.number_of_submissions }}
        </div>

        <button
            class="bg-greenish rounded-xl p-3 my-2 font-bold shadow-md"
            style="color: #ffffff"
        >
          <router-link :to="`/submissions?formId=${form.id}`">View submissions</router-link>
        </button>
      </div>

      <div v-if="forms.length === 0" class="mygrid-item opacity-75 p-7 rounded-xl shadow-md w-full md:w-1/3 lg:w-1/4 p-4">
        <div class="p-1">You don't have any forms.</div>
        <div class="p-1">Create a form in slack by running:</div>
        <div class="p-1 code">/{{ slashCommand }} create</div>
      </div>
    </div>

    <!-- Pagination -->
    <div class="flex justify-center">
      <div class="m-3">
        <template v-if="page > 1">
          <router-link
              :to="{ name: 'forms', query: { page: 1, per_page: per_page } }"
              class="p-3 underline"
          >First</router-link>
          <router-link
              :to="{ name: 'forms', query: { page: page - 1, per_page: per_page } }"
              class="p-3 underline"
          >Previous</router-link>
        </template>
        <span class="p-3">
          Page {{ page }} of {{ total }}
        </span>
        <template v-if="page < total">
          <router-link
              :to="{ name: 'forms', query: { page: page + 1, per_page: per_page } }"
              class="p-3 underline"
          >Next</router-link>
          <router-link
              :to="{ name: 'forms', query: { page: total, per_page: per_page } }"
              class="p-3 underline"
          >Last</router-link>
        </template>
      </div>
    </div>
    <!-- /Pagination -->
  </div>
</template>


<script lang="ts">
import { defineComponent } from "vue";
import type { Form } from "@/types/form";

export default defineComponent({
  name: "FormsView",
  data() {
    return {
      forms: [] as Form[],
      page: 1,
      per_page: 10,
      total: 0,
      slashCommand: import.meta.env.VITE_SLASH_COMMAND,
    };
  },
  async created() {
    await this.fetchForms();
  },
  methods: {
    async fetchForms() {
      try {
        const response = await fetch(
            `/api/v1/forms?page=${this.page}&per_page=${this.per_page}`
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        this.forms = data.forms;
        this.page = data.page;
        this.per_page = data.per_page;
        this.total = data.total;
      } catch (error) {
        console.error(error);
      }
    },
  },
});

</script>

<style scoped>
/* Add your styles here */
</style>
