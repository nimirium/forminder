<script setup lang="ts">
</script>

<template>
  <main>
    <div class="flex flex-col">
      <div class="center flex items-center justify-center">
        <div class="w-1/2 max-w-2xl">
          <img src="@/assets/forminder_no_bg.png" alt="Forminder">
        </div>
        <div class="flex flex-col items-start justify-center">
          <div class="welcome grow">Welcome to</div>
          <div class="forminder grow">Forminder</div>
          <div class="max-w-xs md:max-w-md py-8">
            Effortlessly manage form-filling on Slack. Create customized forms, schedule reminders, and streamline your workflow with ease.
          </div>
          <RouterLink to="/login" class="nav-link py-3 underline">Log in</RouterLink>
          <RouterLink to="/add-to-slack" class="nav-link py-3 underline">Add to Slack</RouterLink>
        </div>
      </div>
    </div>
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

.slack-button img {
  width: 100%;
  max-width: 200px;
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
