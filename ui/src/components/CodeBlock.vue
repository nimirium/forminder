<template>
  <div class="mycode-box">
    <div class="mycode-text">
      <div class="mycode-content-wrapper">
        <span class="mycode-content">
          {{ code }}
        </span>
      </div>
      <font-awesome-icon
          :icon="['fa', 'copy']"
          class="pl-2 hover:cursor-pointer"
          @click="copyToClipboard"
      />
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
  },
  methods: {
    async copyToClipboard() {
      try {
        await navigator.clipboard.writeText(this.code);
      } catch (err) {
        console.error("Failed to copy code: ", err);
      }
    },
  },
};
</script>

<style scoped>
.mycode-box {
  background: #F6F6F6;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 15px;
  overflow: hidden;
}

.mycode-text {
  font-family: 'IBM Plex Mono', monospace;
  font-weight: 400;
  color: #2E2E2E;
  padding: 10px;
  display: flex;
  align-items: center;
}

.mycode-content-wrapper {
  overflow-x: auto;
  white-space: nowrap;
  flex-grow: 1;
  scrollbar-width: none; /* For Firefox */
}

.mycode-content-wrapper::-webkit-scrollbar {
  display: none; /* For WebKit browsers (e.g., Chrome, Safari) */
}

.mycode-content {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
