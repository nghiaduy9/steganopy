<template>
  <div class="container">
    <h3 class="title">Data revealing</h3>
    <h5 class="subtitle">Extract data from an image.</h5>
    <upload-form
      title="Upload image to decode:"
      accept-file="image/*"
      :file-name="imageFileName"
      @input="changeImageFile"
    />
    <div class="columns">
      <div class="control column">
        <button class="button is-dark" @click="decode">Decode</button>
      </div>
    </div>
    <div v-if="responseDataUrl">
      <div class="field has-addons">
        <div class="control">
          <input class="input" type="text" :value="responseDataUrl" readonly />
        </div>
        <div class="control">
          <a class="button is-info">
            <span class="file-icon">
              <ion-icon name="cloud-download"></ion-icon>
            </span>
            <span class="file-label">
              <a :href="responseDataUrl" target="_blank">Download</a>
            </span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import UploadForm from '../components/upload-form'

export default {
  name: 'Decode',
  components: {
    UploadForm
  },
  data() {
    return {
      imageFileName: 'No image choosen...',
      imageFile: null,
      responseDataUrl: ''
    }
  },
  methods: {
    changeImageFile(event) {
      this.imageFile = event
      this.imageFileName = event[0].name
    },
    decode() {
      axios
        .post('/api/reveal')
        .then((response) => {
          if (response.data.url !== undefined) {
            this.responseDataUrl = response.data.url
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
a {
  color: aliceblue;
}
@media only screen and (min-width: 768px) {
  .card {
    max-width: 40%;
    margin: 15px auto;
  }
}
@media only screen and (min-width: 1024px) {
  .card {
    max-width: 33%;
    margin: 15px auto;
  }
}
</style>
