<template>
  <div class="is-centered">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title is-centered">ENCODE</p>
      </header>
      <div class="card-content">
        <div class="content">
          <uploadForm
            title="Upload secret data file:"
            :fileName="secretFileName"
            @input="changeSecretFile"
          />
          <uploadForm
            title="Upload image to hide:"
            acceptFile="image/*"
            :fileName="imageFileName"
            @input="changeImageFile"
          />
          <div class="columns">
            <div class="control column">
              <button class="button is-dark" @click="encode">Encode</button>
            </div>
          </div>
          <div v-if="responseImageUrl">
            <div class="field has-addons">
              <div class="control">
                <input class="input" type="text" :value="responseImageUrl" readonly />
              </div>
              <div class="control">
                <a class="button is-info">
                  <span class="file-icon">
                    <ion-icon name="cloud-download"></ion-icon>
                  </span>
                  <span class="file-label" @click="dowloadResponseImage">Download</span>
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
import axios from 'axios'
import UploadForm from '../components/upload-form'

export default {
  name: 'Encode',
  components: {
    UploadForm
  },
  data() {
    return {
      secretData: null,
      imageFile: null,
      secretFileName: 'No file choosen...',
      imageFileName: 'No image choosen...',
      responseImageUrl: ''
    }
  },
  methods: {
    changeSecretFile(event) {
      this.secretData = event
      this.secretFileName = event[0].name
    },
    changeImageFile(event) {
      this.imageFile = event
      this.imageFileName = event[0].name
    },
    encode() {
      console.log(this.imageFile)
      console.log(this.secretData)
      const formData = new FormData()
      formData.append('files', this.imageFile[0])
      formData.append('files', this.secretData[0])
      axios
        .post('/api/conceal', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        .then((response) => console.log(response))
        .catch((errors) => console.log(errors))
    },
    dowloadResponseImage() {}
  }
}
</script>

<style scoped>
.columns {
  margin: auto;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
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