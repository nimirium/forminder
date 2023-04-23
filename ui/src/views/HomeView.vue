<script setup lang="ts">
import MainContent from "@/components/MainContent.vue";
import WelcomeToForminder from "@/components/WelcomeToForminder.vue";
</script>

<template>
  <main>
    <MainContent>
      <template #default>
        <WelcomeToForminder/>
        <div class="max-w-xs md:max-w-md py-8">
          Effortlessly manage form-filling on Slack. Create customized forms, schedule reminders, and streamline your workflow with ease.
        </div>
        <RouterLink v-if="!afterLogin" to="/login" class="nav-link py-3 underline">Log in</RouterLink>
        <RouterLink to="/add-to-slack" class="nav-link py-3 underline">Add to Slack</RouterLink>
      </template>
    </MainContent>
  </main>
</template>

<script lang="ts">
import {useRoute} from "vue-router";
import {computed} from "vue";

const route = useRoute();
const afterLogin = computed(() => ['/forms', '/submissions'].includes(route.path));

export default {
  name: "HomeView",
  data: function () {
    return {
      afterLogin: afterLogin
    }

  }
}
</script>

<style scoped>
</style>
