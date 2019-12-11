<template>
  <div class="container">
    <h3 class="title">Steganopy</h3>
    <h5 class="subtitle">Steganography with serverless architecture.</h5>
    <section class="section columns">
      <div class="column">
        <feature-card
          title="Data concealing"
          description="Embed data into an image."
          url="/conceal"
        />
      </div>
      <div class="column">
        <feature-card
          title="Data detecting"
          description="Check if an image contains any secret data."
          url="/detect"
        />
      </div>
      <div class="column">
        <feature-card
          title="Data revealing"
          description="Extract secret data from an image."
          url="/reveal"
        />
      </div>
    </section>
  </div>
</template>

<script>
import FeatureCard from '../components/feature-card'

export default {
  components: { FeatureCard }
}
</script>

<style scoped>
.section {
  padding: 3rem 0;
}
</style>
