<template>
  <a :href="addToSlackUrl">
    <img
        alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png"
        srcSet="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x"/>
  </a>
</template>

<script>
export default {
  name: 'AddToSlackButton',
  data() {
    const clientId = import.meta.env.VITE_SLACK_CLIENT_ID;
    const redirectUrl = `${import.meta.env.VITE_DOMAIN}/after-add-to-slack`;
    const addToSlackUrl = `https://slack.com/oauth/v2/authorize?client_id=${clientId}&scope=channels:read,commands,groups:read,im:read,mpim:read,users:read,chat:write&user_scope=&redirect_uri=${redirectUrl}`
    return {
      addToSlackUrl,
    };
  },
};
</script>

<style scoped></style>
