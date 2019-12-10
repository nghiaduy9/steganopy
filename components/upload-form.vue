<template>
  <div class="columns">
    <div class="field column is-clipped">
      <label class="label is-medium">{{ title }}</label>
      <div class="file control has-name">
        <label class="file-label">
          <input
            class="file-input"
            type="file"
            :accept="acceptFile"
            @input="$emit('input', $event.target.files)"
          />
          <span class="file-cta">
            <span class="file-icon">
              <ion-icon name="cloud-upload"></ion-icon>
            </span>
            <span class="file-label">Choose a file…</span>
          </span>
          <span class="file-name">{{ fileName }}</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['title', 'acceptFile', 'fileName', 'value']
}
</script>

<style>
label.file-label {
  width: 100%;
}
span.file-name {
  width: 100%;
}
.file-cta {
  max-width: 50%;
}
</style>
