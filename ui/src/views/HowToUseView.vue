<template>
  <main>
    <MainContent title="How to use Forminder" :hide-image-if-small="true">
      <template #default>
        <TextAndCode text="1. Create a form with" code="/forminder create"></TextAndCode>
        <TextAndCode text="2. View forms with" code="/forminder list"></TextAndCode>
        <img src="@/assets/form_in_slack.png" alt="Example form in slack chat" class="drop-shadow-md rounded-lg max-w-sm md:max-w-lg m-2">
        <TextAndCode text="3. Fill a form with" code="/forminder fill"></TextAndCode>
        <div class="flex py-4 items-center">
          <div class="max-w-xs md:max-w-md">
            4. Schedule the form
          </div>
          <img src="@/assets/schedule_button.png" alt="Schedule button" class="drop-shadow-md rounded-lg w-32 ml-2.5">
        </div>
        <div class="max-w-xs md:max-w-md">
          5. View and export submissions
        </div>
        <img src="@/assets/export_button.png" alt="Schedule button" class="drop-shadow-md rounded-lg w-64 m-2.5">
      </template>
    </MainContent>
  </main>
</template>

<script lang="ts">
import MainContent from "@/components/MainContent.vue";
import TextAndCode from "@/components/TextAndCode.vue";
export default {
  name: "HowToUseView",
  components: {TextAndCode, MainContent}
}
</script>

<style scoped>

</style>
