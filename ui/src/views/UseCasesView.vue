<template>
  <main>
    <MainContent title="Forminder Use Cases" :hide-image-if-small="true">
      <template #default>
        <div class="max-w-xs md:max-w-md">
          <div class="font-bold py-3">
            Use Case #1: Project Update
          </div>
          <div class="py-3">
            Stay up-to-date with your team's daily work progress. This form allows team members to share what they worked on, any blockers they encountered, and their sprint status. It fosters transparency and helps identify issues early on.
          </div>
          <div class="py-3 italic">
            Example: Daily Progress Form
          </div>
          <CodeBlock :code="projectUpdateCommand"></CodeBlock>
        </div>

      </template>
    </MainContent>
  </main>
</template>

<script lang="ts">
import MainContent from "@/components/MainContent.vue";
import TextAndCode from "@/components/TextAndCode.vue";
import CodeBlock from "@/components/CodeBlock.vue";
export default {
  name: "UseCasesView",
  components: {CodeBlock, MainContent},
  data: function () {
    return {
      projectUpdateCommand: '/forminder create --form-name="Daily Progress" --multiline-field="What did you work on today?" --multiline-field="Any blockers?" --select-field="Sprint Status:Behind Schedule,On Schedule”',
    }

  }
}
</script>

<style scoped>

</style>
