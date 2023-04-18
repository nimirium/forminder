<template>
  <a :href="slackAuthUrl" class="slack-button m-5">
    <img src="https://platform.slack-edge.com/img/sign_in_with_slack.png" alt="Sign in with Slack" />
  </a>
</template>

<script>
import { useRoute } from 'vue-router';

const route = useRoute();

export default {
  name: 'SignInWithSlack',
  data() {
    const clientId = import.meta.env.VITE_SLACK_CLIENT_ID;
    const redirectUrl = route?.query?.redirectUrl || `${import.meta.env.VITE_DOMAIN}/forms`;

    const slackAuthUrl = `https://slack.com/oauth/v2/authorize?client_id=${clientId}&scope=users:read&user_scope=&redirect_uri=${redirectUrl}`;

    return {
      slackAuthUrl,
    };
  },
};
</script>

<style scoped></style>
