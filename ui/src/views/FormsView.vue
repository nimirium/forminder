<template>
  <div>
    <div class="w-full text-3xl text-center p-5">
      <span class="text-3xl">Forms</span>
    </div>
    <div v-if="loading" class="loading-indicator">
      Loading...
    </div>
    <div v-if="!loading" class="flex flex-wrap justify-center place-content-evenly">
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

      <div v-if="!loading && forms.length === 0"
           class="mygrid-item opacity-75 p-7 rounded-xl shadow-md w-full md:w-1/3 lg:w-1/4 p-4">
        <div class="p-1">You don't have any forms.</div>
        <div class="p-1">Create a form in slack by running:</div>
        <div class="p-1 code">/{{ slashCommand }} create</div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="!loading" class="flex justify-center">
      <div class="m-3">
        <template v-if="page > 1">
          <router-link
              :to="{ name: 'forms', query: { page: 1, per_page: per_page } }"
              class="p-3 underline"
          >First
          </router-link>
          <router-link
              :to="{ name: 'forms', query: { page: page - 1, per_page: per_page } }"
              class="p-3 underline"
          >Previous
          </router-link>
        </template>
        <span class="p-3">
          Page {{ page }} of {{ last_page }}
        </span>
        <template v-if="page < last_page">
          <router-link
              :to="{ name: 'forms', query: { page: page + 1, per_page: per_page } }"
              class="p-3 underline"
          >Next
          </router-link>
          <router-link
              :to="{ name: 'forms', query: { page: last_page, per_page: per_page } }"
              class="p-3 underline"
          >Last
          </router-link>
        </template>
      </div>
    </div>
    <!-- /Pagination -->
  </div>
</template>


<script lang="ts">
import {defineComponent, getCurrentInstance, watch} from "vue";
import type {Form} from "@/types/form";
import {apiURL} from "@/config/config";
import {logout} from "@/util/login-and-logout";

export default defineComponent({
  name: "FormsView",
  data() {
    const page = parseInt(this.$route.query.page as string, 10) || 1;
    const per_page = parseInt(this.$route.query.per_page as string, 10) || 10;

    return {
      loading: true,
      forms: [] as Form[],
      page,
      per_page,
      total: 0,
      last_page: 1,
      slashCommand: import.meta.env.VITE_SLASH_COMMAND,
    };
  },
  methods: {
    async fetchForms() {
      this.loading = true;
      try {
        const response = await fetch(
            apiURL + `/api/v1/forms?page=${this.page}&per_page=${this.per_page}`
        );
        if (response.status === 401) {
          logout();
          return;
        }
        if (!response.ok) {
          this.loading = false;
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        this.forms = data.forms;
        this.page = data.page;
        this.per_page = data.per_page;
        this.total = data.total;
        this.loading = false;
        this.last_page = Math.floor(this.total / this.per_page) + (this.total % this.per_page > 0 ? 1 : 0);
      } catch (error) {
        console.error(error);
        this.loading = false;
      }
    },
  },
  watch: {
    $route: {
      async handler() {
        this.page = parseInt(this.$route.query.page as string, 10) || 1;
        this.per_page = parseInt(this.$route.query.per_page as string, 10) || 10;
        await this.fetchForms();
      },
      immediate: true,
    },
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
