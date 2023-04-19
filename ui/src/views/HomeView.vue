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
        <RouterLink to="/login" class="nav-link py-3 underline">Log in</RouterLink>
        <RouterLink to="/add-to-slack" class="nav-link py-3 underline">Add to Slack</RouterLink>
      </template>
    </MainContent>
  </main>
</template>

<style scoped>
</style>
