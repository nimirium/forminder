<script setup lang="ts">
import WelcomeToForminder from "@/components/WelcomeToForminder.vue";
import AddToSlackButton from "@/components/AddToSlackButton.vue";
import MainContent from "@/components/MainContent.vue";
</script>

<template>

  <main>
    <MainContent>
      <template #default>
        <WelcomeToForminder/>
        <div class="max-w-xs md:max-w-md py-8">
          Get started by adding Forminder to your Slack workspace
        </div>
        <AddToSlackButton/>
      </template>
    </MainContent>
  </main>
</template>

<style>
</style>
