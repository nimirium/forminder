<script setup lang="ts">
</script>

<template>
  <div id="app-container" class="min-h-screen flex flex-col">

    <div class="p-8 md:p-0">
    <header>

        <nav>

          <div class="flex justify-center items-center">
            <RouterLink to="/" class="px-3 md:px-5 py-3">Home</RouterLink>
            <RouterLink to="/login" class="px-3 md:px-5 py-3">Log in</RouterLink>
            <RouterLink to="/add-to-slack" class="px-3 md:px-5 py-3 hidden md:block">Add to Slack</RouterLink>
            <RouterLink to="/how-to-use" class="px-3 md:px-5 py-3 hidden md:block">How to use</RouterLink>
            <RouterLink to="/use-cases" class="px-3 md:px-5 py-3 hidden md:block">Use cases</RouterLink>
          </div>

        </nav>
      </header>
    </div>


    <div class="flex-grow mx-2">
      <RouterView/>
    </div>

    <div class="py-3 mt-10">
      <footer>

        <nav>

          <div class="flex justify-center items-center flex-col md:flex-row">
            <RouterLink to="/how-to-use" class="px-3 md:px-5 py-1 md:py-3 md:hidden">How to use</RouterLink>
            <RouterLink to="/use-cases" class="px-3 md:px-5 py-1 md:py-3 md:hidden">Use cases</RouterLink>
            <RouterLink to="/about" class="px-3 md:px-5 py-1 md:py-3">About</RouterLink>
            <RouterLink to="/terms-and-conditions" class="px-3 md:px-5 py-1 md:py-3">Terms and Conditions</RouterLink>
          </div>

        </nav>

      </footer>
    </div>
  </div>
</template>

<style scoped>
.router-link-active {
  font-weight: bold;
}
</style>
