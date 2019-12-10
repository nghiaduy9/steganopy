<template>
  <div class="is-centered">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title is-centered">DECODE</p>
      </header>
      <div class="card-content">
        <div class="content">
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
                  <span class="file-label" @click="dowloadResponseData">Download</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UploadForm from '../components/upload-form'

export default {
  name: 'Decode',
  components: {
    UploadForm
  },
  data() {
    return {
      imageFileName: 'No image choosen...',
      imageFile: File,
      responseDataUrl: ''
    }
  },
  methods: {
    changeImageFile(event) {
      this.imageFile = event
      this.imageFileName = event[0].name
    },
    decode() {},
    dowloadResponseData() {}
  }
}
</script>

<style>
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
