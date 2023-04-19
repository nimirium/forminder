<template>
  <a :href="addToSlackUrl">
    <img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png"
         srcSet="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x"/>
  </a>
</template>

<script>
export default {
  name: 'AddToSlackButton',
  data() {
    const clientId = import.meta.env.VITE_SLACK_CLIENT_ID;
    const addToSlackUrl = `https://slack.com/oauth/v2/authorize?client_id=${clientId}&scope=chat:write,commands,users:read,channels:read,groups:read,mpim:read,im:read&user_scope=`
    return {
      addToSlackUrl,
    };
  },
};
</script>

<style scoped></style>
