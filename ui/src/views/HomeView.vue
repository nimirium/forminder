<script setup lang="ts">
// import TheWelcome from '../components/TheWelcome.vue'
import SignInWithSlack from "@/components/SignInWithSlack.vue";
</script>

<template>
  <main>
<!--    <TheWelcome />-->
    <div class="flex flex-col">
      <div class="center flex items-center justify-center">
        <div class="w-1/2">
          <img src="@/assets/forminder_no_bg.png" alt="Forminder">
        </div>
        <div class="flex flex-col items-start justify-center">
          <div class="welcome grow">Welcome to</div>
          <div class="forminder grow">Forminder</div>
          <div class="hidden md:block">
            <SignInWithSlack/>
          </div>
        </div>
      </div>
      <div class="md:hidden center">
        <SignInWithSlack/>
      </div>
    </div>
  </main>
</template>
