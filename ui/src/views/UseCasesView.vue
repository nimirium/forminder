<template>
  <main>
    <MainContent title="Forminder Use Cases" :hide-image-if-small="true">
      <template #default>
        <div class="max-w-xs md:max-w-md">
          <ForminderUseCase
              title="Use Case #1: Project Update"
              description="Stay up-to-date with your team's daily work progress. This form allows team members to share what they worked on, any blockers they encountered, and their sprint status. It fosters transparency and helps identify issues early on."
              example-description="Example: Daily Progress Form"
              code='/forminder create --form-name="Daily Progress" --multiline-field="What did you work on today?" --multiline-field="Any blockers?" --select-field="Sprint Status:Behind Schedule,On Schedule”'
              scheduleDescription="Schedule daily, close to the end of the day "
          />
          <ForminderUseCase
              title="Use Case #2: Friend Referral"
              description="Simplify the process of referring friends for open positions within your company. Collect relevant information about the referred candidate and their qualifications, making it easier to assess their fit for the position."
              example-description="Example: Friend Referral Form"
              :code='friendReferralCommand'
          >
            <template #fill-form>
              <TextAndCode text="Fill the form" code="/forminder fill friend referral"></TextAndCode>
            </template>
          </ForminderUseCase>
          <ForminderUseCase
              title="Use Case #3: Office Dogs"
              description="Coordinate and manage the presence of dogs in your office."
              example-description="Example: Office Dogs Form"
              code="/forminder create --form-name=“Office Dogs” --text-field=“Dog name” --text-field=“Dog name” --select-field=“Is your dog friendly with other dogs?:Yes,No” --select-field=“Are you bringing your dog to work tomorrow?:Yes,No”"
              schedule-description="Schedule weekly"
          />
        </div>

      </template>
    </MainContent>
  </main>
</template>

<script lang="ts">
import MainContent from "@/components/MainContent.vue";
import ForminderUseCase from "@/views/ForminderUseCase.vue";
import TextAndCode from "@/components/TextAndCode.vue";

export default {
  name: "UseCasesView",
  components: {TextAndCode, ForminderUseCase, MainContent},
  data: function () {
    return {
      friendReferralCommand: "/forminder create --form-name=\"Friend Referral\" --text-field=\"Your Name\" --text-field=\"Friend's Name\" --text-field=\"Friend's Email\" --text-field=\"Friend's LinkedIn Profile\" --select-field=\"Position:Software Engineer,Product Manager,Designer,Marketing Specialist\" --multiline-field=\"Why do you recommend them?”"
    }

  }
}
</script>

