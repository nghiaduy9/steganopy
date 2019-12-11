<template>
  <div class="container">
    <h3 class="title">Data detecting</h3>
    <h5 class="subtitle">Check if an image contains any secret data.</h5>
    <uploadForm
      title="Upload image to detect:"
      acceptFile="image/*"
      :fileName="imageFileName"
      @input="changeImageFile"
    />
    <div class="columns">
      <div class="control column">
        <button class="button is-info" @click="check">Check</button>
      </div>
    </div>
    <div v-if="responseDataUrl">
      <div v-if="hasData" class="has-text-success is-centered">
        <span class="icon">
          <ion-icon name="checkmark"></ion-icon>
        </span>
        <span>This image has data inside!</span>
      </div>
      <div v-else class="has-text-danger">
        <span class="icon">
          <ion-icon name="close"></ion-icon>
        </span>
        <span>This image doesn't have data inside!</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import uploadForm from '../components/upload-form'

export default {
  name: 'Check',
  components: {
    uploadForm
  },
  data() {
    return {
      imageFileName: 'No image choosen...',
      imageFile: null,
      responseDataUrl: '',
      hasData: Boolean
    }
  },
  methods: {
    changeImageFile(event) {
      this.imageFile = event
      this.imageFileName = event[0].name
    },
    check() {
      const formData = new FormData()
      formData.append('files', this.imageFile[0])
      axios
        .post('/api/detect', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        .then((response) => {
          if (response.data.result !== undefined) {
            this.hasData = response.data.result
          } else {
            console.log(response.data.error)
          }
        })
        .catch((error) => {
          console.log(error)
        })
    }
  }
}
</script>

<style>
template {
  margin: auto;
}
</style>
