<template>
  <div class="welcome grow">Welcome to</div>
  <div class="forminder grow">Forminder</div>
</template>

<script>
export default {
  name: "WelcomeToForminder"
}
</script>

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
