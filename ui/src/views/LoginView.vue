<script setup lang="ts">
import SignInWithSlackButton from "@/components/SignInWithSlackButton.vue";
import MainContent from "@/components/MainContent.vue";
import WelcomeToForminder from "@/components/WelcomeToForminder.vue";
</script>

<template>
  <main>
    <MainContent>
      <template #default>
        <WelcomeToForminder/>
        <div class="max-w-xs md:max-w-md py-8">
          Log in to view your team's forms and submissions.
        </div>
        <SignInWithSlackButton/>
      </template>
    </MainContent>
  </main>
</template>

<style>
</style>
