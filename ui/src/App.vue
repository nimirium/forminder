<script setup lang="ts">
function removeURLParameter(url: string, parameter: string): string {
  const urlparts = url.split('?');
  if (urlparts.length >= 2) {

    const prefix = encodeURIComponent(parameter) + '=';
    const pars = urlparts[1].split(/[&;]/g);

    for (let i = pars.length; i-- > 0;) {
      if (pars[i].lastIndexOf(prefix, 0) !== -1) {
        pars.splice(i, 1);
      }
    }

    return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
  }
  return url;
}

if (window.history.pushState) {
  let newUrl = removeURLParameter(window.location.href, 'code');
  newUrl = removeURLParameter(newUrl, 'state');
  window.history.pushState({}, '', newUrl);
}
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
            <RouterLink to="/about" class="px-3 md:px-5 py-3 hidden md:block">About</RouterLink>
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
            <RouterLink to="/add-to-slack" class="px-3 md:px-5 py-1 md:py-3 md:hidden">Add to Slack</RouterLink>
            <RouterLink to="/how-to-use" class="px-3 md:px-5 py-1 md:py-3 md:hidden">How to use</RouterLink>
            <RouterLink to="/use-cases" class="px-3 md:px-5 py-1 md:py-3 md:hidden">Use cases</RouterLink>
            <RouterLink to="/about" class="px-3 md:px-5 py-1 md:py-3 md:hidden">About</RouterLink>
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
