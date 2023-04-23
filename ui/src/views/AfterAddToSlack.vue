<script setup lang="ts">
import MainContent from "@/components/MainContent.vue";
import TextAndCode from "@/components/TextAndCode.vue";

</script>

<template>
  <main>
    <MainContent :hide-image-if-small="true">
      <template #default>
        <div class="welcome grow">Congratulations on adding</div>
        <div class="forminder grow">Forminder</div>
        <div class="welcome grow">to your workspace!</div>
        <div class="py-8">
          <TextAndCode text="Get started by typing" code="/forminder" text-after="in any Slack chat."></TextAndCode>
        </div>
        <div class="max-w-xs md:max-w-md">
          Learn more about leveraging Forminder in our
          <RouterLink to="/how-to-use" class="nav-link font-semibold underline">how to use guide</RouterLink>,
          or explore possible
          <RouterLink to="/use-cases" class="nav-link font-semibold underline">use case examples</RouterLink>.
        </div>
      </template>
    </MainContent>
  </main>
</template>

<style scoped>
.welcome {
  font-family: sans-serif;
  font-size: 1.5rem;
}

.forminder {
  font-family: 'Lobster Two', cursive;
  font-size: 4rem;
  font-weight: 700;
}

/* Media query for small screen */
@media (max-width: 720px) {
  .welcome {
    font-size: 1.2rem;
  }

  .forminder {
    font-size: 1.5rem;
  }
}
</style>
