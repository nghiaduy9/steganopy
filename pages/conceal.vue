<template>
  <div class="container">
    <h3 class="title">Data concealing</h3>
    <h5 class="subtitle">Embed data into an image.</h5>
    <upload-form
      title="Upload secret data file:"
      :file-name="secretFileName"
      @input="changeSecretFile"
    />
    <upload-form
      title="Upload image to hide:"
      accept-file="image/jpeg,image/png"
      :file-name="imageFileName"
      @input="changeImageFile"
    />
    <div class="columns">
      <div class="control column">
        <button class="button is-dark" @click="encode">Encode</button>
      </div>
    </div>
    <div v-if="responseImageUrl">
      <div>
        <a :href="responseImageUrl" target="_blank">
          <img :src="responseImageUrl" alt="Embed-image" />
        </a>
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
      const formData = new FormData()
      formData.append('files', this.imageFile[0])
      formData.append('files', this.secretData[0])
      axios
        .post('/api/conceal', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        .then((response) => {
          if (response.data.url !== undefined) {
            this.responseImageUrl = response.data.url
          } else {
            console.log(response.data.error)
          }
        })
        .catch((errors) => console.log(errors))
    }
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
