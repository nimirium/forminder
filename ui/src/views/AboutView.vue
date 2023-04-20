<script setup lang="ts">
import MainContent from "@/components/MainContent.vue";
import sophieImageUrl from '@/assets/sophie.jpeg';
</script>

<template>
  <main>
    <MainContent title="About the Developer">
      <template #image>
        <div class="w-80 m-8 max-w-xl hidden md:block">
          <img :src="sophieImageUrl" alt="Sophie" class="rounded-full">
        </div>
      </template>
      <template #default>
        <div class="max-w-xs md:max-w-md m-8">
          <div class="w-48 m-8 log md:hidden">
            <img :src="sophieImageUrl" alt="Sophie" class="rounded-full">
          </div>
          Hi! I'm Sophie, a Full Stack developer and a proud mom. My expertise lies in cloud services, and I specialize in helping companies create efficient, reliable, and scalable software solutions.
          <br/><br/>
          Forminder began as a personal project to fulfill my need for tracking my daily work accomplishments. Now that it's production-ready, I believe it can greatly benefit other individuals and companies looking to improve their productivity and organization.
          <br/><br/>
          Outside of development, I have a deep interest in urban planning and enjoy immersing myself in gaming.
          <br/><br/>
          Feel free to reach out to me at <a href="mailto: sophie.fogel@gmail.com" class="font-semibold">sophie.fogel@gmail.com</a> or connect with me on <a href="https://www.linkedin.com/in/sophie-fogel-bb57309a/" target="_blank" class="font-semibold">LinkedIn</a>. I'd be happy to discuss your ideas, answer any questions, or explore collaboration opportunities.
        </div>
      </template>
    </MainContent>
  </main>
</template>

<style scoped>
</style>
