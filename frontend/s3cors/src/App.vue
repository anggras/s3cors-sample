<script setup>
import HelloWorld from './components/HelloWorld.vue'
import UploadTest from './components/UploadTest.vue';
import cdkout from "../../../output.json"

let stack = cdkout.S3CorsStack;

let allApiEndpoint = undefined;
let testApiEndpoint = undefined;
let localhostApiEndpoint = undefined;

for (const aKey in stack) {
  if (Object.hasOwnProperty.call(stack, aKey)) {
    if (aKey.startsWith("All")) {
      allApiEndpoint = stack[aKey];
    } else if (aKey.startsWith("Test")) {
      testApiEndpoint = stack[aKey];
    } else if (aKey.startsWith("Local")) {
      localhostApiEndpoint = stack[aKey];
    }
  }
}
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div>
  </header>

  <main>
    <UploadTest title="CORS All (allowed origin *)" :endpoint="allApiEndpoint"/>
    <UploadTest title="CORS Test (allowed origin https://test.com)" :endpoint="testApiEndpoint"/>
    <UploadTest title="CORS Localhost (allowed origin http://locahost:5173)" :endpoint="localhostApiEndpoint"/>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
