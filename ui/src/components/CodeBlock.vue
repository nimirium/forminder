<template>
  <div class="mycode-box">
    <div class="mycode-text">
      <span>
         {{ code }}
      </span>
      <font-awesome-icon :icon="['fa', 'copy']" class="pl-2 hover:cursor-pointer" />
    </div>
  </div>
</template>

<script>
export default {
  name: "CodeBlock",
  props: {
    code: {
      type: String,
      required: true,
    },
  }
}
</script>

<style scoped>
.mycode-box {
  background: #F6F6F6;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 15px;
  margin-left: 10px;
}

.mycode-text {
  font-family: 'IBM Plex Mono', monospace;
  font-weight: 400;
  color: #2E2E2E;
  padding: 10px;
}
</style>
