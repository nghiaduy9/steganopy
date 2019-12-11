<template>
  <nuxt-link :to="url">
    <div class="box is-flex">
      <h4 class="title is-4 has-text-white">{{ title }}</h4>
      <h6 class="subtitle is-6 has-text-light">{{ description }}</h6>
    </div>
  </nuxt-link>
</template>

<script>
export default {
  props: {
    title: { type: String, required: true },
    description: { type: String, default: '' },
    url: { type: String, required: true }
  }
}
</script>

<style scoped>
.box {
  border-radius: 1rem;
  background-image: url(/sample-image.jpg);
  background-position: center center;
  background-size: cover;
  width: 20vw;
  height: 50vh;
}
.box:hover {
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url(/sample-image.jpg);
}
.is-flex {
  flex-direction: column;
  justify-content: center;
}
</style>
